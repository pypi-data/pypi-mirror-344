from torch import nn

from ...rl.reinforce import *
from ...rl.utils import *
from typing import Optional, Union, Literal, List
import numpy as np
import torch


class PolicyNet(nn.Module):
    def __init__(self, config):
        super(PolicyNet, self).__init__()
        self.__lstm = nn.LSTM(input_size = config.node_dim,
                              hidden_size = config.CELL_SIZE,
                              num_layers = config.LAYERS_NUM).to(config.device)
        self.__mu = nn.Linear(config.CELL_SIZE, config.output_dim_actor).to(config.device)
        self.__sigma = nn.Linear(config.CELL_SIZE, config.output_dim_actor).to(config.device)
        self.__distribution = torch.distributions.Normal
        self.__config = config

    def forward(self, x, h, c):
        cell_out, (h_, c_) = self.__lstm(x, (h, c))
        mu = self.__mu(cell_out)
        sigma = torch.sigmoid(self.__sigma(cell_out))
        return mu, sigma, h_, c_

    def sampler(self, inputs, ht, ct):
        mu, sigma, ht_, ct_ = self.forward(inputs, ht, ct)
        normal = self.__distribution(mu, sigma)
        sample_w = torch.clip(normal.sample(), 0, 1).reshape(self.__config.action_shape)
        return sample_w, ht_, ct_


class LDE(REINFORCE_Agent):
    def __init__(self, config):

        self.config = config
        # self.__BATCH_SIZE = self.config.train_batch_size
        self.__BATCH_SIZE = None
        self.config.NP = 50
        self.config.TRAJECTORY_NUM = 20
        self.config.TRAJECTORY_LENGTH = 50
        self.config.CELL_SIZE = 50
        self.config.BINS = 5
        self.config.LAYERS_NUM = 1
        self.config.lr_model = 0.005
        self.config.lr_decay = 1
        self.config.gamma = 0.99
        self.config.output_dim_actor = self.config.NP * 2
        # self.config.action_shape = (1, self.__BATCH_SIZE, self.config.NP * 2,)
        self.config.action_shape = None
        self.config.node_dim = self.config.NP + 2 * self.config.BINS
        # self.__feature_shape = (self.__BATCH_SIZE, self.config.node_dim,)
        self.__feature_shape = None

        model = PolicyNet(self.config)
        self.config.optimizer = 'Adam'
        # origin LDE doesn't have clip
        self.config.max_grad_norm = math.inf
        self.device = self.config.device
        self.config.agent_save_dir = self.config.agent_save_dir + self.__str__() + '/' + self.config.train_name + '/'
        super().__init__(self.config, {'model': model}, [self.config.lr_model])

    def __str__(self):
        return "LDE"

    def __discounted_norm_rewards(self, r):
        for ep in range(self.config.TRAJECTORY_NUM * self.__BATCH_SIZE):
            length = r.shape[0] // self.config.TRAJECTORY_NUM
            single_rs = r[ep * length: ep * length + length]
            discounted_rs = np.zeros_like(single_rs)
            running_add = 0.
            # 动态计算length 这里需要
            for t in reversed(range(0, single_rs.shape[-1])):
                running_add = running_add * self.config.gamma + single_rs[t]
                discounted_rs[t] = running_add
            if ep == 0:
                all_disc_norm_rs = discounted_rs
            else:
                all_disc_norm_rs = np.hstack((all_disc_norm_rs, discounted_rs))
        return all_disc_norm_rs

    def train_episode(self,
                      envs,
                      seeds: Optional[Union[int, List[int], np.ndarray]],
                      para_mode: Literal['dummy', 'subproc', 'ray', 'ray-subproc'] = 'dummy',
                      #   asynchronous: Literal[None, 'idle', 'restart', 'continue']=None,
                      #   num_cpus: Optional[Union[int, None]]=1,
                      #   num_gpus: int=0,
                      compute_resource = {},
                      tb_logger = None,
                      required_info = {}):
        num_cpus = None
        num_gpus = 0 if self.config.device == 'cpu' else torch.cuda.device_count()
        if 'num_cpus' in compute_resource.keys():
            num_cpus = compute_resource['num_cpus']
        if 'num_gpus' in compute_resource.keys():
            num_gpus = compute_resource['num_gpus']
        env = ParallelEnv(envs, para_mode, num_cpus = num_cpus, num_gpus = num_gpus)

        self.__BATCH_SIZE = self.config.train_batch_size
        self.config.action_shape = (1, self.__BATCH_SIZE, self.config.NP * 2,)
        self.__feature_shape = (self.__BATCH_SIZE, self.config.node_dim,)

        self.optimizer.zero_grad()
        inputs_batch = []
        action_batch = []
        hs_batch = []
        cs_batch = []
        rewards_batch = []

        env.seed(seeds)
        _R = torch.zeros(len(env))
        _reward = []
        for l in range(self.config.TRAJECTORY_NUM):
            input_net = env.reset()

            # raise
            h0 = torch.zeros(self.config.LAYERS_NUM, self.__BATCH_SIZE, self.config.CELL_SIZE).to(self.config.device)
            c0 = torch.zeros(self.config.LAYERS_NUM, self.__BATCH_SIZE, self.config.CELL_SIZE).to(self.config.device)
            for t in range(self.config.TRAJECTORY_LENGTH):
                input_net = input_net.reshape(self.__feature_shape)
                # [bs, NP+BINS*2]
                action, h_, c_ = self.model.sampler(torch.Tensor(input_net[None, :]).to(self.config.device), h0, c0)  # parameter controller
                action = action.reshape(self.__BATCH_SIZE, 1, -1).cpu().numpy()
                # action = np.squeeze(action.cpu().numpy(), axis=1)

                inputs_batch.append(input_net)
                action_batch.append(action.squeeze(axis = 1))
                next_input, reward, is_done, _ = env.step(action)

                hs_batch.append(torch.squeeze(h0, axis = 0))
                cs_batch.append(torch.squeeze(c0, axis = 0))
                rewards_batch.append(reward.reshape(self.__BATCH_SIZE))
                _R += reward.reshape(-1)
                _reward.append(torch.Tensor(reward))
                h0 = h_
                c0 = c_
                input_net = next_input.copy()
                if env.all_done():
                    break

        inputs = [np.stack(inputs_batch, axis = 0).transpose((1, 0, 2)).reshape(-1, self.config.node_dim)]
        actions = [np.stack(action_batch, axis = 0).transpose((1, 0, 2)).reshape(-1, self.config.output_dim_actor)]
        hs = [torch.stack(hs_batch, axis = 0).permute(1, 0, 2).reshape(-1, self.config.CELL_SIZE)]
        cs = [torch.stack(cs_batch, axis = 0).permute(1, 0, 2).reshape(-1, self.config.CELL_SIZE)]
        rewards = [np.stack(rewards_batch, axis = 0).transpose((1, 0)).flatten()]

        # update network parameters
        all_eps_mean, all_eps_std, all_eps_h, all_eps_c = self.model.forward(torch.Tensor(np.vstack(inputs)[None, :]).to(self.device),
                                                                             torch.vstack(hs)[None, :],
                                                                             torch.vstack(cs)[None, :])
        actions = torch.Tensor(np.vstack(actions)).to(self.device)
        all_eps_mean = torch.squeeze(all_eps_mean, 0).to(self.device)
        all_eps_std = torch.squeeze(all_eps_std, 0).to(self.device)
        normal_dis = torch.distributions.Normal(all_eps_mean, all_eps_std)
        log_prob = torch.sum(normal_dis.log_prob(actions + 1e-8), 1).to(self.device)
        all_eps_dis_reward = self.__discounted_norm_rewards(np.hstack(rewards))
        loss = - torch.mean(log_prob * torch.Tensor(all_eps_dis_reward).to(self.device))
        loss.backward()
        grad_norms = clip_grad_norms(self.optimizer.param_groups)

        self.optimizer.step()
        self.learning_time += 1

        if self.learning_time >= (self.config.save_interval * self.cur_checkpoint) and self.config.end_mode == "step":
            save_class(self.config.agent_save_dir, 'checkpoint-' + str(self.cur_checkpoint), self)
            self.cur_checkpoint += 1

        if not self.config.no_tb:
            self.log_to_tb_train(tb_logger, self.learning_time,
                                 grad_norms,
                                 loss,
                                 _R, _reward,
                                 log_prob)

        is_train_ended = self.learning_time >= self.config.max_learning_step
        _Rs = _R.detach().numpy().tolist()
        return_info = {'return': _Rs, 'loss': [loss.item()], 'learn_steps': self.learning_time, }
        env_cost = env.get_env_attr('cost')
        return_info['gbest'] = env_cost[-1]
        for key in required_info.keys():
            return_info[key] = env.get_env_attr(required_info[key])
        env.close()

        return is_train_ended, return_info

    def rollout_episode(self,
                        env,
                        seed = None,
                        required_info = {}):
        with torch.no_grad():
            self.__BATCH_SIZE = 1
            self.config.action_shape = (1, self.__BATCH_SIZE, self.config.NP * 2,)
            self.__feature_shape = (self.__BATCH_SIZE, self.config.node_dim,)

            env.seed(seed)
            is_done = False
            input_net = env.reset()

            h0 = torch.zeros(self.config.LAYERS_NUM, self.__BATCH_SIZE, self.config.CELL_SIZE).to(self.config.device)
            c0 = torch.zeros(self.config.LAYERS_NUM, self.__BATCH_SIZE, self.config.CELL_SIZE).to(self.config.device)
            R = 0
            while not is_done:
                # [bs, NP+BINS*2]
                action, h_, c_ = self.model.sampler(torch.Tensor(input_net[None, :]).to(self.device), h0, c0)  # parameter controller
                action = action.reshape(1, self.__BATCH_SIZE, -1) 
                action = np.squeeze(action.cpu().numpy(), axis = 0)
                next_input, reward, is_done, _ = env.step(action)
                R += np.mean(reward)
                h0 = h_
                c0 = c_
                input_net = next_input.copy()
            env_cost = env.get_env_attr('cost')
            env_fes = env.get_env_attr('fes')
            results = {'cost': env_cost, 'fes': env_fes, 'return': R}
            if self.config.full_meta_data:
                meta_X = env.get_env_attr('meta_X')
                meta_Cost = env.get_env_attr('meta_Cost')
                metadata = {'X': meta_X, 'Cost': meta_Cost}
                results['metadata'] = metadata

            for key in required_info.keys():
                results[key] = getattr(env, required_info[key])
            return results

    def rollout_batch_episode(self,
                              envs,
                              seeds = None,
                              para_mode: Literal['dummy', 'subproc', 'ray', 'ray-subproc'] = 'dummy',
                              #   asynchronous: Literal[None, 'idle', 'restart', 'continue']=None,
                              #   num_cpus: Optional[Union[int, None]]=1,
                              #   num_gpus: int=0,
                              compute_resource = {},
                              required_info = {}):
        num_cpus = None
        num_gpus = 0 if self.config.device == 'cpu' else torch.cuda.device_count()
        if 'num_cpus' in compute_resource.keys():
            num_cpus = compute_resource['num_cpus']
        if 'num_gpus' in compute_resource.keys():
            num_gpus = compute_resource['num_gpus']
        env = ParallelEnv(envs, para_mode, num_cpus = num_cpus, num_gpus = num_gpus)

        env.seed(seeds)
        input_net = env.reset()
        try:
            input_net = torch.Tensor(input_net).to(self.device)
        except:
            pass
        h0 = torch.zeros(self.config.LAYERS_NUM, self.__BATCH_SIZE, self.config.CELL_SIZE).to(self.config.device)
        c0 = torch.zeros(self.config.LAYERS_NUM, self.__BATCH_SIZE, self.config.CELL_SIZE).to(self.config.device)
        R = torch.zeros(len(env))

        while not env.all_done():
            # [bs, NP+BINS*2]
            action, h_, c_ = self.model.sampler(torch.Tensor(input_net[None, :]).to(self.devicee), h0, c0)  # parameter controller
            action = action.reshape(self.__BATCH_SIZE, 1, -1).cpu().numpy()
            next_input, reward, is_done, _ = env.step(action)
            R += reward.reshape(-1)
            h0 = h_
            c0 = c_
            input_net = next_input.copy()
        _Rs = R.detach().numpy().tolist()
        env_cost = env.get_env_attr('cost')
        env_fes = env.get_env_attr('fes')
        results = {'cost': env_cost, 'fes': env_fes, 'return': _Rs}

        if self.config.full_meta_data:
            meta_X = env.get_env_attr('meta_X')
            meta_Cost = env.get_env_attr('meta_Cost')
            metadata = {'X': meta_X, 'Cost': meta_Cost}
            results['metadata'] = metadata

        for key in required_info.keys():
            results[key] = env.get_env_attr(required_info[key])
        return results




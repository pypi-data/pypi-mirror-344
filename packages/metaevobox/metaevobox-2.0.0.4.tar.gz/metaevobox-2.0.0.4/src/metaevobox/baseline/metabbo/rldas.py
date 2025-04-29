from torch.distributions import Categorical

from .networks import *
from ...rl.ppo import *
from ...rl.utils import *


class Actor(nn.Module):
    def __init__(self, dim, optimizer_num, feature_dim, device):
        super().__init__()
        self.device = device
        self.embedders = nn.ModuleList([])
        for i in range(optimizer_num):
            self.embedders.append((nn.Sequential(*[
                nn.Linear(dim, 64), nn.ReLU(),
                nn.Linear(64, 1), nn.ReLU(),
            ])).to(device))
            self.embedders.append(nn.Sequential(*[
                nn.Linear(dim, 64), nn.ReLU(),
                nn.Linear(64, 1), nn.ReLU(),
            ]).to(device))
        self.embedder_final = nn.Sequential(*[
            nn.Linear(feature_dim + optimizer_num * 2, 64), nn.Tanh(),
        ]).to(device)
        self.model = nn.Sequential(*[
            nn.Linear(64, 16), nn.Tanh(),
            nn.Linear(16, optimizer_num),  nn.Softmax(),
        ]).to(device)

    def forward(self, obs, fix_action = None, require_entropy = False):
        feature = list(obs[:, 0])
        if not isinstance(feature, torch.Tensor):
            feature = torch.Tensor(feature).to(self.device)
        moves = []
        for i in range(len(self.embedders)):
            moves.append(self.embedders[i](torch.Tensor(list(obs[:, i + 1])).to(self.device)))
        moves = torch.cat(moves, dim=-1)
        batch = obs.shape[0]
        feature = torch.cat((feature, moves), dim=-1).view(batch, -1)
        feature = self.embedder_final(feature)
        logits = self.model(feature)
        policy = Categorical(logits)
        if fix_action is None:
            actions = policy.sample()
        else:
            actions = fix_action
        log_prob = policy.log_prob(actions)

        if require_entropy:
            entropy = policy.entropy()  # for logging only

            return (actions, log_prob, entropy)
        else:
            return (actions, log_prob)

class Critic(nn.Module):
    def __init__(self, dim, optimizer_num, feature_dim, device):
        super().__init__()
        self.device = device
        self.embedders = nn.ModuleList([])
        for i in range(optimizer_num):
            self.embedders.append((nn.Sequential(*[
                nn.Linear(dim, 64), nn.ReLU(),
                nn.Linear(64, 1), nn.ReLU(),
            ])).to(device))
            self.embedders.append(nn.Sequential(*[
                nn.Linear(dim, 64), nn.ReLU(),
                nn.Linear(64, 1), nn.ReLU(),
            ]).to(device))
        self.embedder_final = nn.Sequential(*[
            nn.Linear(feature_dim + optimizer_num * 2, 64), nn.Tanh(),
        ]).to(device)
        self.model = nn.Sequential(*[
            nn.Linear(64, 16), nn.Tanh(),
            nn.Linear(16, 1), # nn.Softmax(),
        ]).to(device)

    def forward(self, obs):
        feature = list(obs[:, 0])
        if not isinstance(feature, torch.Tensor):
            feature = torch.Tensor(feature).to(self.device)
        moves = []
        for i in range(len(self.embedders)):
            moves.append(self.embedders[i](torch.Tensor(list(obs[:, i + 1])).to(self.device)))
        moves = torch.cat(moves, dim=-1)
        batch = obs.shape[0]
        feature = torch.cat((feature, moves), dim=-1).view(batch, -1)
        feature = self.embedder_final(feature)
        batch = obs.shape[0]
        bl_val = self.model(feature.view(batch, -1))[:, 0]
        return bl_val.detach(), bl_val

class RLDAS(PPO_Agent):
    def __init__(self, config):
        self.config = config

        self.config.optimizer = 'Adam'
        self.config.lr = 1e-5

        self.config.feature_dim = 9
        self.config.optim_num = 3

        self.config.gamma = 0.99
        self.config.n_step = 10
        self.config.K_epochs = None # RLDAS can calculate base optimizer
        self.config.eps_clip = 0.1
        self.config.max_grad_norm = 0.1


        actor = Actor(dim = self.config.dim,
                      optimizer_num = self.config.optim_num,
                      feature_dim = self.config.feature_dim,
                      device = self.config.device)

        critic = Critic(dim = self.config.dim,
                        optimizer_num = self.config.optim_num,
                        feature_dim = self.config.feature_dim,
                        device = self.config.device)
        self.config.agent_save_dir = self.config.agent_save_dir + self.__str__() + '/' + self.config.train_name + '/'
        super().__init__(self.config, {'actor': actor, 'critic': critic}, self.config.lr)

    def __str__(self):
        return "RLDAS"

    def train_episode(self,
                      envs,
                      seeds: Optional[Union[int, List[int], np.ndarray]],
                      para_mode: Literal['dummy', 'subproc', 'ray', 'ray-subproc'] = 'dummy',
                      # todo: asynchronous: Literal[None, 'idle', 'restart', 'continue'] = None,
                      # num_cpus: Optional[Union[int, None]] = 1,
                      # num_gpus: int = 0,
                      compute_resource = {},
                      tb_logger = None,
                      required_info = {}):
        num_cpus = None
        num_gpus = 0 if self.config.device == 'cpu' else torch.cuda.device_count()
        if 'num_cpus' in compute_resource.keys():
            num_cpus = compute_resource['num_cpus']
        if 'num_gpus' in compute_resource.keys():
            num_gpus = compute_resource['num_gpus']
        k = 1
        for env in envs:
            k = max(k, int(0.3*(env.optimizer.MaxFEs // env.optimizer.period)))

        env = ParallelEnv(envs, para_mode, num_cpus, num_gpus)
        env.seed(seeds)
        memory = Memory()

        # params for training
        gamma = self.gamma
        n_step = self.n_step

        K_epochs = k
        eps_clip = self.eps_clip

        state = env.reset()
        try:
            state = torch.Tensor(state).to(self.device)
        except:
            pass

        t = 0
        # initial_cost = obj
        _R = torch.zeros(len(env))
        _loss = []
        # sample trajectory
        while not env.all_done():
            t_s = t
            total_cost = 0
            entropy = []
            bl_val_detached = []
            bl_val = []

            # accumulate transition
            while t - t_s < n_step and not env.all_done():

                memory.states.append(state.copy())
                action, log_lh, entro_p = self.actor(state, require_entropy = True)


                memory.actions.append(action.clone() if isinstance(action, torch.Tensor) else copy.deepcopy(action))
                memory.logprobs.append(log_lh)

                entropy.append(entro_p.detach().cpu())

                baseline_val_detached, baseline_val = self.critic(state)

                bl_val_detached.append(baseline_val_detached)
                bl_val.append(baseline_val)

                # state transient
                state, rewards, is_end, info = env.step(action.detach().cpu().numpy())
                memory.rewards.append(torch.Tensor(rewards).to(self.device))
                # print('step:{},max_reward:{}'.format(t,torch.max(rewards)))
                _R += rewards
                # store info

                # next
                t = t + 1

                try:
                    state = torch.Tensor(state).to(self.device)
                except:
                    pass

            # store info
            t_time = t - t_s
            total_cost = total_cost / t_time

            # begin update
            old_actions = torch.stack(memory.actions)
            try:
                old_states = torch.stack(memory.states).detach()  # .view(t_time, bs, ps, dim_f)
            except:
                pass
            # old_actions = all_actions.view(t_time, bs, ps, -1)
            old_logprobs = torch.stack(memory.logprobs).detach().view(-1)

            # Optimize PPO policy for K mini-epochs:
            old_value = None
            for _k in range(K_epochs):
                if _k == 0:
                    logprobs = memory.logprobs

                else:
                    # Evaluating old actions and values :
                    logprobs = []
                    bl_val_detached = []
                    bl_val = []
                    entropy = []

                    for tt in range(t_time):
                        # get new action_prob
                        _, log_p, entro_p = self.actor(state, fix_action = old_actions[tt], require_entropy = True)

                        logprobs.append(log_p)
                        entropy.append(entro_p.detach().cpu())
                        baseline_val_detached, baseline_val = self.critic(state)

                        bl_val_detached.append(baseline_val_detached)
                        bl_val.append(baseline_val)

                logprobs = torch.stack(logprobs).view(-1)
                entropy = torch.stack(entropy).view(-1)
                bl_val_detached = torch.stack(bl_val_detached).view(-1)
                bl_val = torch.stack(bl_val).view(-1)

                # get traget value for critic
                Reward = []
                reward_reversed = memory.rewards[::-1]
                # get next value
                R = self.critic(state)[0]
                critic_output = R.clone()
                for r in range(len(reward_reversed)):
                    R = R * gamma + reward_reversed[r]
                    Reward.append(R)
                # clip the target:
                Reward = torch.stack(Reward[::-1], 0)
                Reward = Reward.view(-1)

                # Finding the ratio (pi_theta / pi_theta__old):
                ratios = torch.exp(logprobs - old_logprobs.detach())

                # Finding Surrogate Loss:
                advantages = Reward - bl_val_detached

                surr1 = ratios * advantages
                surr2 = torch.clamp(ratios, 1 - eps_clip, 1 + eps_clip) * advantages
                reinforce_loss = -torch.min(surr1, surr2).mean()

                # define baseline loss
                if old_value is None:
                    baseline_loss = ((bl_val - Reward) ** 2).mean()
                    old_value = bl_val.detach()
                else:
                    vpredclipped = old_value + torch.clamp(bl_val - old_value, - eps_clip, eps_clip)
                    v_max = torch.max(((bl_val - Reward) ** 2), ((vpredclipped - Reward) ** 2))
                    baseline_loss = v_max.mean()

                # check K-L divergence (for logging only)
                approx_kl_divergence = (.5 * (old_logprobs.detach() - logprobs) ** 2).mean().detach()
                approx_kl_divergence[torch.isinf(approx_kl_divergence)] = 0
                # calculate loss
                loss = baseline_loss + reinforce_loss

                # update gradient step
                self.optimizer.zero_grad()
                loss.backward()
                _loss.append(loss.item())
                # Clip gradient norm and get (clipped) gradient norms for logging
                # current_step = int(pre_step + t//n_step * K_epochs  + _k)
                grad_norms = clip_grad_norms(self.optimizer.param_groups, self.config.max_grad_norm)

                # perform gradient descent
                self.optimizer.step()
                self.learning_time += 1
                if self.learning_time >= (self.config.save_interval * self.cur_checkpoint) and self.config.end_mode == "step":
                    save_class(self.config.agent_save_dir, 'checkpoint-' + str(self.cur_checkpoint), self)
                    self.cur_checkpoint += 1

                if not self.config.no_tb:
                    self.log_to_tb_train(tb_logger, self.learning_time,
                                         grad_norms,
                                         reinforce_loss, baseline_loss,
                                         _R, Reward, memory.rewards,
                                         critic_output, logprobs, entropy, approx_kl_divergence)

                if self.learning_time >= self.config.max_learning_step:
                    memory.clear_memory()
                    _Rs = _R.detach().numpy().tolist()
                    return_info = {'return': _Rs, 'loss': _loss,'learn_steps': self.learning_time, }
                    env_cost = env.get_env_attr('cost')
                    return_info['normalizer'] = env_cost[0]
                    return_info['gbest'] = env_cost[-1]
                    for key in required_info:
                        return_info[key] = env.get_env_attr(key)
                    env.close()
                    return self.learning_time >= self.config.max_learning_step, return_info

            memory.clear_memory()

        is_train_ended = self.learning_time >= self.config.max_learning_step
        _Rs = _R.detach().numpy().tolist()
        return_info = {'return': _Rs, 'loss': _loss,'learn_steps': self.learning_time,}
        env_cost = env.get_env_attr('cost')
        return_info['normalizer'] = env_cost[0]
        return_info['gbest'] = env_cost[-1]
        for key in required_info:
            return_info[key] = env.get_env_attr(key)
        env.close()
        return is_train_ended, return_info

    def rollout_batch_episode(self,
                              envs,
                              seeds = None,
                              para_mode: Literal['dummy', 'subproc', 'ray', 'ray-subproc'] = 'dummy',
                              # todo: asynchronous: Literal[None, 'idle', 'restart', 'continue'] = None,
                              # num_cpus: Optional[Union[int, None]] = 1,
                              # num_gpus: int = 0,
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
        state = env.reset()
        try:
            state = torch.Tensor(state).to(self.device)
        except:
            pass

        R = torch.zeros(len(env))
        # sample trajectory
        while not env.all_done():
            with torch.no_grad():
                action, log_lh = self.actor(state)

            # state transient
            state, rewards, is_end, info = env.step(action.detach().cpu().numpy())
            # print('step:{},max_reward:{}'.format(t,torch.max(rewards)))
            R += torch.Tensor(rewards).squeeze()
            # store info
            try:
                state = torch.Tensor(state).to(self.device)
            except:
                pass
        _Rs = R.detach().numpy().tolist()
        env_cost = env.get_env_attr('cost')
        env_fes = env.get_env_attr('fes')
        results = {'cost': env_cost, 'fes': env_fes, 'return': _Rs}
        for key in required_info.keys():
            results[key] = env.get_env_attr(required_info[key])
        return results

    def rollout_episode(self,
                        env,
                        seed = None,
                        required_info = {}):
        with torch.no_grad():
            if seed is not None:
                env.seed(seed)
            is_done = False
            state = env.reset()
            R = 0
            while not is_done:
                try:
                    state = torch.Tensor(state).to(self.device)
                except:
                    pass
                action = self.actor(np.array([state]))[0]
                action = action.cpu().numpy().squeeze()
                state, reward, is_done, info = env.step(action)
                R += reward
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

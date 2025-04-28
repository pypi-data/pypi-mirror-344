import copy

import torch
from torch import nn
from ...rl.basic_agent import Basic_Agent
from ...environment.parallelenv.parallelenv import ParallelEnv
from typing import Optional, Union, Literal, List
import numpy as np
from ...rl.utils import clip_grad_norms, save_class
from cmaes import CMA
from dill import loads, dumps

class LGA(Basic_Agent):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

        self.M = 256
        self.T = 50
        self.J = 256
        self.optimizer = CMA(mean = np.zeros(673),
                             sigma = 0.1,
                             population_size = self.M)

        self.x_population = None
        self.meta_performances = None
        self.optimizer_step()
        self.best_x = self.x_population[0]

        self.costs = None
        self.best_lga = None
        self.gbest = 1e-10

        self.learning_step = 0
        self.cur_checkpoint = 0

        self.task_step = 0
        self.config.agent_save_dir = self.config.agent_save_dir + self.__str__() + '/' + self.config.train_name + '/'
        save_class(self.config.agent_save_dir, 'checkpoint-' + str(self.cur_checkpoint), self)
        self.cur_checkpoint += 1

    def __str__(self):
        return "LGA"

    def get_step(self):
        return self.learning_step

    def optimizer_step(self):
        # inital sampling
        samples = []
        for _ in range(self.M):
            samples.append(self.optimizer.ask())
        self.x_population = np.vstack(samples)
        self.meta_performances = [[] for _ in range(self.M)]

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
        env = ParallelEnv(envs, para_mode, num_cpus = num_cpus, num_gpus = num_gpus)
        env.seed(seeds)

        env.set_env_attr("rng_cpu", "None")
        if self.config.device != 'cpu':
            env.set_env_attr("rng_gpu", "None")
        env_population = [loads(dumps(env)) for _ in range(self.M)]

        for i, e in enumerate(env_population):
            e.reset()
            action = {'net': self.x_population[i],
                      'skip_step': self.T}

            action = [copy.deepcopy(action) for _ in range(len(env))]
            sub_best, _, _, _ = e.step(action)

            self.meta_performances[i].append(sub_best)

        self.task_step += len(env)
        # Task 256
        if self.task_step % 256 == 0:
            self.update()
            self.learning_step += 1
            if not self.config.no_tb:
                self.log_to_tb_train(tb_logger, self.learning_step, self.gbest)

        if self.learning_step >= (self.config.save_interval * self.cur_checkpoint) and self.config.end_mode == "step":
            save_class(self.config.agent_save_dir, 'checkpoint-' + str(self.cur_checkpoint), self)
            self.cur_checkpoint += 1

        return_info = {'return': 0, 'loss':0 ,'learn_steps': self.learning_step, }
        return_info['gbest'] = env_population[0].get_env_attr('cost')[-1],
        for key in required_info.keys():
            return_info[key] = env_population[0].get_env_attr(required_info[key])
        for i, e in enumerate(env_population):
            e.close()
        # return exceed_max_ls
        return self.learning_step >= self.config.max_learning_step, return_info

    def rollout_episode(self, env, seed = None, required_info = {}):
        env.seed(seed)
        R = 0
        # use best_x to rollout
        env.reset()
        action = {'net': self.best_x,
                  'skip_step': None}
        gbest, r, _, _ = env.step(action)
        R += r

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

        R = np.zeros(len(env))
        # use best_x to rollout
        env.reset()
        action = {'net': self.best_x,
                  'skip_step': None}
        action = [copy.deepcopy(action) for _ in range(len(env))]
        gbest, r, _, _ = env.step(action)
        R += np.array(r).squeeze().tolist()

        env_cost = env.get_env_attr('cost')
        env_fes = env.get_env_attr('fes')
        results = {'cost': env_cost, 'fes': env_fes, 'return': R}
        if self.config.full_meta_data:
            meta_X = env.get_env_attr('meta_X')
            meta_Cost = env.get_env_attr('meta_Cost')
            metadata = {'X': meta_X, 'Cost': meta_Cost}
            results['metadata'] = metadata

        for key in required_info.keys():
            results[key] = env.get_env_attr(required_info[key])

        return results

        # if self.Policy is None:
        #     # beginning
        #     ps_list = env.get_env_attr('NP')
        #     NP = ps_list[0]
        #     self.Policy = [Policy(pop_size = NP, mu = self.config.mu[m], sigma = self.config.sigma, DK = self.config.DK, device = self.config.device).to(self.config.device)
        #                    for m in range(self.config.M)]
        #
        #     self.j = 0
        #
        # for p, policy in enumerate(self.Policy):
        #     state = env.reset() # [bs, NP]
        #     policy.eval() # don't need gradient
        #     for t in range(self.config.T):
        #         action = [policy for _ in range(len(env))]
        #
        #         state, reward, is_end, info = env.step(action)
        #
        #     min_f = np.min(state, axis = 1)
        #     for f in min_f:
        #         self.Memory[p][self.j] = f
        #         self.j += 1
        #
        #         if self.j == self.config.J:
        #             # cal Z-score
        #             M_mean = np.mean(self.Memory, axis = 1, keepdims = True)
        #             M_std = np.std(self.Memory, axis = 1, keepdims = True)
        #             self.Memory = (self.Memory - M_mean) / (M_std + 1e-8)
        #
        #             self.meta_fitness = np.median(self.Memory, axis = 1)
        #
        #             self.Memory = np.zeros((self.config.M, self.config.J), dtype = np.float64)
        #
        #             A = (self.meta_fitness - np.mean(self.meta_fitness)) / np.std(self.meta_fitness) # [NP]
        #             self.config.mu = self.config.mu + self.config.alpha / (self.config.M * self.config.sigma) * np.dot(self.config.mu, A)
        #
        #             self.learning_time += 1
        #
        #             # reinit
        #             NP = self.meta_fitness.shape[0]
        #             self.Policy = [Policy(pop_size = NP, mu = self.config.mu[m], sigma = self.config.sigma, DK = self.config.DK, device = self.config.device).to(self.config.device)
        #                            for m in range(self.config.M)]
        #
        #             self.mu_best = self.config.mu[np.argmax(self.meta_fitness)]
        #
        #             self.j = 0
        #
        #             if self.learning_time >= (self.config.save_interval * self.cur_checkpoint) and self.config.end_mode == "step":
        #                 save_class(self.config.agent_save_dir, 'checkpoint' + str(self.cur_checkpoint), copy.deepcopy(self))
        #                 self.cur_checkpoint += 1
        #
        #             if self.learning_time >= self.config.max_learning_step:
        #                 break
        #     if self.learning_time >= self.config.max_learning_step:
        #         break
        # is_train_ended = self.learning_time >= self.config.max_learning_step
        # return_info = {'return': 0, 'learn_steps': self.learning_time}
        # env.close()
        #
        # return is_train_ended, return_info

    def update(self):
        scores = np.stack(self.meta_performances).reshape(self.M, -1) # [M, J]
        M_mean = np.mean(scores, axis = 1, keepdims = True)
        M_std = np.std(scores, axis = 1, keepdims = True)

        scores = (scores - M_mean) / (M_std + 1e-8)

        self.fitness = np.median(scores, axis = 1)

        self.meta_performances = [[] for _ in range(self.M)]

        if np.min(self.fitness) > self.gbest:
            self.gbest = np.max(self.fitness)
            self.best_lga = np.argmax(self.fitness)
            self.best_x = self.x_population[self.best_lga]

        self.optimizer.tell(list(zip(self.x_population, self.fitness)))
        self.optimizer_step()

    def log_to_tb_train(self, tb_logger, mini_step,gbest,
                        extra_info = {}):
        # Iterate over the extra_info dictionary and log data to tb_logger
        # extra_info: Dict[str, Dict[str, Union[List[str], List[Union[int, float]]]]] = {
        #     "loss": {"name": [], "data": [0.5]},  # No "name", logs under "loss"
        #     "accuracy": {"name": ["top1", "top5"], "data": [85.2, 92.5]},  # Logs as "accuracy/top1" and "accuracy/top5"
        #     "learning_rate": {"name": ["adam", "sgd"], "data": [0.001, 0.01]}  # Logs as "learning_rate/adam" and "learning_rate/sgd"
        # }
        #
        # train metric
        tb_logger.add_scalar('train/gbest', self.gbest, mini_step)

        # extra info
        for key, value in extra_info.items():
            if not value['name']:
                tb_logger.add_scalar(f'{key}', value['data'][0], mini_step)
            else:
                name_list = value['name']
                data_list = value['data']
                for name, data in zip(name_list, data_list):
                    tb_logger.add_scalar(f'{key}/{name}', data, mini_step)






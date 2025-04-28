import torch
from torch import nn
from ...rl.basic_agent import Basic_Agent
from ...rl.utils import *
from cmaes import CMA
import copy
from ...environment.parallelenv.parallelenv import ParallelEnv
import numpy as np
from dill import loads, dumps
from typing import Optional, Union, Literal, List
import math

class LES(Basic_Agent):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

        self.meta_pop_size = 16
        self.skip_step = 50
        self.optimizer = CMA(mean = np.zeros(246), 
                             sigma = 0.1, 
                             population_size=self.meta_pop_size)
        
        # population in cmaes
        self.x_population = None
        self.meta_performances = None
        self.optimizer_step()
        self.best_x= self.x_population[0]

        self.costs = None
        self.best_les = None
        self.gbest = 1e10

        self.learning_step=0


        self.cur_checkpoint=0
        # save init agent
        self.config.agent_save_dir = self.config.agent_save_dir + self.__str__() + '/' + self.config.train_name + '/'
        save_class(self.config.agent_save_dir,'checkpoint-'+str(self.cur_checkpoint),self)
        self.cur_checkpoint+=1

    def __str__(self):
        return "LES"

    def get_step(self):
        return self.learning_step

    def update_setting(self, config):
        self.config.max_learning_step = config.max_learning_step
        self.config.agent_save_dir = config.agent_save_dir
        self.learning_step = 0
        save_class(self.config.agent_save_dir, 'checkpoint0', self)
        self.config.save_interval = config.save_interval
        self.cur_checkpoint = 1

    def optimizer_step(self):
        # inital sampling
        samples = []
        for _ in range(self.meta_pop_size):
            samples.append(self.optimizer.ask())
        self.x_population = np.vstack(samples)
        self.meta_performances = [[] for _ in range(self.meta_pop_size)]

    # eval task to get meta performance
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
        env = ParallelEnv(envs, para_mode, num_cpus=num_cpus, num_gpus=num_gpus)
        env.seed(seeds)

        env.set_env_attr("rng_cpu", "None")
        if self.config.device != 'cpu':
            env.set_env_attr("rng_gpu", "None")
        env_population = [loads(dumps(env)) for _ in range(self.meta_pop_size)]

        # sequential
        for i, e in enumerate(env_population):
            e.reset()
            action = {'attn':self.x_population[i][:68],
                      'mlp':self.x_population[i][68:],
                      'skip_step': self.skip_step}
            action = [copy.deepcopy(action) for _ in range(len(env))]
            sub_best, _, _, _ = e.step(action)
            
            self.meta_performances[i].append(sub_best)

        # todo: modify threshold
        self.learning_step += 1
            
        if self.learning_step % 10 == 0 and self.config.train_problem in ['protein','protein-torch']:
            self.train_epoch()
            if not self.config.no_tb:
                self.log_to_tb_train(tb_logger, self.learning_step, self.gbest)
            
        if self.learning_step >= (self.config.save_interval * self.cur_checkpoint) and self.config.end_mode == 'step':
            save_class(self.config.agent_save_dir, 'checkpoint-'+str(self.cur_checkpoint), self)
            self.cur_checkpoint += 1

        return_info = {'return': [0] * len(env), 'loss': [0], 'learn_steps': self.learning_step, }
        return_info['gbest'] = env_population[0].get_env_attr('cost')[-1],
        for key in required_info.keys():
            return_info[key] =  env_population[0].get_env_attr(required_info[key])
        for i, e in enumerate(env_population):
            e.close()
        # return exceed_max_ls
        return self.learning_step >= self.config.max_learning_step, return_info

    # meta train, update self.x_population
    def train_epoch(self):
        scores = np.stack(self.meta_performances).reshape(self.meta_pop_size, -1)
        

        self.costs = np.median((scores - np.mean(scores,axis=0)[None, :])/scores.std(axis=0)[None, :], axis=-1)
        
        # record x gbest
        if np.min(self.costs) < self.gbest:
            self.gbest = np.min(self.costs)
            self.best_les = np.argmin(self.costs)
            self.best_x=self.x_population[self.best_les]

        # update optimizer
        self.optimizer.tell(list(zip(self.x_population,self.costs)))
        self.optimizer_step()
        

    # rollout_episode need transform 
    def rollout_episode(self,env, seed = None, required_info = {}) :
        env.seed(seed)
        R = 0
        # use best_x to rollout
        env.reset()
        action = {'attn':self.best_x[:68],
                      'mlp':self.best_x[68:],}
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
                              required_info = {}) :
        num_cpus = None
        num_gpus = 0 if self.config.device == 'cpu' else torch.cuda.device_count()
        if 'num_cpus' in compute_resource.keys():
            num_cpus = compute_resource['num_cpus']
        if 'num_gpus' in compute_resource.keys():
            num_gpus = compute_resource['num_gpus']
        env = ParallelEnv(envs, para_mode, num_cpus=num_cpus, num_gpus=num_gpus)
        env.seed(seeds)

        R = np.zeros(len(env))
        # use best_x to rollout
        env.reset()
        action = {'attn':self.best_x[:68],
                      'mlp':self.best_x[68:],}
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

        # return {'cost':env.optimizer.cost,'fes': env.optimizer.FEs, 'return': R}

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


import pickle
import time
import torch
from tqdm import tqdm
from .environment.basic_environment import PBO_Env
from .environment.parallelenv import *
from .logger import *
import copy
from .environment.problem.utils import *
import numpy as np
import os, warnings
import matplotlib
import matplotlib.pyplot as plt
from .rl.utils import save_class
from tensorboardX import SummaryWriter
import pprint

from .environment.optimizer import (
    DEDDQN_Optimizer,
    DEDQN_Optimizer,
    RLHPSDE_Optimizer,
    LDE_Optimizer,
    QLPSO_Optimizer,
    RLEPSO_Optimizer,
    RLPSO_Optimizer,
    RNNOPT_Optimizer,
    GLEET_Optimizer,
    RLDAS_Optimizer,
    LES_Optimizer,
    NRLPSO_Optimizer,
    SYMBOL_Optimizer,
    RLDEAFL_Optimizer,
    SurrRLDE_Optimizer,
    RLEMMO_Optimizer,
    MADAC_Optimizer,
    GLHF_Optimizer,
    B2OPT_Optimizer,
    LGA_Optimizer,
    PSORLNS_Optimizer,
    L2T_Optimizer
)

from .baseline.bbo import (
    DE,
    JDE21,
    MADDE,
    NLSHADELBC,
    PSO,
    GLPSO,
    SDMSPSO,
    SAHLPSO,
    CMAES,
    Random_search,
    SHADE,
    MOEAD,
    MFEA
)
from .baseline.metabbo import (
    GLEET,
    DEDDQN,
    DEDQN,
    QLPSO,
    NRLPSO,
    RLHPSDE,
    RLDEAFL,
    LDE,
    RLPSO,
    SYMBOL,
    RLDAS,
    SurrRLDE,
    RLEMMO,
    GLHF,
    B2OPT,
    LGA,
    PSORLNS,
    LES,
    L2T,
    MADAC,
    RNNOPT
)


matplotlib.use('Agg')


class Trainer(object):
    def __init__(self, config, user_agent, user_optimizer, user_datasets):
        """
        Initializes the trainer with the given configuration.
        todo:重写注释
        Args:
            config (object): Configuration object containing the following attributes:
                - seed (int): Random seed for reproducibility.
                - resume_dir (str or None): Directory to resume training from a saved agent. 
                  If None, a new agent is created.
                - train_agent (str): Name of the training agent class to instantiate or load.
                - train_optimizer (str): Name of the optimizer class to instantiate.
                - problem (str): Problem type, e.g., 'bbob-surrogate'.
                - is_train (bool): Flag indicating whether the mode is training or not.

        Attributes:
            config (object): Stores the provided configuration.
            agent (object): The training agent, either newly created or loaded from a file.
            optimizer (object): The optimizer for training the agent.
            train_set (object): The training dataset constructed based on the problem type.
            test_set (object): The testing dataset constructed based on the problem type.

        Notes:
            - Sets random seeds for reproducibility across PyTorch, CUDA, and NumPy.
            - Configures PyTorch's cuDNN backend for deterministic behavior.
            - If `resume_dir` is provided, loads the agent from a pickle file and updates its settings.
            - Constructs the training and testing datasets based on the problem type.
        """
        self.config = config
        self.config.run_time = f"{self.config.run_time}_{self.config.train_problem}_{self.config.train_difficulty}"
        self.train_set, self.test_set = user_datasets

        self.config.dim = max(self.train_set.maxdim, self.test_set.maxdim)

        torch.manual_seed(self.config.seed)
        torch.cuda.manual_seed_all(self.config.seed)
        np.random.seed(self.config.seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        self.agent = user_agent

        self.optimizer = user_optimizer
            
        if self.config.train_parallel_mode == 'subproc' and self.agent.__str__() in ['B2OPT', 'GLHF', 'Surr_RLDE', 'RNNOPT'] and self.config.device != 'cpu':
            warnings.warn("Subproc training parallel mode for MetaBBO optimizers using CUDA will lead to CUDA kernel errors, changed to dummy.", category=UserWarning)
            self.config.train_parallel_mode = 'dummy'

    def save_log(self, epochs, steps, cost, returns, normalizer):
        """
        # Introduction
        Saves training logs including epochs, steps, costs, returns, and normalizer values for each problem in the training set. The logs are saved as NumPy arrays in a structured directory based on agent class and runtime.
        # Args:
        - epochs (list or np.ndarray): List or array of epoch indices.
        - steps (list or np.ndarray): List or array of step counts corresponding to each epoch.
        - cost (dict): Dictionary mapping problem names to lists of cost values per epoch.
        - returns (list or np.ndarray): List or array of return values per step.
        - normalizer (dict): Dictionary mapping problem names to lists of normalizer values per epoch.
        # Returns:
        - None
        # Notes:
        - Creates the log directory if it does not exist.
        - Pads cost and normalizer lists with their last value if they are shorter than the number of epochs.
        - Saves logs as `.npy` files for later analysis.
        """
        
        log_dir = self.config.log_dir + f'/train/{self.agent.__str__()}/{self.config.run_time}/log/'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return_save = np.stack((steps, returns),  0)
        np.save(log_dir+'return', return_save)
        for problem in self.train_set:
            name = problem.__str__()
            if len(cost[name]) == 0:
                continue
            while len(cost[name]) < len(epochs):
                cost[name].append(cost[name][-1])
                normalizer[name].append(normalizer[name][-1])
            cost_save = np.stack((epochs, cost[name], normalizer[name]),  0)
            np.save(log_dir+name+'_cost', cost_save)
            
    def save_class(dir, file_name, saving_class):
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(dir+file_name+'.pkl', 'wb') as f:
            pickle.dump(saving_class, f, -1)

    def train(self):
        """
        Trains the agent using the specified training configuration and dataset.

        This method orchestrates the training process, including setting up the training environment,
        managing epochs, logging progress, and saving checkpoints. It supports different training modes
        ("single" and "multi") and integrates with TensorBoard for logging.

        Attributes:
            self.config (object): Configuration object containing training parameters such as batch size,
                training mode, seed values, and logging options.
            self.train_set (object): Dataset object containing the training problems.
            self.agent (object): The agent to be trained.
            self.optimizer (object): Optimizer used for training.

        Workflow:
            1. Initializes TensorBoard logger if enabled.
            2. Configures batch size and training mode based on the configuration.
            3. Iteratively trains the agent for each epoch until the stopping condition is met.
            4. Logs training progress using tqdm and TensorBoard.
            5. Saves checkpoints at specified intervals.
            6. Handles random seed management for reproducibility.

        Returns:
            None
        """
        print(f'start training: {self.config.run_time}')
        print("following config:")
        pprint.pprint(vars(self.config))
        is_end = False
        tb_logger = None
        start_time = time.time()
        if not self.config.no_tb:
            if not os.path.exists(os.path.join('output/tensorboard', self.config.run_time)):
                os.makedirs(os.path.join('output/tensorboard', self.config.run_time))
            tb_logger = SummaryWriter(os.path.join('output/tensorboard', self.config.run_time))
            tb_logger.add_scalar("epoch-step", 0, 0)
        train_log = {'loss': [], 'learn_steps': [], 'return': [], 'runtime': [], 'config': copy.deepcopy(self.config)}
        if not os.path.exists(os.path.join('output/train_log', self.config.run_time)):
            os.makedirs(os.path.join('output/train_log', self.config.run_time))
        epoch = 0
        bs = self.config.train_batch_size
        if self.config.train_mode == "single":
            self.train_set.batch_size = 1
            self.train_set.ptr = [i for i in range(0, self.train_set.N)]
        elif self.config.train_mode == "multi":
            self.train_set.batch_size = bs

        epoch_seed = 100
        id_seed = 5
        seed = self.config.seed

        checkpoint_time0 = time.time()
        while not is_end:
            learn_step = 0
            self.train_set.shuffle()
            return_record = []
            loss_record = []
            with tqdm(range(int(np.ceil(self.train_set.N / self.train_set.batch_size))), desc = f'Training {self.agent.__class__.__name__} Epoch {epoch}') as pbar:
                for problem_id, problem in enumerate(self.train_set):
                    # set seed
                    seed_list = (epoch * epoch_seed + id_seed * (np.arange(bs) + bs * problem_id) + seed).tolist()

                    if self.config.train_mode == "single":
                        env_list = [PBO_Env(copy.deepcopy(problem[0]), copy.deepcopy(self.optimizer)) for _ in range(bs)] # bs
                    elif self.config.train_mode == "multi":
                        env_list = [PBO_Env(copy.deepcopy(p), copy.deepcopy(self.optimizer)) for p in problem] # bs

                    exceed_max_ls, train_meta_data = self.agent.train_episode(envs = env_list,
                                                                              seeds = seed_list,
                                                                              tb_logger = tb_logger,
                                                                              para_mode = self.config.train_parallel_mode,
                                                         )
                    # train_meta_data {'return': list[], 'loss': list[], 'learn_steps': int}

                    # exceed_max_ls, pbar_info_train = self.agent.train_episode(env)  # pbar_info -> dict
                    postfix_str = (
                        f"loss={np.mean(train_meta_data['loss']):.2e}, "
                        f"learn_steps={train_meta_data['learn_steps']}, "
                        f"return={np.mean(train_meta_data['return']):.2e}"
                    )

                    train_log['loss'].append(train_meta_data['loss'])
                    train_log['learn_steps'].append(train_meta_data['learn_steps'])
                    train_log['return'].append(train_meta_data['return'])
                    train_log['runtime'].append(time.time() - start_time)

                    with open(os.path.join('output/train_log', self.config.run_time, 'train_log.pkl'), 'wb') as f:
                        pickle.dump(train_log, f)
                    
                    pbar.set_postfix_str(postfix_str)
                    pbar.update(self.train_set.batch_size)
                    learn_step = train_meta_data['learn_steps']
                    
                    return_record.append(np.mean(train_meta_data['return']))
                    loss_record.append(np.mean(train_meta_data['loss']))
                    
                    # for id, p in enumerate(problem):
                    #     name = p.__str__()
                    #     cost_record[name].append(train_meta_data['gbest'][id])
                    #     normalizer_record[name].append(train_meta_data['normalizer'][id])
                    #     return_record.append(np.mean(train_meta_data['return']))
                    # learn_steps.append(learn_step)
                    # if learn_step >= (self.config.save_interval * self.agent.cur_checkpoint) and self.config.end_mode == "step":
                    #     save_class(self.config.agent_save_dir, 'checkpoint' + str(self.agent.cur_checkpoint), self.agent)
                    #     # 记录 checkpoint 和 total_step
                    #     with open(self.config.agent_save_dir + "/checkpoint_log.txt", "a") as f:
                    #         f.write(f"Checkpoint {self.agent.cur_checkpoint}: {learn_step}\n")

                    if self.config.end_mode == "step" and exceed_max_ls:
                        is_end = True
                        break
                # self.agent.train_epoch()
            # epoch_steps.append(learn_step)
            checkpoint_time_epoch = time.time() - checkpoint_time0
            epoch += 1

            if not self.config.no_tb:
                tb_logger.add_scalar("epoch-step", learn_step, epoch)
                tb_logger.add_scalar("epoch-avg-return", np.mean(return_record), epoch)
                tb_logger.add_scalar("epoch-avg-loss", np.mean(loss_record), epoch)

            if epoch >= (self.config.save_interval * self.agent.cur_checkpoint) and self.config.end_mode == "epoch":
                save_class(self.config.agent_save_dir, 'checkpoint-' + str(self.agent.cur_checkpoint), self.agent)
                # 记录 checkpoint 和 total_step
                with open(self.config.agent_save_dir + "/checkpoint_log.txt", "a") as f:
                    f.write(f"Checkpoint {self.agent.cur_checkpoint}: {learn_step}; Time: {checkpoint_time_epoch} s\n")

                # 保存状态
                # cpu_state = torch.random.get_rng_state()
                # cuda_state = torch.cuda.get_rng_state()
                # np_state = np.random.get_state()
                # self.rollout(self.agent.cur_checkpoint)
                # 载入
                # torch.random.set_rng_state(cpu_state)
                # torch.cuda.set_rng_state(cuda_state)
                # np.random.set_state(np_state)

                self.agent.cur_checkpoint += 1
            if self.config.end_mode == "epoch" and epoch >= self.config.max_epoch:
                is_end = True

    def rollout(self, checkpoint, rollout_run = 10):
        def rollout(self, checkpoint, rollout_run=10):
            """
            Perform a rollout operation using a specified checkpoint and number of runs.

            This method loads a pre-trained agent from a checkpoint file, initializes the 
            environment for testing, and performs a batch rollout to evaluate the agent's 
            performance on the test set.

            Args:
                checkpoint (int): The checkpoint index to load the agent from.
                rollout_run (int, optional): The number of rollout runs to perform for each 
                    problem in the test set. Defaults to 10.

            Behavior:
                - Seeds are set for reproducibility using the configuration's seed value.
                - The agent is loaded from a serialized file located in the `agent_save_dir`.
                - A deep copy of the test set is created for the rollout process.
                - The rollout is performed in batches, iterating through the test set.
                - For each problem in the test set, multiple environments are created, and 
                  the agent performs a batch rollout using these environments.
                - Progress is displayed using a progress bar, which updates with the agent's 
                  status.

            Notes:
                - The method uses PyTorch for deterministic behavior by setting seeds and 
                  disabling certain optimizations.
                - The `rollout_batch_episode` method of the agent is called to perform the 
                  rollout in parallel.

            Raises:
                FileNotFoundError: If the checkpoint file does not exist.
                pickle.UnpicklingError: If there is an error while loading the agent.

            """
        # 读取 agent
        torch.manual_seed(self.config.seed)
        torch.cuda.manual_seed(self.config.seed)
        np.random.seed(self.config.seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        with open(self.config.agent_save_dir + 'checkpoint' + str(checkpoint) + ".pkl", "rb") as f:
            agent = pickle.load(f)
        rollout_set = copy.deepcopy(self.test_set)
        bs = self.config.train_batch_size

        seed_list = list(range(1, rollout_run + 1)) * bs
        pbar = (rollout_set.N // bs + rollout_set.N % bs)
        with tqdm(range(pbar), desc = f"Rollout{checkpoint}") as pbar:
            for i, problem in enumerate(rollout_set):
                env_list = [PBO_Env(copy.deepcopy(p), copy.deepcopy(self.optimizer))
                            for p in problem
                            for _ in range(rollout_run)]
                with torch.no_grad():
                    meta_rollout_data = agent.rollout_batch_episode(envs = env_list,
                                                                    seeds = seed_list,
                                                                    para_mode = 'dummy',
                                                                    asynchronous = None,
                                                                    num_cpus = 1,
                                                                    num_gpus = 0,
                                                                    )
                pbar.set_postfix({'MetaBBO': agent.__str__()})
                pbar.update(1)
            
        
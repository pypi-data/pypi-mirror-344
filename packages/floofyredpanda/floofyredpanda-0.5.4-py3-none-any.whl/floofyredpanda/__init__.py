__version__ = "0.5.4"
from .nn import infer, register_output_converter
from .train import train
from .rl import train as rl
from .rl import predict

# core classes
from .rl import DQNAgent, DQN, ReplayBuffer, PrioritizedReplayBuffer
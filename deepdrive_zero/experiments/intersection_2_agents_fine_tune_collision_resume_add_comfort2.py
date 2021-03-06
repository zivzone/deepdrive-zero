import os
import sys

from deepdrive_zero import player
from deepdrive_zero.experiments import utils
from spinup.utils.run_utils import ExperimentGrid
from spinup import ppo_pytorch
import torch

experiment_name = os.path.basename(__file__)[:-3]
notes = """Driving smoothness is much improved, but we are colliding 
too much (~12% of episodes) and our g-force is still too high at around ~2.2,
with max g's still around 80! Also jerk is over 1000 m/s**3! and max
jerk is around 40k!! https://i.imgur.com/MWcTNXJ.jpg So going to 
increase collision, g-force, and jerk penalties. Also doubling epoch size
again because why not."""

env_config = dict(
    env_name='deepdrive-2d-intersection-w-gs-allow-decel-v0',
    is_intersection_map=True,
    expect_normalized_action_deltas=False,
    jerk_penalty_coeff=1.5 * 0.20 / (60*100),
    gforce_penalty_coeff=1.5 * 0.06,
    collision_penalty_coeff=1.5,
    end_on_harmful_gs=False,
    incent_win=True,
    constrain_controls=False,
)

net_config = dict(
    hidden_units=(256, 256),
    activation=torch.nn.Tanh
)

eg = ExperimentGrid(name=experiment_name)
eg.add('env_name', env_config['env_name'], '', False)
# eg.add('seed', 0)
eg.add('resume', '/home/c2/src/tmp/spinningup/data/intersection_2_agents_fine_tune_collision_resume_add_comfort1/intersection_2_agents_fine_tune_collision_resume_add_comfort1_s0_2020_03-13_21-45.39')
eg.add('reinitialize_optimizer_on_resume', True)
eg.add('pi_lr', 3e-6)  # doesn't seem to have an effect, but playing it safe and lowering learning rate since we're not restoring adam rates
eg.add('vf_lr', 1e-5)  # doesn't seem to have an effect, but playing it safe and lowering learning rate since we're not restoring adam rates
eg.add('epochs', 8000)
eg.add('steps_per_epoch', 16000)
eg.add('ac_kwargs:hidden_sizes', net_config['hidden_units'], 'hid')
eg.add('ac_kwargs:activation', net_config['activation'], '')
eg.add('notes', notes, '')
eg.add('run_filename', os.path.realpath(__file__), '')
eg.add('env_config', env_config, '')

def train():
    eg.run(ppo_pytorch)


if __name__ == '__main__':
    utils.run(train_fn=train, env_config=env_config, net_config=net_config)
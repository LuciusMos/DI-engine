from copy import deepcopy
from ding.entry import serial_pipeline
from easydict import EasyDict

qbert_dqn_config = dict(
    env=dict(
        collector_env_num=8,
        evaluator_env_num=8,
        n_evaluator_episode=8,
        stop_value=30000,
        env_id='QbertNoFrameskip-v4',
        frame_stack=4,
        manager=dict(shared_memory=False, )
    ),
    policy=dict(
        cuda=True,
        priority=False,
        model=dict(
            obs_shape=[4, 84, 84],
            action_shape=6,
            encoder_hidden_size_list=[128, 128, 512],
        ),
        nstep=3,
        discount_factor=0.99,
        learn=dict(
            update_per_collect=10,
            batch_size=32,
            learning_rate=0.0001,
            target_update_freq=500,
        ),
        collect=dict(n_sample=100, demonstration_info_path='path'
                     ),  #Users should add their own path here (path should lead to a well-trained model)
        eval=dict(evaluator=dict(eval_freq=4000, )),
        other=dict(
            eps=dict(
                type='exp',
                start=1.,
                end=0.05,
                decay=1000000,
            ),
            replay_buffer=dict(replay_buffer_size=400000, ),
        ),
    ),
)
qbert_dqn_config = EasyDict(qbert_dqn_config)
main_config = qbert_dqn_config
qbert_dqn_create_config = dict(
    env=dict(
        type='atari',
        import_names=['dizoo.atari.envs.atari_env'],
    ),
    env_manager=dict(type='subprocess', force_reproducibility=True),
    policy=dict(type='dqn'),
)
qbert_dqn_create_config = EasyDict(qbert_dqn_create_config)
create_config = qbert_dqn_create_config

if __name__ == '__main__':
    serial_pipeline((main_config, create_config), seed=0)

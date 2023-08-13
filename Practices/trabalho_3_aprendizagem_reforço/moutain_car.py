# experimento e aprendizado
import gymnasium as gym
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import DQN, PPO

# gravação de video
from pathlib import Path
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

import subprocess
import os
from pathlib import Path

def start_xvfb_server(display_num):
    devnull = open(os.devnull, 'w')
    subprocess.Popen(["Xvfb", f":{display_num}", "-screen", "0", "1024x768x24", "&"], stdout=devnull, stderr=devnull)

def stop_xvfb_server(display_num):
    subprocess.run(["killall", f"Xvfb:{display_num}"])

def remove_lock_file(display_num):
    lock_file = f"/tmp/.X{display_num}-lock"
    lock_path = Path(lock_file)
    if lock_path.is_file():
        lock_path.unlink()

def record_video(env_id, model, video_length=500, prefix="", video_folder="videos/"):
    # Iniciar o servidor Xvfb
    display_num = 1
    start_xvfb_server(display_num)

    # Remover o arquivo de bloqueio
    remove_lock_file(display_num)

    # Criar o diretório de vídeos, se não existir
    Path(video_folder).mkdir(parents=True, exist_ok=True)

    # Configurar o ambiente de avaliação de vídeo
    eval_env = DummyVecEnv([lambda: gym.make(env_id, render_mode="rgb_array")])
    eval_env = VecVideoRecorder(
        eval_env,
        video_folder=video_folder,
        record_video_trigger=lambda step: step == 0,
        video_length=video_length,
        name_prefix=prefix,
    )

    # Gravar o vídeo
    obs = eval_env.reset()
    for _ in range(video_length):
        action, _ = model.predict(obs)
        obs, _, _, _ = eval_env.step(action)

    # Parar o servidor Xvfb
    stop_xvfb_server(display_num)

# Exemplo de uso
env_id = "CartPole-v1"
model = PPO("MlpPolicy", env_id)
record_video(env_id, model, video_length=1000, prefix="cartpole", video_folder="videos/")

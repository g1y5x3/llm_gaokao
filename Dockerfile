FROM --platform=linux/amd64 pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel

RUN apt-get update && \
    apt-get install -y ssh && \ 
    apt-get install -y vim  && \
    apt-get install -y git  && \
    apt-get install -y tmux && \
    apt-get install -y libgl1 && \
    apt-get install -y python3-pip && \
    pip install transformers && \
    pip install flash_attn && \
    pip install numpy && \
    pip install Pillow && \
    pip install ipywidgets && \
    pip install ipykernel && \
    pip install notebook && \
    pip install wandb && \
    pip install tensorboard && \
    pip install datasets && \
    pip install timm && \
    pip install deepspeed && \
    pip install accelerate && \
    pip install sentencepiece

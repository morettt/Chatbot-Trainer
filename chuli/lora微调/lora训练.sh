#!/bin/bash

source activate py310_chat     
cd /root/Chatbot-Trainer
python finetune.py  data/  /root/autodl-tmp/glm-4-9b-chat  lora.yaml
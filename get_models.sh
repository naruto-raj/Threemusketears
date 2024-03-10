#!/bin/bash

# Define the folder and file paths
MODEL_FOLDER="models"
MODEL_FILE="llama-2-7b-chat.Q2_K.gguf"

# Check if the model folder exists, if not, create it
if [ ! -d "$MODEL_FOLDER" ]; then
    echo "Creating model folder..."
    mkdir "$MODEL_FOLDER"
else
    echo "Model folder already exists."
fi

# Check if the model file exists, if not, download it
if [ ! -f "$MODEL_FOLDER/$MODEL_FILE" ]; then
    echo "Downloading model file..."
    wget -O "$MODEL_FOLDER/$MODEL_FILE" "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf"
else
    echo "Model file already exists."
fi

echo "Task completed."

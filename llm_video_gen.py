from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat
from os.path import expanduser

from langchain_community.llms import LlamaCpp
import re

import base64
import os
from PIL import Image
from io import BytesIO
import requests
import time
import sys
import threading
import configparser

def load_api_key(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    api_key = config.get('API', 'api_key')
    return api_key

# Example usage
config_file = 'config.ini'

# authentication
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = load_api_key(config_file)
print(api_key)

#text to image
def text_to_image(api_key, prompt, debug=False):
    """ generates image based on text prompt and returns image data """
    try:
        response = requests.post(f"{api_host}/v1/generation/{engine_id}/text-to-image",
                                 headers={
                                     "Content-Type": "application/json",
                                     "Accept": "application/json",
                                     "Authorization": f"Bearer {api_key}"},
                                json={
                                    "text_prompts": [
                                        {"text": prompt}
                                    ],
                                    "cfg_scale": 7,
                                    "height": 576,
                                    "width": 1024,
                                    "samples": 1,
                                    "steps": 30,
                                })
        
        data = response.json()
    
        # set debug=true if debugging, will save file to local
        if debug:
            for i, image in enumerate(data["artifacts"]):
                with open(f"./txt2img_{i}.png", "wb") as f:
                    f.write(base64.b64decode(image["base64"]))
        
        image_base64 = response.json()["artifacts"][0]["base64"]  # Assuming only one image is generated
        decoded_image = base64.b64decode(image_base64)
        return decoded_image

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# image to video
def image_to_video(api_key, img, debug=False):
    """ generates video based on image and returns video data """
    try:
        get_response = requests.post(
            f"https://api.stability.ai/v2alpha/generation/image-to-video",
            headers={"authorization": api_key},
            files={"image": img},
            data={
                "seed": 0,
                "cfg_scale": 1.8,
                "motion_bucket_id": 127
            },
        )
        
        get_response.raise_for_status()
        generation_id = get_response.json().get('id')
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during image-to-video generation: {e}")

    try:
        status = 0
        time.sleep(10)
        while status!=200:
            time.sleep(5)
            post_response = requests.request(
            "GET",
            f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
            headers={
                'Accept': "video/*",  
                'authorization': api_key
            },)
            post_response.raise_for_status()
            status = post_response.status_code
        print('video Generated')
        # set debug=true if debugging, will save file to local
        if debug:
            with open("video.mp4", 'wb') as file:
                file.write(post_response.content)
                
        return post_response.content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during image-to-video result retrieval: {e}")

# Langchain setup llama
def lang_chains():
    template_message1 = [
        SystemMessage(content="You are the narrator of a dungeons and dragon game and you assist the player play the game based on the players responses, you ll ask the player to select suggested options answer"),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
    prompt_template1 = ChatPromptTemplate.from_messages(template_message1)
    template_message2 = [
        SystemMessage(content="You are the narrator of a dungeons and dragon game and assist in generating a text prompt for an image generation model for the given scenario"),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
    prompt_template2 = ChatPromptTemplate.from_messages(template_message2)
    model_path1 = "models/llama-2-7b-chat.Q2_K.gguf"
    model_path2 = "models/llama-2-7b-chat.Q2_K.gguf"

    llm1 = LlamaCpp(
        model_path=model_path1,
        streaming=False,
        n_ctx=2048,
    )
    llm2 = LlamaCpp(
        model_path=model_path2,
        streaming=False,
        n_ctx=512,
    )
    model1 = Llama2Chat(llm=llm1)
    model2 = Llama2Chat(llm=llm2)
    memory1 = ConversationBufferMemory(memory_key="chat_history", k=2, return_messages=True)
    # memory2 = ConversationBufferMemory(memory_key="prompt_history", k=2, return_messages=True)
    chain1 = LLMChain(llm=model1, prompt=prompt_template1, memory=memory1)
    chain2 = LLMChain(llm=model2, prompt=prompt_template2)
    return chain1,chain2

# add prefix to text to get prompt for text-image via llama
def add_prefix(text):
    return text + " . create a 10 word prompt to generate an image for this scene in format {prompt:'prompt'}"

# extract the prompt from the llama output
def extract_prompt(text):
    """
    Extracts the prompt from the given text.
    
    Args:
        text (str): The input text containing the prompt.
        
    Returns:
        str: The extracted prompt, or None if no prompt is found.
    """
    # Define a regular expression pattern to match the prompt
    pattern = r'"(.*?)"'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        # If a match is found, return the prompt (group 1 of the match)
        return match.group(1)
    else:
        # If no match is found, return None
        return None

# A typing effect
def typing_effect(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the sleep time to control the typing speed
    print() 

# Multi threaded execution
def run_typing_effect(text):
    typing_thread = threading.Thread(target=typing_effect, args=(text,))
    typing_thread.start()
 
# Execute llama to get prompt and story
def LLM_chat(text,chain1,chain2):
    image_prompt = chain2.run(
        text=add_prefix(text)
    )

    story = chain1.run(
            text=text
        )
    return image_prompt,story
def extract_options(story):
    pattern = r"(\n|^)[a-zA-Z0-9]+[).:]\s*(.*?)(?=[\n\r]|$)"
    matches = re.findall(pattern, story)
    return [i[1] for i in matches if i[1]]
# langchain llama
# chain1,chain2 = lang_chains()

# # prompts and generate image and video with next scene
# image_prompt,story = LLM_chat("A hungry Knight enters the realm of dragons",chain1,chain2)
# image_prompt = extract_prompt(image_prompt)
# image_data = text_to_image(api_key, image_prompt,debug=True)
# run_typing_effect(story)
# video_data = image_to_video(api_key, image_data,debug=True)

# image_prompt,story = LLM_chat("Try to find some shade and rest for a while before continuing on.",chain1,chain2)
# image_data = text_to_image(api_key, extract_prompt(image_prompt),debug=True)
# run_typing_effect(story)
# video_data = image_to_video(api_key, image_data,debug=True)

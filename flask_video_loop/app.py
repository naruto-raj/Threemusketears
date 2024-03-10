from flask import Flask, render_template, request
import sys, os
sys.path.append(os.getcwd())
from llm_video_gen import *
app = Flask(__name__)
chain1,chain2 = lang_chains()

def story_gen(text_prompt, chain1, chain2):
    image_prompt, story = LLM_chat(text_prompt,chain1,chain2)
    print(story)
    image_prompt = extract_prompt(image_prompt)
    image_data = text_to_image(api_key, image_prompt,debug=True)
    # run_typing_effect(story)
    video_data = image_to_video(api_key, image_data,debug=True)
    base64_video_data = base64.b64encode(video_data).decode('utf-8')
    return base64_video_data

@app.route('/')
def index():
    # Initially, set the default video URL
    video_url = 'sample_video.mp4'
    return render_template('index.html', video_url=video_url)

@app.route('/submit', methods=['POST'])
def submit():
    # if request.method == 'POST':
    #     text_prompt = request.form['text_prompt']
    #     print("User input:", text_prompt)
    #     # Do whatever you want with the input data here
    #     return 'Input received: ' + text_prompt  # Example response
    if request.method == 'POST':
        text_prompt = request.form['text_prompt']
        print("User input:", text_prompt)
        # prompts and generate image and video with next scene
        #"A hungry Knight enters the realm of dragons"
        base64_video_data = story_gen(text_prompt, chain1, chain2)
        print("Video generated")
        # Based on the user input, choose a different video URL
        # video_url = choose_video_url(text_prompt)  # You need to implement this function
        # print(video_url)
        return render_template('index.html', base64_video_data=base64_video_data)

# def choose_video_url(text_prompt):
#     # Implement your logic here to choose a video URL based on the user input
#     # This function should return the URL of the chosen video
#     # Example logic:
#     return 'sample_video1.mp4'

if __name__ == '__main__':
    app.run(debug=True)
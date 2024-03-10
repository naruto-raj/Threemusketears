from flask import Flask, render_template, request

app = Flask(__name__)

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
        # Based on the user input, choose a different video URL
        video_url = choose_video_url(text_prompt)  # You need to implement this function
        print(video_url)
        return render_template('index.html', video_url=video_url)

def choose_video_url(text_prompt):
    # Implement your logic here to choose a video URL based on the user input
    # This function should return the URL of the chosen video
    # Example logic:
    return 'sample_video1.mp4'

if __name__ == '__main__':
    app.run(debug=True)

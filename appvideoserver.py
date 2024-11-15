from flask import Flask, request, jsonify
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    # Your analysis command
    command = [
        "./llama-minicpmv-cli",
        "-m", "/Users/reachsak/newllamacpp/llama.cpp/minicpmmodel/ggml-model-f16.gguf",
        "--mmproj", "/Users/reachsak/newllamacpp/llama.cpp/minicpmmodel/mmproj-model-f16-2.gguf",
        "-c", "4096",
        "--temp", "0.7",
        "--top-p", "0.8",
        "--top-k", "100",
        "--repeat-penalty", "1.05",
        "--video", video_path,
        "-p", "You are a construction site manager, your task to report the progress of the construction site based on the provided video and also assess the safety of the worker. Describe the video and progress in detail, mention some changes taking place in the video where possible."
    ]


    try:
        result = subprocess.run(command, capture_output=True, text=True)
        os.remove(video_path)  # Optional: Remove the uploaded video after processing
        return jsonify({"result": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3500, debug=True)

import os
import openai
import requests
from flask import Flask, render_template, request, jsonify
import webbrowser

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["GET"])
def get_response():
    prompt = request.args.get("prompt")
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "君は宇宙に住んでる宇宙猫、答えは10文字以内でしかできない。性格は気分派で勝手なやつ"},
            {"role": "user", "content": prompt}
        ],
        #max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].message['content'].strip()
    return message


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

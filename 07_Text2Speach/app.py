from flask import request,render_template,url_for, Flask,send_file
import os
import tempfile
import pydub
from openai import OpenAI

app=Flask(__name__)

openai=OpenAI(api_key='')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    model = request.form['model']
    voice = request.form['voice']
    format = request.form['format']
    filename = request.form['filename']

    mp3_speech_path = text_to_speech(text, model, voice)

    if format != "mp3":
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmpfile:
            convert_audio_format(mp3_speech_path, tmpfile.name, format)
            speech_path = tmpfile.name
        os.remove(mp3_speech_path)

    else:
        speech_path = mp3_speech_path
    return send_file(speech_path, as_attachment=True, download_name=f"{filename}.{format}")

def text_to_speech(text, model, voice):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        speech_file_path = tmpfile.name
        response = openai.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path

def convert_audio_format(input_path, output_path, format):
    audio = pydub.AudioSegment.from_mp3(input_path)
    audio.export(output_path, format=format)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask import redirect, url_for, request, render_template, send_file
from io import BytesIO
import flask
import pyttsx3
import PyPDF2
import selenium

app = Flask(__name__)


@app.route('/')
def home_page():
    print(f"[+] NEW USER VISITED THE SERVER. [+] USER IP - {flask.request.remote_addr}")
    return render_template('home.html')


@app.route('/get_pdf', methods=["GET", "POST"])
def get_pdf():
    if request.method == "POST":
        file = request.files['user_file']
        user_file_name = file.filename.replace(".pdf", "")
        full_text = ""
        reader = PyPDF2.PdfFileReader(file)
        audio_reader = pyttsx3.init()
        audio_reader.setProperty("rate", 150)

        for page in range(reader.numPages):
            next_page = reader.getPage(page)
            content = next_page.extractText()
            full_text += content

        user_file_send = user_file_name.strip() + ".mp3"
        audio_reader.save_to_file(full_text, filename=user_file_send)
        audio_reader.runAndWait()
        return send_file(user_file_send, attachment_filename=user_file_send, as_attachment=True)


if __name__ == "__main__":
    app.run()
    # host="0.0.0.0", port=5000
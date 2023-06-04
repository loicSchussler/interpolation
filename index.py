from flask import Flask, render_template, request, send_file,  send_from_directory
import os
from imageScanner.main import process_image
import random

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello World!"


# there is only one value in the request (filename : string)
@app.post("/process")
def process():
    filename = request.form['filename']

    print("filename: ", filename)
    absolute_path = os.path.abspath(filename)
    print("absolute_path: ", absolute_path)
    currentDirectory = os.getcwd()
    savePath = currentDirectory + 'processed.xml'
    process_image(absolute_path, savePath)
    
    return send_file(savePath, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():    # get file from request formData
    file = request.files['file_upload']
    print("file: ", file)
    filename = file.filename
    # save file to process_filename
    with open(os.path.join(filename), 'wb') as f:
        f.write(file.read())


    return "success"

if __name__ == '__main__':
    app.run(debug=True)
    

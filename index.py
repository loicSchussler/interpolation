from flask import Flask, render_template, request, send_file
import os
from imageScanner.main import process_image

app = Flask(__name__)

@app.route('/')
def index():
    #add style.css to index.html
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():    # get file from request formData
    file = request.files['file_upload']
    print("file: ", file)
    filename = file.filename
    # save file to process_filename
    with open(os.path.join(filename), 'wb') as f:
        f.write(file.read())

    absolute_path = os.path.abspath(filename)
    print("absolute_path: ", absolute_path)
    currentDirectory = os.getcwd()
    savePath = currentDirectory + 'processed.xml'
    process_image(absolute_path, savePath)

    return send_file(savePath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

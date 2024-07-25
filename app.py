from flask import Flask, request, send_from_directory, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp directory in serverless environments
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MarcGenie</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to MarcGenie!</h1>
            <form id="uploadForm" enctype="multipart/form-data">
                <label for="fileInput">Choose MARC file:</label>
                <input type="file" id="fileInput" name="marcFile" accept=".mrk,.mrc">
                <br><br>
                <label for="outputName">Output File Name:</label>
                <input type="text" id="outputName" name="outputName" required>
                <br><br>
                <button type="submit" class="button">Process File</button>
            </form>
            <p id="output"></p>
        </div>

        <script>
            document.getElementById('uploadForm').addEventListener('submit', function(event) {
                event.preventDefault();

                var formData = new FormData();
                formData.append('marcFile', document.getElementById('fileInput').files[0]);
                formData.append('outputName', document.getElementById('outputName').value);

                fetch('https://your-backend-endpoint-url/auto', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.text())
                .then(data => {
                    document.getElementById('output').innerText = data;
                })
                .catch(error => {
                    document.getElementById('output').innerText = 'Error: ' + error;
                });
            });
        </script>
    </body>
    </html>
    '''

# <!doctype html>
#     <title>Upload File</title>
#     <h1>Upload File</h1>
#     <form method=post enctype=multipart/form-data action="/upload">
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        download_link = url_for('download_file', filename=file.filename, _external=True)
        return f'File uploaded successfully. Download link: <a href="{download_link}">{download_link}</a>'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()


# from flask import Flask, request, send_from_directory
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp directory in serverless environments
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# def index():
#     return '''
#     <!doctype html>
#     <title>Upload File</title>
#     <h1>Upload File</h1>
#     <form method=post enctype=multipart/form-data action="/upload">
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     <h1>Download File</h1>
#     <form method=get action="/download">
#       <input type=text name=filename>
#       <input type=submit value=Download>
#     </form>
#     '''

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part'
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file'
#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         return 'File uploaded successfully'

# @app.route('/download', methods=['GET'])
# def download_file():
#     filename = request.args.get('filename')
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == '__main__':
#     app.run()

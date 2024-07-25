from flask import Flask, request, send_from_directory, url_for, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp directory in serverless environments
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'marcFile' not in request.files or 'outputName' not in request.form:
        return 'No file part or output name'
    file = request.files['marcFile']
    output_name = request.form['outputName']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_ext = os.path.splitext(file.filename)[1]
        output_filename = output_name + file_ext
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        file.save(filepath)
        download_link = url_for('download_file', filename=output_filename, _external=True)
        return f'File uploaded successfully. Download link: <a href="{download_link}">{download_link}</a>'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()



# //////////////////////////



# from flask import Flask, request, send_from_directory, url_for
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp directory in serverless environments
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# def index():
#     return '''
#     <!doctype html>
#         <title>Upload File</title>
#         <h1>Upload File</h1>
#         <form method=post enctype=multipart/form-data action="/upload">
#         <input type=file name=file>
#         <input type=submit value=Upload>
#         </form>
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
#         download_link = url_for('download_file', filename=file.filename, _external=True)
#         return f'File uploaded successfully. Download link: <a href="{download_link}">{download_link}</a>'

# @app.route('/download/<filename>', methods=['GET'])
# def download_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == '__main__':
#     app.run()







# ///////////////////////
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

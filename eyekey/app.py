from flask import Flask, jsonify, request, render_template, send_file
import os
import base64
import MLDL_model

UPLOAD_FOLDER = './files' # 파일 저장할 경로
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','mp3']) # 허용할 파일 확장자 모음
 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
    return render_template('13_upload.html') # 테스트용 폼 (multipart/form-data)

@app.route('/uploader', methods=['GET','POST'])
def uploader_file():
    if request.method == 'POST':
        img = request.files['file1']
        img_filename = img.filename
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename)) 
        img_path = UPLOAD_FOLDER+'/'+img_filename

        record = request.files['file2']
        record_filename = record.filename
        record.save(os.path.join(app.config['UPLOAD_FOLDER'], record_filename)) 
        record_path = UPLOAD_FOLDER+'/'+record_filename

        return send_file(MLDL_model.run_model(img_path, record_path))
        
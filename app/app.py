from flask import Flask, render_template, request
import os 
from deeplearning import OCR, object_detection
from yolo import yolo_predictions
# webserver gateway interface
app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH,filename)
        upload_file.save(path_save)
        # print(upload_file)
        # image = yolo_predictions(path_save,filename)
        liscense_text = yolo_predictions(path_save, filename)

        return render_template('index.html',upload=True,upload_image=filename,text=liscense_text)

    return render_template('index.html',upload=False)

@app.route('/signin',methods=['POST','GET'])
def signin():
    return render_template('signin.html')

@app.route('/register',methods=['POST','GET'])
def register():
    return render_template('register.html')


if __name__ =="__main__":
    app.run(debug=True)
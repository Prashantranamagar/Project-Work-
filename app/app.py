from flask import Flask, render_template, request
import os 
from deeplearning import OCR, object_detection
from yolo import yolo_predictions
from flask import Flask, render_template, request, session, redirect, url_for

from db import DB


# webserver gateway interface
app = Flask(__name__)
app.secret_key = 'secret_key'

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


db = DB()
db.create()

@app.route('/',methods=['POST','GET'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            upload_file = request.files['image_name']
            filename = upload_file.filename
            path_save = os.path.join(UPLOAD_PATH,filename)
            upload_file.save(path_save)
            # print(upload_file)
            # image = yolo_predictions(path_save,filename)
            image = yolo_predictions(path_save)
            
            # text = OCR(path_save,filename)
            text = 'abc'

            return render_template('index.html',upload=True,upload_image=filename,text=text)
        return render_template('index.html',upload=False)
    return render_template('signin.html',upload=False)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user_cred(username, password)
        if user:
            session['username'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error='Invalid login credentials.')
    else:
        return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        password = request.form['pas']
        print(password)
        user = db.get_user_cred(username)
        if user:
            return render_template('register.html', error='Username already taken.')
        else:
            db.insert(username, password)
            session['username'] = username
            return redirect(url_for('index'))
        
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ =="__main__":
    app.run(debug=True)
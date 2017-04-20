# encoding=utf8
import os, time
from flask import Flask, request, redirect, url_for, Response, abort
from wand.image import Image
from werkzeug import secure_filename

UPLOAD_FOLDER = './uploads/'
CONVERTED_FOLDER = './converted/'
ALLOWED_EXTENSIONS = set(['mvg', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/c/<image_name>', methods=['GET'])
def get_image(image_name=None):
    if image_name[-3:] != "jpg":
        return abort(404)
    image_file = os.path.join(app.config['CONVERTED_FOLDER'] + image_name)
    try:
        with open(image_file) as f:
            return Response(f.read(), status=200, mimetype='image/jpg')
    except Exception:
        return abort(404)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with Image(filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)) as img:
                img.format = 'jpeg'
                fname = str(time.time())
                img.save(filename=os.path.join(app.config['CONVERTED_FOLDER'], fname + '.jpg'))
            return "/c/" + fname + '.jpg'

    return '''
    <!doctype html>
    <title>CVE-2016–3714 - ImageMagick</title>
    <h1>Upload Image (mvg,jpg,jpeg,gif)</h1> Convert images
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload></p>
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

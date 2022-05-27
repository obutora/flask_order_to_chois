import os
import shutil
from flask import Flask, redirect, send_file, request, render_template
import zipfile

from logic import foo
from logic import order_to_chois


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/html/<name>')
def html(name):
    return render_template('hello.html', name=name)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            shutil.rmtree('upload')
            shutil.rmtree('output')

        except:
            print('no upload/output folder')

        os.mkdir('upload/')
        os.mkdir('output/')

        try:
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']

            file1.save(os.path.join('./upload/', file1.filename))
            file2.save(os.path.join('./upload/', file2.filename))
            file3.save(os.path.join('./upload/', file3.filename))

            order_to_chois.order_to_chois(
                os.path.join('./upload/', file1.filename),
                os.path.join('./upload/', file2.filename),
                os.path.join('./upload/', file3.filename)
            )

            with zipfile.ZipFile('./output/result.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                zf.write('./output/check.csv')
                zf.write('./output/detail.csv')
                zf.write('./output/order.csv')

            return send_file(
                './output/result.zip',
                as_attachment=True
            )
        except:
            return 'ファイルの送信に失敗しました'
    else:
        return redirect('/')


@app.route('/func')
def func():
    foo.bar()
    return 'func'

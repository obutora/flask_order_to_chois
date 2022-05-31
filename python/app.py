# coding: UTF-8

import os
import shutil
from flask import Flask, redirect, send_file, request, render_template
import zipfile

from logic import order_to_chois

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/download')
def download():
    return send_file(
        './output/result.zip',
        as_attachment=True
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        try:
            shutil.rmtree('upload/')
            shutil.rmtree('output/')

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
                zf.write('./output/check.csv',
                         arcname='【要確認】直近で発注歴がないJAN、発注する場合は手動でお願いします.csv')
                zf.write('./output/detail.csv',
                         arcname='【必要に応じて確認】発注予定リスト.csv')
                zf.write('./output/order.csv', arcname='【CHOIS用】一括発注用ファイル.csv')

            # return send_file(
            #     './output/result.zip',
            #     as_attachment=True
            # )
            return render_template('download.html')

        except:
            return render_template('error.html')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

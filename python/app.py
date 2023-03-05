# coding: UTF-8

import os
import shutil
from flask import Flask, jsonify, redirect, request_finished, send_file, request, render_template
import zipfile
import json

from logic import order_to_chois
from logic.order import Order

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/edit')
def edit():

    dataList = [
        {
            "医薬品名": "アミティーザカプセル２４μｇ",
            "2021-12": 341.0,
            "2022-01": 231.0,
            "2022-02": 495.0,
            "2022-03": 373.0,
            "2022-04": 296.0,
            "平均出庫量": 347.2,
            "在庫数量": 144.0,
            "JANコード": 4987888172097.0,
            "仕入単価": 9818.0,
            "包装単位": 100.0,
            "発注数": 4.0,
        },
        {
            "医薬品名": "アミユー配合顆粒",
            "2021-12": 595.0,
            "2022-01": 557.0,
            "2022-02": 432.0,
            "2022-03": 742.0,
            "2022-04": 354.0,
            "平均出庫量": 536.0,
            "在庫数量": 588.0,
            "JANコード": 4987476165203.0,
            "仕入単価": 12006.0,
            "包装単位": 210.0,
            "発注数": 1.0,
        },
        {
            "医薬品名": "アデホスコーワ顆粒１０％",
            "2021-12": 411.0,
            "2022-01": 908.0,
            "2022-02": 452.0,
            "2022-03": 413.0,
            "2022-04": 861.0,
            "平均出庫量": 609.0,
            "在庫数量": 652.0,
            "JANコード": 4987770528803.0,
            "仕入単価": 10848.0,
            "包装単位": 600.0,
            "発注数": 1.0,
        },
    ]

    return render_template('edit.html', data=dataList)


@app.route('/edit_continue')
def editContinue():
    return render_template('edit_continue.html')


@app.route('/download')
def download():
    return send_file(
        './output/result.zip',
        as_attachment=True
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    outputPath = './upload'

    if request.method == 'POST':
        try:
            os.mkdir(outputPath)
        except:
            print('make folder error')

        try:
            print(request.files)
            # file1 = request.form['file1']
            # print(file1)
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']

            file1.save(os.path.join('./upload/', file1.filename))
            file2.save(os.path.join('./upload/', file2.filename))
            file3.save(os.path.join('./upload/', file3.filename))

            json = order_to_chois.order_to_chois(
                os.path.join('./upload/', file1.filename),
                os.path.join('./upload/', file2.filename),
                os.path.join('./upload/', file3.filename)
            )

            try:
                os.remove(os.path.join('./upload/', file1.filename))
                os.remove(os.path.join('./upload/', file2.filename))
                os.remove(os.path.join('./upload/', file3.filename))
            except:
                print('no output folder')

            # データ転送速度がネックと考え
            # ブラウザでZIPしたDataを受け取って展開する方法を実装していたが、
            # かえってブラウザでZIP→サーバーで展開の処理に時間がかかり、遅くなったため削除した。
            # file1 = request.files['file1']
            # file2 = request.files['file2']
            # file3 = request.files['file3']

            # file1.save(os.path.join(outputPath, file1.filename))
            # file2.save(os.path.join(outputPath, file2.filename))
            # file3.save(os.path.join(outputPath, file3.filename))

            # print('save file complete')
            # print(f'${outputPath}1y.csv.zip')

            # with zipfile.ZipFile(f'{outputPath}/1y.csv.zip') as zf:
            #     zf.extractall(outputPath)
            # with zipfile.ZipFile(f'{outputPath}/5m.csv.zip') as zf:
            #     zf.extractall(outputPath)
            # with zipfile.ZipFile(f'{outputPath}/list.csv.zip') as zf:
            #     zf.extractall(outputPath)

            # print('unzip complete')

            # json = order_to_chois.order_to_chois(
            #     f'{outputPath}/1y.csv',
            #     f'{outputPath}/5m.csv',
            #     f'{outputPath}/list.csv'
            # )

            # print('order_to_chois complete')

            # try:
            #     shutil.rmtree(outputPath)
            # except:
            #     print('no output folder')

            # return jsonify(json)

            # return render_template('download.html')
            return render_template('edit.html', data=json)
            # # return redirect('/edit')

        except:
            print('upload error')
            return render_template('error.html')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

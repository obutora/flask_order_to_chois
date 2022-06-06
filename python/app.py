# coding: UTF-8

import os
import shutil
from flask import Flask, redirect, send_file, request, render_template
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
    # dataList = ['a','b','c']
    # dataList = [
    #     {'name' : 'name1', 'value': 1},
    #     {'name' : 'name2', 'value': 2},
    # ]

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


@app.route('/download')
def download():
    return send_file(
        './output/result.zip',
        as_attachment=True
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        # try:
        #     shutil.rmtree('upload/')
        #     shutil.rmtree('output/')

        # except:
        #     print('no upload/output folder')

        try:
            os.mkdir('upload/')
            os.mkdir('output/')
        except:
            print('make folder error')

        # # 安全係数
        # safeCoff = request.form.get('week')
        # return safeCoff

        try:
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
                shutil.rmtree('upload/')
                shutil.rmtree('output/')

            except:
                print('no upload/output folder')

            # with zipfile.ZipFile('./output/result.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            #     zf.write('./output/check.csv',
            #              arcname='【要確認】直近で発注歴がないJAN、発注する場合は手動でお願いします.csv')
            #     zf.write('./output/detail.csv',
            #              arcname='【必要に応じて確認】発注予定リスト.csv')
            #     zf.write('./output/order.csv', arcname='【CHOIS用】一括発注用ファイル.csv')

            # return render_template('download.html')
            return render_template('edit.html', data=json)

        except:
            return render_template('error.html')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

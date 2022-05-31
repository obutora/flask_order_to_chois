# Order To CHOIS

CHOIS の一括発注用ファイルを作成するための Flask アプリケーションです。

## 必要なもの

- 過去 1 年分の入庫データ
- 5 ～ 6 ヵ月分の入庫データ
- 医薬品集データ

```
すべてのファイルはCHOIS上でダウンロード可能です。
Excelで開くと、JANコードのデータが破損してしまう為、
ダウンロードしたらそのままOrder To CHOIS に渡してください。
```

## ローカルのPython環境で動かす場合
### 必要なライブラリ
 - Flask
 - Pandas
 - Numpy

### 実行
`flask run --debugger --reload`　または `python -m flask run --debugger --reload`


## Docker コンテナ で動かす場合のTips
1. `docker stop flask`
2. `docker system prune -f`
3. `docker image build -t flask --no-cache .`
4. `docker run -dit -p 3000:5000 --name flask flask`

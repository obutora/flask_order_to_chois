
# coding: UTF-8

import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore', FutureWarning)


def order_to_chois(in1y, out6m, iyakusyu):
    # %%
    # inDF = pd.read_csv('csv/in_past1y.csv', encoding='cp932')
    inDF = pd.read_csv(in1y, encoding='cp932')
    inDF = inDF.loc[:, ['商品コード', '医薬品名', 'バラ換算数量', '箱数量']]
    inDF = inDF.sort_index(ascending=False)
    inDF = inDF.drop_duplicates()
    inDF['包装単位'] = inDF['バラ換算数量'] / inDF['箱数量']
    inDF.drop(['バラ換算数量', '箱数量'], axis='columns')

    inDF.rename(columns={'商品コード': 'JANコード'}, inplace=True)
    # orderDF.rename(columns={'医薬品名':'販売名称'}, inplace=True)
    # display(inDF.head())
    # display(len(inDF))

    # %%
    # 出庫量の読み込みと、必要な列のみ抽出
    # outDF = pd.read_csv(
    #     'csv/2021_12_2022_04_out_medicine.csv', encoding='cp932')
    outDF = pd.read_csv(out6m, encoding='cp932')
    outDF = outDF[outDF['規制'] != '麻薬']
    outDF = outDF[outDF['薬価単位'] != 'ＭＬ']
    outDF = outDF.loc[:, ['医薬品名', '伝票日付', 'バラ換算数量']]

    # 日付を年月のみにしたいのでDateTimeにしてからStringにformatしなおしている
    outDF['伝票日付'] = pd.to_datetime(outDF['伝票日付'])
    outDF['伝票日付'] = outDF['伝票日付'].apply(lambda x: x.strftime('%Y-%m'))
    # outDF.head()
    # print(len(outDF))

    # %%
    outPivot = pd.pivot_table(
        outDF, index='医薬品名', columns='伝票日付', values='バラ換算数量', aggfunc=np.sum).reset_index()
    outPivot = outPivot.fillna(0)

    std = outPivot.std(axis=1)
    avg = outPivot.mean(axis=1)

    outPivot['std'] = std
    outPivot['avg'] = avg
    # outPivot.head()

    # %%
    medDF = pd.read_csv(iyakusyu, encoding='cp932')
    medDF = medDF.loc[:, ['医薬品名', 'YJコード', 'JANコード', '在庫数量']]
    # medDF = medDF.loc[:, ['医薬品名','在庫数量']]

    # medDF.head()

    # %%
    joinDF = outPivot.merge(medDF, how='left', on='医薬品名')
    joinDF = joinDF.merge(inDF, how='left', on='医薬品名')
    # joinDF = outPivot.merge(inDF, how='left', on='医薬品名')

    joinDF.rename(columns={'JANコード_x': 'JANコード'}, inplace=True)
    joinDF.drop('JANコード_y', axis='columns', inplace=True)
    joinDF = joinDF.drop_duplicates(subset=['医薬品名'])

    needCheckDF = joinDF[joinDF['包装単位'].isnull()]
    needCheckDF.to_csv(
        'output/check.csv', encoding='cp932')

    # Nullになっている行を表示しておく
    # print('JANコードがNaNのもの')
    # display(len(joinDF[joinDF['JANコード'].isnull()]))
    # print('包装単位がNaNのもの')
    # display(len(needCheckDF))

    # その後NaNは処理
    joinDF = joinDF.dropna()
    # display(joinDF.head())
    # print(len(joinDF))

    # %%
    # 2SE + AVG - 在庫数量
    # SE = std / sqrt(n)
    # sqrt(5) = 2.236, sqrt(6)=2.449
    # 2SE ≒ 2 * std / sqrt(n) ≒ std
    joinDF['発注量'] = joinDF['std'] + joinDF['avg'] - joinDF['在庫数量']

    # 出庫量が0以下になるものは除外しておく
    joinDF = joinDF[joinDF['発注量'] > 0]

    # 四捨五入して発注数を決めている
    joinDF['発注数'] = (joinDF['発注量'] / joinDF['包装単位']).round()
    joinDF = joinDF[joinDF['発注数'] > 0]
    # display(joinDF.head())

    joinDF.to_csv('output/detail.csv', encoding='cp932')

    # %%
    orderDF = joinDF.loc[:, ['JANコード', '発注数', '医薬品名']]
    orderDF.rename(columns={'医薬品名': '販売名称'}, inplace=True)
    orderDF['規格'] = 0
    orderDF['総入数／単位'] = 0
    orderDF['MC送信卸コード'] = 0

    orderDF['JANコード'] = orderDF['JANコード'].astype(str).str[:-2]
    orderDF['発注数'] = orderDF['発注数'].astype(str).str[:-2]

    # orderDF.head()

    # %%
    orderDF.to_csv('output/order.csv', encoding='cp932', index=False)

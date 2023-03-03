
# coding: UTF-8

import pandas as pd
import numpy as np
import re


def order_to_chois(in1y, out6m, iyakusyu):
    print('start order to chois')
    print('in1y:', in1y)
    # %%
    inUseCols = ['商品コード', '医薬品名', 'バラ換算数量', '箱数量', '仕入単価']
    inDF = pd.read_csv(in1y, usecols=inUseCols)

    print('read in1y.csv complete')

    inDF = inDF.sort_index(ascending=False)
    inDF = inDF.drop_duplicates()
    inDF['包装単位'] = inDF['バラ換算数量'] / inDF['箱数量']
    inDF.drop(['バラ換算数量', '箱数量'], axis='columns')

    inDF.rename(columns={'商品コード': 'JANコード'}, inplace=True)
    # 逆順にする。仕入単価は毎回違うので最新の金額を反映するため
    inDF[inDF.columns[::-1]]

    # %%
    # 出庫量の読み込みと、必要な列のみ抽出
    # outDF = pd.read_csv(
    #     'csv/2021_12_2022_04_out_medicine.csv', encoding='cp932')
    outUseCols = ['医薬品名', '伝票日付', 'バラ換算数量', '規制', '薬価単位']
    outDF = pd.read_csv(out6m, usecols=outUseCols, dtype={
        '医薬品名': str,
        '伝票日付': str,
        'バラ換算数量': float,
        '規制': 'category',
        '薬価単位': 'category'}
    )

    print('read out5m.csv complete')

    outDF = outDF[outDF['規制'] != '麻薬']
    outDF = outDF[outDF['薬価単位'] != 'ＭＬ']
    # outDF = outDF.loc[:, ['医薬品名', '伝票日付', 'バラ換算数量']]
    outDF.drop(['規制', '薬価単位'], axis='columns', inplace=True)

    # 日付を年月のみにしたいのでDateTimeにしてからStringにformatしなおしている
    # outDF['伝票日付'] = pd.to_datetime(outDF['伝票日付'])
    # outDF['伝票日付'] = outDF['伝票日付'].apply(lambda x: x.strftime('%Y-%m'))
    m = re.compile(r'\d{4}\/([1-9])\/(0?[1-9]|[12][0-9]|3[01])$')
    outDF['伝票日付'] = outDF['伝票日付'].apply(
        lambda x: x[:6] if m.match(x) else x[:7])

    # %%
    outPivot = pd.pivot_table(
        outDF, index='医薬品名', columns='伝票日付', values='バラ換算数量', aggfunc=np.sum).reset_index()
    outPivot = outPivot.fillna(0)

    std = outPivot.std(axis=1)
    avg = outPivot.mean(axis=1)

    outPivot['std'] = std
    outPivot['avg'] = avg

    print('try read list.csv')
    # outPivot.head()

    medUseCols = ['医薬品名', 'YJコード', 'JANコード', '在庫数量']
    medDF = pd.read_csv(iyakusyu, usecols=medUseCols, dtype={
        '医薬品名': str, 'YJコード': str, 'JANコード': str, '在庫数量': float
    })

    print('read list.csv complete')

    # %%
    joinDF = outPivot.merge(medDF, how='left', on='医薬品名')
    joinDF = joinDF.merge(inDF, how='left', on='医薬品名')
    # joinDF = outPivot.merge(inDF, how='left', on='医薬品名')

    joinDF.rename(columns={'JANコード_x': 'JANコード'}, inplace=True)
    joinDF.drop('JANコード_y', axis='columns', inplace=True)
    joinDF = joinDF.drop_duplicates(subset=['医薬品名'])

    print('joinDF drop duplicates')

    # その後NaNは処理
    joinDF = joinDF.dropna()
    # display(joinDF.head())
    # print(len(joinDF))

    # %%
    # 2SE + AVG - 在庫数量
    # SE = std / sqrt(n)
    # sqrt(5) = 2.236, sqrt(6)=2.449
    # 2SE ≒ 2 * std / sqrt(n) ≒ std
    joinDF['発注量'] = 2*joinDF['std'] + joinDF['avg'] - joinDF['在庫数量']

    # 出庫量が0以下になるものは除外しておく
    joinDF = joinDF[joinDF['発注量'] > 0]

    # 四捨五入して発注数を決めている
    joinDF['発注数'] = (joinDF['発注量'] / joinDF['包装単位']).round()
    joinDF = joinDF[joinDF['発注数'] > 0]
    # display(joinDF.head())
    joinDF.drop(columns=['std', 'YJコード', 'バラ換算数量', '箱数量', '発注量'], inplace=True)
    joinDF.rename(columns={'avg': '平均出庫量'}, inplace=True)

    print('joinDF complete')

    json = list(joinDF.to_dict(orient='index').values())

    return json

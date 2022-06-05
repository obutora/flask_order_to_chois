function getMonthNames(list) {
    return Object.keys(list).filter(
        (name) =>
            name != "医薬品名" &&
            name != "平均出庫量" &&
            name != "在庫数量" &&
            name != "JANコード" &&
            name != "仕入単価" &&
            name != "包装単位" &&
            name != "発注数"
    );
}

const bodyNames = ["平均出庫量", "在庫数量", "仕入単価", "包装単位"];

function downloadCSV(data) {
    // var blob = new Blob(["Hello, world!"], {
    //   type: "text/plain;charset=utf-8",
    // });
    // saveAs(blob, "hello world.txt");

    const header = ["JANコード", "発注数", "販売名称", "規格", "総入数／単位", "MC送信卸コード"].join(",")

    // console.log(name)

    const t = data.map(item => `${item["JANコード"]},${item["発注数"]},${item["医薬品名"]},0,0,0`).join("\n")
    console.log(t)


    // const csvFormat = (col) => `"${col}"`;

    // // // 数値に csvFormatを適応すると " " が入ってしまうので不要
    const csvData = [
        header,
        t,
        // ["列1", "列2", "列3"].map(csvFormat).join(","),
        // ["あいうえお", "かきくけこ", "さしすせそ"].map(csvFormat).join(","),
        // [1, 2, 3].join(","),
        // ["キズナアイ", "輝夜月", "虹河ラキ"].map(csvFormat).join(","),
    ].join("\n");

    const unicodeList = [];
    for (let i = 0; i < csvData.length; i += 1) {
        unicodeList.push(csvData.charCodeAt(i));
    }

    // 変換処理の実施
    const shiftJisCodeList = window.Encoding.convert(
        unicodeList,
        "sjis",
        "unicode"
    );
    const uInt8List = new Uint8Array(shiftJisCodeList);

    // csv書き込みの実装
    const writeData = new Blob([uInt8List], { type: "text/csv" });

    saveAs(writeData, `【一括発注用リスト】-${new Date().getTime()}.csv`);
}


function downloadJson(data) {
    const str = JSON.stringify(data)

    var blob = new Blob([str], {type : 'application/json'});
    saveAs(blob, "【一時保存】発注データ.json");
}


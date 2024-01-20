# GIF_downloader  
## 開発主旨  
[自治体標準オープンデータセット](https://www.digital.go.jp/resources/open_data/municipal-standard-data-set-test)をダウンロードして、不足しているデータがあれば自動補完してくれることを目指します。  

## 仕様
　・Pythonを設置したフォルダ以下へのアクセス権および作業領域・データ保持が可能であること  

## 補完用データセット
### [市区町村名 住居表示](https://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi)　[address.py](address.py)  
**【利用シーン】**  
　・住居の座標が知りたい  
　・座標の住居が知りたい  
　・住居等の全国地方公共団体コード,町字idが知りたい  
　・全国地方公共団体コード,町字idの都道府県名,市区町村名,大字・町丁目名が知りたい  
現在は、北九州市に特化しています。  
最終的には、全国　OR　市区町村を選択できるよようになるといいな～～～  
1. 入力  
 市区町村名 住居表示－街区マスター位置参照拡張 データセット  
 "gaiku_url_list.txt　にURLを入力  
 市区町村名 住居表示－住居マスター位置参照拡張 データセット  
 "jyuukyo_url_list.txt"にURLを入力  
1. 出力  
 二つのデータセットを統合し、住居データとして出力  
 'merged_jyuukyo.csv' ファイルが出力されます  
 workフォルダには作業の状況が残ります
 ただし、work/extracted_filesフォルダ内は最後に作用した状況のみです  

### [国土数値情報 地域・施設](https://nlftp.mlit.go.jp/ksj/index.html)  []()
**【利用シーン】**  
　・公共施設の座標が知りたい  
　・公共施設の所在地が知りたい  
とりあえず、[町村役場等及び公的集会施設データ](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P05-v3_0.html)の全国をダウンロード一つのSHPファイルを構築まで完成
1. 変換ルール  
  [自治体標準オープンデータセット一覧の属性名称](https://www.digital.go.jp/resources/open_data/municipal-standard-data-set-test)　に統一
属性日本語名　「名称」に統一  　
・工業用地名,工業団地名または単独工場の名称,文字列型（CharacterString）,L05_002  
・発電施設名称,当該発電施設の名称,文字列型,P03_0002  
・施設名称,医療施設の名称,文字列型（CharacterString）,P04_002  
・公園名,都市公園の名称,文字列型（CharacterString）,P13_003  
・施設名称,廃棄物処理施設の名称,文字列型（CharacterString）,P15_001  
・施設名称,当該施設の名称,文字列型,P21B_003  
・施設名称,当該施設の名称,文字列型,P22*_002  
・施設名,地場産業関連施設の名称,文字列型,P24_005  
・連たんニュータウン名称,連たんニュータウンの名称,文字列型,P26_006  
・施設名称,施設名および施設の名称,文字列型（CharacterString）,P33_005  

1. 入力  
2. 出力  
# GIF_downloader  
## 開発主旨  
[自治体標準オープンデータセット](https://www.digital.go.jp/resources/open_data/municipal-standard-data-set-test)をダウンロードして、不足しているデータがあれば自動補完してくれることを目指します。  
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

### [国土数値情報 地域・施設](hhttps://nlftp.mlit.go.jp/ksj/index.html)  []()
**【利用シーン】**  
　・公共施設の座標が知りたい  
　・公共施設の所在地が知りたい  
1. 入力  
1. 出力  
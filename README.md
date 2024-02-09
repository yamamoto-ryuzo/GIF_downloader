# GIF_downloader  
## 開発主旨  
[自治体標準オープンデータセット](https://www.digital.go.jp/resources/open_data/municipal-standard-data-set-test)をダウンロードして、不足しているデータがあれば自動補完してくれることを目指します。    
ダウンロードしたデータは以下でPostgRESTとして公開予定をしています。（たまに試験起動してます）  
　https://github.com/yamamoto-ryuzo/PostgREST-installation-Japanese-memo/blob/main/%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95.md  

## 仕様
　・Pythonを設置したフォルダ以下へのアクセス権および作業領域・データ保持が可能であること  
　・EPSGコード不明はいったんEPSG：4612で処理　2024-01-26  

## 補完用データセット
### [国土数値情報 地域・施設](https://nlftp.mlit.go.jp/ksj/index.html)  []()
**【利用シーン】**  
　・公共施設の座標が知りたい  
　・公共施設の所在地が知りたい  

1. GIFコードへの変換ルール  
  [自治体標準オープンデータセット一覧の属性名称](https://www.digital.go.jp/resources/open_data/municipal-standard-data-set-test)　に統一  
  国土数値情報 地域・施設 の属性は　[シェープファイルの属性について](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P28.html)　による  
  【緯度・経度】  
・ジオメトリより属性に付加  
【GIFへの属性統一】  
・全国地方公共団体コード  
・名称  
・所在地_連結表記  
・所在地_都道府県  
・所在地_市区町村  

1. 今後の予定  
  ・GIFへの属性統一推進  
　　　取得したデータに不足しているGIFデータを補足する  
  ・任意の県データ取得への変更  
  ・EPSGコードの正しい設定  
  ・市区町村名 住居表示と統合
  ・全国地方公共団体コードから所在地_都道府県,所在地_市区町村がない場合にデータを補完   

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

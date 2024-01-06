##########################
######## 使いかた #########
##########################
### 入力
# 国土数値情報 地域・施設
# "input_list/digital_national_land_information_url_list.txt　にURLを入力
###　出力
# データセットを統合し出力
#'input_list/digital_national_land_informatio.csv' ファイルが出力されます
# workフォルダには作業の状況が残ります
# ただし、work/extracted_filesフォルダ内は最後に作用した状況のみです

##################################################################
######### モジュール(module)やパッケージ(package)の読み込み #########
##################################################################
#Webページやデータを取得
import requests
#ZIPの圧縮・解凍
import zipfile
#OS依存機能を利用
import os
#データ分析作業を支援するためのモジュール
import pandas as pd
import shutil

###########################################
######## 自作関数ファイルを読み込み #########
###########################################
import GIF_functions

#########################
######## メイン #########
########################
try:
    ### work　フォルダのクリーニング
    work_folder_path = 'work'
    if os.path.exists(work_folder_path):
        shutil.rmtree(work_folder_path)
    os.makedirs(work_folder_path)
    print(f"workフォルダのクリーニングが完了しました。")

    ### 住居表示ファイルの取得及び結合
    # address_download("住居表示ファイル名一覧ファイル名を指定",'結合住居表示ファイル名')
    #市区町村名 住居表示－街区マスター位置参照拡張 データセット
    GIF_functions.geo_download("input_list/digital_national_land_information_url_list.txt")
    print(f"結合データが作成されました。")

# エラー処理
except FileNotFoundError:
    print(f"ファイルが見つかりません。")

except Exception as e:
    print(f"エラーが発生しました: {e}")

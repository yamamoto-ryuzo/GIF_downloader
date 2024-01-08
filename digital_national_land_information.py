##########################
######## 使いかた #########
##########################
### 入力
# 国土数値情報 地域・施設
# "input_list/digital_national_land_information_url_list.txt　にURLを入力
###　出力
# データセットを統合し出力

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
    GIF_functions.clean_work_folder(work_folder_path)

    ### 住居表示ファイルの取得及び結合
    # address_download("住居表示ファイル名一覧ファイル名を指定",'結合住居表示ファイル名')
    #市区町村名 住居表示－街区マスター位置参照拡張 データセット
    GIF_functions.geo_download("input_list/digital_national_land_information_url_list.txt")
    folder_path = 'work/other_files_folder'
    ###座標系と統一
    target_epsg = 'EPSG:4326'
    GIF_functions.unify_crs_in_folder(folder_path, target_epsg)
    ### フォルダ内のGEOファイルを結合
    folder_path = 'work/other_files_folder'
    output_filename = 'result/digital_national_land_information.shp'
    GIF_functions.combine_shapefiles(folder_path, output_filename)
    #他の形式も作成
    input_path = 'result/digital_national_land_information.shp'
    output_path = 'result/digital_national_land_information.gpkg'
    GIF_functions.convert_format(input_path, output_path, input_format='ESRI Shapefile', output_format='GPKG')
    output_path = 'result/digital_national_land_information.csv'
    GIF_functions.convert_format(input_path, output_path, input_format='ESRI Shapefile', output_format='csv')
# エラー処理
except FileNotFoundError:
    print(f"ファイルが見つかりません。")

except Exception as e:
    print(f"エラーが発生しました: {e}")

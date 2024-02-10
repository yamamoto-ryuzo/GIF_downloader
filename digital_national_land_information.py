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
    work_folder_path = 'work'
    GIF_functions.clean_work_folder(work_folder_path)
    ### geoファイルの取得及び各県のデータを１ファイルに結合
    GIF_functions.geo_download("input_list/digital_national_land_information_url_list.txt")
    folder_path = 'work/other_files_folder'
    ###座標系と統一
    target_epsg = 'EPSG:4326'
    GIF_functions.unify_crs_in_folder(folder_path, target_epsg)

### フォルダ内のすべてのSHPにジオメトリの経度X、緯度Y座標属性値を追加
    GIF_functions.add_coordinates_to_shapefiles(folder_path)

    GIF_functions.convert_shp_to_gpkg(folder_path,folder_path)

    ### SHP属性名コードを日本語属性名に変更
    # 対象のSHPファイルが含まれるフォルダのパス
    # UTF-8　で作成のこと
    csv_file_path = 'input_list/国土数値情報コード名称変換.csv'
    GIF_functions.replace_attributes(folder_path,csv_file_path)

    ### フォルダ内のすべてのジオメトリをPOINTに変更
    gpkg_folder_path = 'work/other_files_folder'
    GIF_functions.convert_geometries_to_points(gpkg_folder_path)

    ### フォルダ内のGEOファイルを結合
    folder_path = 'work/other_files_folder'
    gpkg_file_path = 'result/digital_national_land_information.gpkg'
    GIF_functions.merge_geopackages(folder_path, gpkg_file_path)

    ###
    csv_file_path = 'input_list/AdminiBoundary_CD.csv'
    GIF_functions.find_final_city(gpkg_file_path, csv_file_path)

    ### 他の形式も作成
    csv_file_path = 'result/digital_national_land_information.csv'
    GIF_functions.convert_format(gpkg_file_path, csv_file_path, input_format='gpkg', output_format='csv')
# エラー処理
except FileNotFoundError:
    print(f"ファイルが見つかりません。")

except Exception as e:
    print(f"エラーが発生しました: {e}")


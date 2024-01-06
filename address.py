##########################
######## 使いかた #########
##########################
###　入力
#市区町村名 住居表示－街区マスター位置参照拡張 データセット
#"gaiku_url_list.txt　にURLを入力
#市区町村名 住居表示－住居マスター位置参照拡張 データセット
#"jyuukyo_url_list.txt"にURLを入力
###　出力
# 二つのデータセットを統合し、住居データとして出力
#'result/merged_jyuukyo.csv' ファイルが出力されます
#workフォルダには作業の状況が残ります
#ただし、work/extracted_filesフォルダ内は最後に作用した状況のみです

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
    GIF_functions.address_download("input_list/gaiku_url_list.txt",'work/combined_gaiku.csv')
    print(f"市区町村名 住居表示－街区マスターが作成されました。")
    #市区町村名 住居表示－住居マスター位置参照拡張 データセット
    GIF_functions.address_download("input_list/jyuukyo_url_list.txt",'work/combined_jyuukyo.csv')
    print(f"市区町村名 住居表示－住居マスターが作成されました。")

    ###　住居マスターに街区マスターを結合する
    # 1つ目のCSVファイルを読み込む
    df1 = pd.read_csv('work/combined_jyuukyo.csv')
    # 2つ目のCSVファイルを読み込む
    df2 = pd.read_csv('work/combined_gaiku.csv')
    # 属性をキーにして結合
    # 結合方式はleftのすべての行が保持
    # 同じ属性が重複する場合は街区データ側に接尾辞を追加
    merged_df = pd.merge(df1, df2, on='街区ユニークid', how='left', suffixes=('', '_街区'))
    # 結合結果を新しいCSVファイルとして保存
    merged_df.to_csv('result/merged_jyuukyo.csv', index=False)
    print(f"居住データベースが作成されました。")
    
# エラー処理
except FileNotFoundError:
    print(f"ファイルが見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
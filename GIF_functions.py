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

###########################
######### 関数定義 #########
###########################
### ファイルのダウンロード
def download_file(url, local_filename):
    # URLからファイルをダウンロードし、特定のローカルファイルパスに保存する
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

### 住居表示ファイルの取得及び結合
def address_download(file_name,combined_data_file):
    ### work/extracted_files　フォルダのクリーニング
    ### ※注意！　フォルダ内全ての一括処理があるため必ずその都度クリーニングを行うこと
    extracted_folder_path = 'work/extracted_files'
    if os.path.exists(extracted_folder_path):
        shutil.rmtree(extracted_folder_path)
    os.makedirs(extracted_folder_path)
    print(f"work/extracted_filesフォルダのクリーニングが完了しました。")
    ### 指定ファイル内のファイル一覧を読み込む
    # ファイルを読み込みモードで開く
    with open(file_name, "r") as file:
        # ファイルから行を1行ずつ読み込む
        file_list = file.readlines()
    # 各行の末尾の改行文字を削除
    file_list = [line.strip() for line in file_list]
    ### 読み込んだファイル一覧を順次処理
    for file_path in file_list:
        print(file_path)
        ### ファイルのダウンロード
        url = file_path
        local_filename = 'work/download.zip'
        download_file(url, local_filename)
        ### ダウンロードしてZIPファイルを読み込みモードで開き解凍
        with zipfile.ZipFile(local_filename, 'r') as my_zip:
            # ZIPファイル内のファイル一覧を表示
            file_list = my_zip.namelist()
            print("ZIPファイル内のファイル一覧:")
            for file_name in file_list:
                print(file_name)
            # ZIPファイル内の全てのファイルを解凍
            my_zip.extractall('work/extracted_files')
            ### 所定のフォルダ内のすべてのCSVファイルを結合
            ### 最初のファイルの属性行を取得しそれ以降のファイルの属性行は無視
            # CSVファイルが保存されているディレクトリを指定
            csv_directory = 'work/extracted_files'
            # 最初のCSVファイルから列名を取得
            first_file = os.listdir(csv_directory)[0]
            first_file_path = os.path.join(csv_directory, first_file)
            first_df = pd.read_csv(first_file_path)
            column_names = first_df.columns.tolist()
            # 結合するための空のDataFrameを作成
            combined_data = pd.DataFrame(columns=column_names)
            # 指定したディレクトリ内のCSVファイルを結合
            for filename in os.listdir(csv_directory):
                if filename.endswith(".csv"):
                    file_path = os.path.join(csv_directory, filename)
                if file_path == first_file_path:
                    # 最初のファイルはスキップして、列名を引き継ぐ
                    continue
                df = pd.read_csv(file_path)
                # 列名を引き継いで結合
                combined_data = pd.concat([combined_data, df], ignore_index=True)
                # 結合したデータを1つのCSVファイルに保存
                combined_data.to_csv(combined_data_file, index=False)
            print(f"CSVファイルの結合が完了しました。")
    ### CSVファイルを文字列として読み込む
    df = pd.read_csv(combined_data_file,dtype=str)
    # 結合したい文字列の属性を選択し、新しい文字列の属性を作成する
    df['街区ユニークid'] = df['全国地方公共団体コード'] + df['町字id'] + df['街区id']
    # 新しいCSVファイルに保存する
    df.to_csv(combined_data_file, index=False)
    print(f"街区ユニークidを追加しました。")
    return
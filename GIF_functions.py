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
#GISデータの処理
#pip install geopandas
import geopandas as gpd
import json

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

### 複数階層のZIPファイルを解凍
### ZIPファイルの中にZIPファイルがあるときは作業用フォルダに解凍
### ZIPファイル以外のファイルは特定のフォルダに解凍
# 使用例:
# zip_file_path = 'path/to/yourfile.zip'
# extract_to = 'path/to/destination_folder'
# work_folder = 'path/to/work_folder'
# other_files_folder = 'path/to/other_files_folder'
# extract_files(zip_file_path, extract_to, work_folder, other_files_folder)
def extract_files(zip_file_path, extract_to, work_folder, other_files_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # ZIPファイル内のすべてのファイルを取得
        file_list = zip_ref.namelist()
        for file in file_list:
            file_path = os.path.join(extract_to, file)
            
            # フォルダの場合はスキップ
            if file.endswith('/'):
                continue
            # ZIPファイル以外のファイルを特定のフォルダに解凍
            if not file.endswith('.zip'):
                zip_ref.extract(file, other_files_folder)
            else:
                # ZIPファイルの場合は作業用フォルダに解凍
                nested_folder = os.path.join(work_folder, os.path.splitext(file)[0])
                os.makedirs(nested_folder, exist_ok=True)
                zip_ref.extract(file, nested_folder)
                # 作業用フォルダに解凍されたZIPファイルを再帰的に処理
                extract_files(os.path.join(nested_folder, file), nested_folder, work_folder, other_files_folder)


### 仮想にあるフォルダ内のデータをすべて最上層に移動
# 移動したいフォルダのパスを指定します
# folder_path = '/path/to/your/folder'
# move_folders_data_to_top(folder_path)
def move_folders_data_to_top(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                shutil.move(file_path, folder_path)
            except shutil.Error as e:
                print(f"Failed to move {file_path}: {e}")

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

###geoファイルを結合
#指定フォルダのすべてのSHPファイルを結合して指定のファイル名にする関数
#結合候補のファイルを表示
# 使用例
#folder_path = "指定されたフォルダのパス"
#output_filename = "結合されたファイル名.shp"
#combine_shapefiles(folder_path, output_filename)
def combine_shapefiles(folder_path, output_filename):
    shp_files = [file for file in os.listdir(folder_path) if file.endswith(".shp")]
    
    if len(shp_files) == 0:
        print("指定されたフォルダにSHPファイルが見つかりませんでした。")
        return
    print("結合候補のファイル:")
    for file in shp_files:
        print(file)
    # 最初のファイルをベースにして読み込み
    # 文字コード明示
    gdf_list = [gpd.read_file(os.path.join(folder_path, shp_files[0]), encoding='shift_jis')]
    # 他のファイルをリストに追加
    for file in shp_files[1:]:
        data = gpd.read_file(os.path.join(folder_path, file))
        gdf_list.append(data)
    # リスト内のすべてのGeoDataFrameを結合
    combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True), crs=gdf_list[0].crs)
    # 結合したデータを保存
    # 文字コードを明示
    combined_gdf.to_file(output_filename, encoding='shift_jis')
    print(f"ファイル {output_filename} に結合されたデータを保存しました。")

### geoファイルの取得及び結合
def geo_download(file_name):
    try:
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
            # ZIPファイル内の全てのファイルを解凍
            zip_file_path = 'work/download.zip'
            extract_to = 'work/extracted_files'
            work_folder = 'work/work_folder'
            other_files_folder = 'work/other_files_folder'
            extract_files(zip_file_path, extract_to, work_folder, other_files_folder)
            print(f"ZIPファイルの解凍が完了しました。")
        ### 仮想にあるフォルダ内のデータをすべて最上層に移動
        # 移動したいフォルダのパスを指定します
        folder_path = 'work/other_files_folder'
        move_folders_data_to_top(folder_path)
        ### フォルダ内のGEOファイルを結合
        folder_path = 'work/other_files_folder'
        output_filename = "result/digital_national_land_information.shp"
        combine_shapefiles(folder_path, output_filename)

    # エラー処理
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        # エラーが発生した場合の処理をスキップする
        pass

    return
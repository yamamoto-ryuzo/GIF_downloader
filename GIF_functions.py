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
import fiona

###########################
######### 関数定義 #########
###########################

###フォルダのクリーニング
#work_folder_path = 'work'
#clean_work_folder(work_folder_path)
def clean_work_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    print(f"{folder_path}フォルダのクリーニングが完了しました。")

###ファイルの中にある??を01－47の連番にして新しいファイルを作成する
#input_filename = 'input.txt'  # 元のファイル名
#output_filename = 'output.txt'  # 出力先のファイル名
#process_file(input_filename, output_filename)
def process_file(input_file, output_file):
    # ファイルからデータを読み込む
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 条件を満たす行を増殖させて新しいリストに追加する
    new_lines = []
    for line in lines:
        # ここで条件を確認し、??があれば01～47の連番に増殖させる（条件に合わせて変更してください）
        if '??' in line:
            #とりあえず全国だと大きすぎたので40：福岡県へ修正
            for i in range(40, 41):
                new_line = line.replace('??', f'{i:02d}')  # ??を01～47の連番で置換
                new_lines.append(new_line)
        else:
            new_lines.append(line)
    # 新しいファイルに書き込む
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

### ファイルのダウンロード
def download_file(url, local_filename):
    try:
        # URLからファイルをダウンロードし、特定のローカルファイルパスに保存する
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except requests.exceptions.HTTPError as e:
        print(f"HTTPエラーが発生しました: {e}")
    except IOError as e:
        print(f"ファイル書き込みエラーが発生しました: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
    return None

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
def move_files_to_parent_folder(folder_path):
    # フォルダ内のすべてのファイルを取得
    #root: 現在走査しているディレクトリのパスです。
    #dirs: そのrootディレクトリ内のディレクトリ名のリストです。
    #files: そのrootディレクトリ内のファイル名のリストです。
    for root, dirs, files in os.walk(folder_path):
        # ファイルを親フォルダに移動
        for file in files:
            # ファイルのパスを取得
            file_path = os.path.join(root, file)
            try:
                if folder_path != os.path.dirname(file_path):
                    shutil.move(file_path, folder_path)
            except shutil.Error as e:
                print(f"移動に失敗しました {file_path}: {e}")

### 指定されたフォルダ内のすべてのShapefileの座標系を統一する関数。
# 使用例:
#folder_path = 'path/to/your/folder'
#target_epsg = 'EPSG:4326'
#unify_crs_in_folder(folder_path, target_epsg)
def unify_crs_in_folder(folder_path, target_epsg):
    non_crs_folder = os.path.join(folder_path, 'NON_CRS')
    os.makedirs(non_crs_folder, exist_ok=True)
    
    for file in os.listdir(folder_path):
        if file.endswith('.shp'):
            file_path = os.path.join(folder_path, file)
            # Shapefileを読み込む
            gdf = gpd.read_file(file_path, encoding='shift_jis')
            
            # 座標系が不明な場合の処理
            if gdf.crs is None:
                base_name, _ = os.path.splitext(file)
                # 関連ファイルをNON_CRDフォルダに移動
                related_files = [f"{base_name}.shp", f"{base_name}.shx", f"{base_name}.dbf", f"{base_name}.prj", f"{base_name}.cpg"]
                for related_file in related_files:
                    related_file_path = os.path.join(folder_path, related_file)
                    if os.path.exists(related_file_path):
                        shutil.move(related_file_path, os.path.join(non_crs_folder, related_file))
                        print(f"CRSが不明なファイル: {related_file} を NON_CRS フォルダに移動しました。")
                continue
            
            # 座標系を統一する
            gdf = gdf.to_crs(target_epsg)
            # ファイルを上書き保存する
            gdf.to_file(file_path, encoding='shift_jis')
    print(f"すべてのShapefileを一つの座標系に統一しました。")

### データ形式変換
#ESRI Shapefile: driver='ESRI Shapefile' (.shp)
#GeoPackage: driver='GPKG' (.gpkg)
#Keyhole Markup Language (KML): driver='KML' (.kml)
#GeoJSON: driver='GeoJSON' (.geojson)
#ただしCSVは以下で実行
#gdf.to_csv('output.csv')
# 使用例
#input_path = 'path/to/your/input_data.shp'
#output_path = 'path/to/your/output_data.gpkg'
#convert_format(input_path, output_path, input_format='ESRI Shapefile', output_format='GPKG')
def convert_format(input_path, output_path, input_format='ESRI Shapefile', output_format='GPKG'):
    # データを読み込む
    gdf = gpd.read_file(input_path)
    # 指定された出力フォーマットでファイルに保存する
    if output_format != 'csv':
        gdf.to_file(output_path, driver=output_format)
    else:
        gdf.to_csv(output_path)
    print(f"ファイルを変換しました：{output_path}")

###################################################################################

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

def merge_geopackages(input_folder, output_gpkg):
    # フォルダ内のすべての GeoPackage ファイルをリストアップ
    gpkg_files = [f for f in os.listdir(input_folder) if f.endswith('.gpkg')]

    # 最初の GeoPackage ファイルをベースとして読み込む
    merged_gdf = gpd.read_file(os.path.join(input_folder, gpkg_files[0]))

    # 他の GeoPackage ファイルを順次マージ
    for gpkg_file in gpkg_files[1:]:
        gdf_to_merge = gpd.read_file(os.path.join(input_folder, gpkg_file))
        merged_gdf = gpd.GeoDataFrame(pd.concat([merged_gdf, gdf_to_merge], ignore_index=True))

    # マージしたデータを新しい GeoPackage ファイルに保存
    merged_gdf.to_file(output_gpkg, driver="GPKG")



### geoファイルの取得及び各県のデータを１ファイルに結合
def geo_download(file_name):
    try:
        #読み込み専用ファイルへの変換
        #ファイルの中にある??を01－47の連番にして新しいファイルを作成する
        work_file_name = file_name + '.work'
        process_file(file_name, work_file_name)
        print(f"作業用ファイル {work_file_name} を作成しました。")
        ### 指定ファイル内のファイル一覧を読み込む
        # ファイルを読み込みモードで開く
        with open( work_file_name, "r", encoding='UTF-8') as file:
            # ファイルから行を1行ずつ読み込む
            file_list = file.readlines()
        # 各行の末尾の改行文字を削除
        file_list = [line.strip() for line in file_list]
        # 読み込んだファイル一覧を順次処理
        for line in file_list:
            line = line.strip()  # 各行の先頭および末尾の空白を削除
            if ',' in line:  # ',' がデリミタとして使われていると仮定
                file_path, file_title = line.split(',')
                file_path = file_path.strip()  # ファイル名から空白を削除
                file_title = file_title.strip()  # タイトルから空白を削除
                print(f"ファイルパス: {file_path}, タイトル: {file_title}")
            else:
                file_path = line
                print(f"ファイルパス: {file_path}")

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
        print(f"{folder_path}の下層にフォルダがある場合はすべて直下に移動します。")
        move_files_to_parent_folder(folder_path)

    # エラー処理
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        # エラーが発生した場合の処理をスキップする
        pass
    return


def replace_attributes(folder_path, csv_file_path):
    # フォルダ内のすべてのGPKGファイルに対して処理を行う
    for filename in os.listdir(folder_path):
        if filename.endswith(".gpkg"):
            # GPKGファイルを読み込む
            gpkg_path = os.path.join(folder_path, filename)
            gdf = gpd.read_file(gpkg_path)

            # CSVファイルを読み込む
            csv_data = pd.read_csv(csv_file_path)

            # 属性の置き換えを行う
            for index, row in csv_data.iterrows():
                shp_attribute_name = row['shp属性名']
                attribute_name = row['属性名']

                if shp_attribute_name in gdf.columns:
                    gdf[attribute_name] = gdf[shp_attribute_name]
                    gdf = gdf.drop(columns=[shp_attribute_name])

            # 置き換えたデータを新しいGPKGファイルとして保存
            new_gpkg_path = os.path.join(folder_path, filename)
            gdf.to_file(new_gpkg_path, driver='GPKG')
            print(f"{filename}の属性をコードから日本語に置き換えました。")


def convert_shp_to_gpkg(input_folder, output_folder):
    # SHPファイルが格納されている入力フォルダ
    shp_files = [f for f in os.listdir(input_folder) if f.endswith('.shp')]

    # GPKGファイルの出力フォルダ
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for shp_file in shp_files:
        shp_path = os.path.join(input_folder, shp_file)

        # .shpを.gpkgに置き換えてGPKGファイル名を作成
        gpkg_file = os.path.splitext(shp_file)[0] + '.gpkg'
        gpkg_path = os.path.join(output_folder, gpkg_file)

        # Geopandasを使用してSHPファイルを読み込む
        gdf = gpd.read_file(shp_path)

        # GeoPackageに書き込む
        gdf.to_file(gpkg_path, driver='GPKG')

        print(f"{shp_file} を {gpkg_file} に変換しました")
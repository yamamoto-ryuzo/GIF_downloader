#####################################
############## 環境設定 ##############
#####################################
#RustとCargoをインストール
#https://rustup.rs/
#1) Quick install via the Visual Studio Community installer
#   (free for individuals, academic uses, and open source).
#　[1]を選択
#   'cargo'等その他のインストール
#   1) Proceed with installation (default)
#　[1]を選択
#念のためPCは再起動
#DOS-コマンド　管理者権限
#pip install open-interpreter
#ローカルの Code Llamaを準備
# https://lmstudio.ai/
# 適当にインストール
#　lmstudio起動後
# 検索画面で　Llama2
#  likeの順で多かったのを選択
#  　　今回は[]
#     画面右側でダウンロード
# 画面左側で<->ボタンを押して
# 画面上側でダウンロードしたモデルを選択
# 画面左中ほどの Start Server　を教えてスタート
#DOS-コマンド　管理者権限
#interpreter --local


#######################################
############## python本体##############
#######################################
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  messages=[
    {"role": "system", "content": "Always answer in rhymes."},
    {"role": "user", "content": "Introduce yourself."}
  ],
  temperature=0.7,
)

# Swagger_Spec_Loader
## 機能
 - Open API Initiativeの策定するyml形式のSpec(2.0)の解析
 - エンドポイント一覧の提供
 - リクエストの`Intruder`,`Repeater`への展開
 - 任意の`header`,`authorization token`を追加可能
 - 指定したQueryとParameterの一括置換

## インストール
### 表記
- `[ タブ ]`
- `( ボタン )`
- `項目名` * 何も囲っていないものは項目名

### リポジトリのクローン
```sh
git clone https://git.pepabo.com/nori/Swagger_Spec_Loader.git
cd ./Swagger_Spec_Loader
```
### Jythonの設定
**Jythonの設定がまだな方はこちら**
1. Jythonのダウンロード

    [ここから](http://www.jython.org/downloads.html)最新版のJython - Standalone Jarをダウンロードします。
1. requirements.txtから必要なパッケージのインストール
```sh
pip install -r requieremnts.txt
```
1. Burp Suiteでの環境設定

    1. 起動後 `[Extender] > [Option]`のタブへ移動
    1. Python Environmentで先ほどダウンロードしたJyhtonとパッケージを設定

        - Location of Jython standalone JAR Fileの`(select file)`からStandalone Jarを選択
        - python のsite-packagesまでのpathを指定

### Extentionの追加
1. Extentionの追加
 - `(Add) > Extention Detail > (Python ▼)`
 - `(select file)`から先ほどダウンロードしたリポジトリ内のmain.pyを選択
 - `(Next)`で追加完了

## 使い方
### spec yamlのロードとエンドポイントへの反映
1. `[Home] > Select Yaml > (Swagger Yaml File)`
1. クリック後利用したいspecを選択
1. `Load Data > (Load Data)`でエンドポイントへ反映

### 各種値の設定
#### パラメータ/クエリの置き換え
1. `Set_Param > (Add)`から置き換えたい項目名と置き換える値を入力
1. `(Load Data)`で置き換え後のエンドポイントが追加

#### 任意のヘッダーの追加
1. `Set_Header > (Add)`から追加したいヘッダーと値を入力
1. `(Load Data)`で置き換え後のエンドポイントが追加

#### 任意の認証トークンを追加
1. `Set_Token > (Add)`から追加したいTokenのタイプと値を入力
1. `(Load Data)`で置き換え後のエンドポイントが追加

### エンドポイント一覧からの操作
エンドポイントからは`Intruder`,`Repeater`への展開が可能

### 設定したパラメータが反映されるタイミングについて
反映されるタイミングは`(Load Data)`時なので一度エンドポイントに出力されたものには変更が及ばない

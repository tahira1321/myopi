# ====================
# Import
# ====================
# Standard Library: OS環境変数の読み込み
import os

# Third-party Library: MySQL接続用ドライバ
from flask import current_app # __init__.py からapp.configの値を取得するためのLibrary
from flask import g
import pymysql
import pymysql.cursors
import pymysql.err

# --------------------
# Database Connection Settings
# --------------------
def get_connection():
    return pymysql.connect(
            # __init__.py のapp,config の値を取得
            host = current_app.config['DB_HOST'],
            user = current_app.config['DB_USER'],
            password = current_app.config['DB_PASSWORD'],
            database = current_app.config['DB_NAME'],
            cursorclass = pymysql.cursors.DictCursor
            )

# --------------------
# Save data
# --------------------
## --- Create & Save ---
def save_memo(title, content, question_date):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO memos (title, content, question_date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (title, content, question_date,))
            connection.commit() # commit: 保存・変更・削除の確定
            return True
    except pymysql.err.MySQLError as e:
        print(f"データベースエラー: {e}")
        connection.rollback() # 失敗した場合は処理を巻き戻す
        return False # 呼び出し元に「失敗」を伝える
    finally:
        connection.close()

## --- Read ---
def get_all_memos():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM memos WHERE status != 'deleted' ORDER BY question_date DESC")
            memos = cursor.fetchall() # fetchall: 取得したデータを手元に持ってくる
            return memos
    finally:
        connection.close()

def get_memo_by_id(memo_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM memos WHERE id = %s"
            cursor.execute(sql, (memo_id,))
            memo = cursor.fetchone()
            return memo
    finally:
        connection.close()

def update_memo(title, content, question_date, memo_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE memos SET title = %s, content = %s, question_date = %s WHERE id = %s"
            cursor.execute(sql, (title, content, question_date, memo_id,) )
            connection.commit()
            return True
    finally:
        connection.close()

# Delete memo
def delete_memo(memo_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE memos SET STATUS = 'deleted' WHERE id = %s"
            cursor.execute(sql, (memo_id,))
            connection.commit()
            return True
    finally:
        connection.close()



# ====================
# Execution Flow & Roadmap (Guide for Future Self)
# ====================
"""
[ このファイルの役割 ]
1. データベース（MySQL）との直接的な「対話」を担当するデータ層。
2. SQL文を発行し、データの保存（INSERT）や取得（SELECT）を行う。

[ 情報の流れ（データフロー）の覚書 ]
- 従来: models.py ──(直接)──> .env / OS環境変数
- 今回: models.py ──(current_app経由)──> __init__.py ──(一括管理)──> .env / OS環境変数

[ 理由とメリット ]
1. 設定の一元管理: 接続先を変えたい時は __init__.py（または .env）を一箇所直すだけで済む。
2. 堅牢性: 各ファイルでバラバラに環境変数を読み込むと、一箇所だけ読み込みに失敗するなどの
   ミスが起きるが、current_app 経由なら「アプリが持っている正しい値」を常に参照できる。

[ 開発時のTips ]
- current_app は Flask がリクエストを処理している間（アプリが動いている間）だけ使える。
- INSERT/UPDATE/DELETE の後は必ず connection.commit() を呼んで変更を確定させる。

[ DictCursor を使う理由とメリット ]
1. データの取り扱い：
   - 通常（設定なし）： 取得データは「タプル形式」になり、`memo[0]`, `memo[1]` のように
     「何番目のデータか」という番号でしか指定できない。
   - DictCursor（設定あり）： 取得データが「辞書（Dictionary）形式」になり、
     `memo['title']`, `memo['content']` のように、DBのカラム名で直接指定できる。

2. メンテナンス性：
   - もし将来、DBのテーブルに新しい列（カラム）が増えて順番が変わっても、
     名前で指定していればプログラムを書き直す必要がない（番号指定だとズレて壊れる）。
   - HTML（Jinja2）側で `{{ memo.title }}` と書くだけで中身が表示されるので、
     直感的でミスが減る。

[ SQL操作の深掘り備忘録 ]

1. 命令の使い分け（commit vs fetchall）
   - connection.commit(): 「保存・変更・削除」の確定。ハンコを押す作業。
     ※これがないと、プログラム上は成功してもDBには反映されない！
   - cursor.fetchall(): 「取得」したデータを手元に持ってくる作業。
     ※SELECT文の時だけ使用。見るだけなので commit は不要。

2. 記述のスタイル（sql = ... と分ける理由）
   - 長いSQLや、%s（変数）を使う場合は、先に `sql = "..."` と変数に分けると読みやすい。
   - 短いSQL（SELECT * など）は、execute() の中に直接書いてもOK。
   - どちらも「可読性（読みやすさ）」のための使い分け。

3. 安全なデータ受け渡し（%s の魔法）
   - title などの変数をSQLに直接入れず、必ず `%s` を使い execute の第2引数で渡す。
   - これにより「SQLインジェクション」という攻撃を防ぎ、記号（'や"）が含まれていても
     エラーにならず安全に保存できる。

[ 実務でよく使うカーソル操作・拡張編 ]

1. cursor.fetchone() : 「1件だけ」の精密な取得
   - 役割: 条件に一致する最初の1行だけを返す。
   - 場面: 「IDを指定した詳細表示」や「ログイン時のユーザー確認」など。
   - 利点: fetchall() のようにリストをループさせる必要がなく、直接データを扱える。

2. cursor.rowcount : 「影響を受けた行数」の確認
   - 役割: 直前の execute（UPDATEやDELETEなど）で、何行のデータが動いたかを数値で返す。
   - 場面: 「削除ボタンを押して、実際に1件消えたか？」をチェックしてユーザーに通知する時。
   - 利点: 画面上で「0件削除されました（失敗）」などの正確なフィードバックができる。

3. cursor.lastrowid : 「生まれたてのID」の特定
   - 役割: INSERT文で新しく発行された「自動採番（AUTO_INCREMENT）のID」を取得する。
   - 場面: メモを保存した直後に、そのメモ専用のURL（例: /memo/25）へリダイレクトさせたい時。
   - 利点: 保存した瞬間にそのデータの「背番号」がわかるため、次のアクションに繋げやすい。

[ return の判断基準 ]
- データを「取得」する関数（get_...）: 
  必ず return が必要。これがないと呼び出し側の Flask が「空っぽ（None）」を受け取ってエラーになる。
- データを「操作」する関数（save_..., delete_...）: 
  基本は不要。ただし、成功したかどうか（True/False）や、
  新しく発行された ID（lastrowid）を報告したい時は return を使う。

[ 丁寧なアプリ設計のための return 活用術 ]

1. 基本スタンス（フィードバックの原則）:
   - データを操作する関数（save/update/delete）でも、原則として `return True`（成功）や 
     `return False`（失敗）を返すように設計する。
   - 呼び出し側（main.py）で「保存できました！」という通知（Flashメッセージ等）を出すための判断材料にするため。

2. 例外（完全に内部で完結する場合）:
   - ログの記録や、一時的な計算用ファイルの削除など、ユーザーの目に触れない
     「裏方の作業」であれば、return なし（Noneを返す）でも問題ない。

3. ユーザー体験（UX）への影響:
   - return がある = 呼び出し側が「状況」を把握できる = ユーザーに「結果」を伝えられる。
   - 「無言で終わるアプリ」より「一言添えてくれるアプリ」の方が、ユーザーは安心して使い続けられる。

[ データベース接続の備忘録 ]
- get_connection(): 認証済みのカードキーを発行する関数。
- connection.commit(): 実施した処置を正式に記録（保存）する確定ボタン。
- connection.close(): 業務終了。鍵を返却して通信を切断する（忘れるとエラーの元）。
- 複数DB: 接続設定を増やせば、複数の病院（データベース）を跨いで活動も可能。
"""

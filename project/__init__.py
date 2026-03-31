# ====================
# Import
# ====================
# Standard Library:OS操作・システム関連モジュール
import os

# Third-party Library:フレームワーク本体・pipでインストールした拡張機能など
from flask import Flask, render_template
from dotenv import load_dotenv

# Read .env:アプリ起動前に環境変数を確定
load_dotenv()

# ====================
# Extensions Instance 
# ====================
### 以下は記載位置の例
### db = SQLAlchemy()
### login_manager = LoginManager()


# ====================
# Application Factory 
# ====================
def create_app():
    # --- Framework Instance Creation ---
    app = Flask(__name__)

    # --- Configuration ---
    ## Security
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    ## Database
    ### app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config.update(
            DB_HOST = os.environ.get('DB_HOST', '127.0.0.1'),
            DB_USER = os.environ.get('DB_USER', 'root'),
            DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root123'),
            DB_NAME = os.environ.get('DB_NAME', 'project_db')
            )

    ## Debug

    # --- Initialize Extensions:拡張機能とアプリの紐づけ ---
    ### db.init_app(app)
    ### login_manager.init_app(app)
    
    # --- Error Handling ---
    ## カスタムエラーページの登録
    register_error_handlers(app)

    # --- Global Request Hooks ---
    ## 全ルート共通の処理
    register_request_hooks(app)

    # --- Local Modules ---
    ## Blueprint import & registration
    from .main import main
    app.register_blueprint(main)

    ##Models import:DBテーブル定義の読込
    ### from . import models

    return app

# ====================
# Helper Functions 
# ====================
def register_error_handlers(app):
    # エラーハンドリングの具体的内容を記入
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    pass

def register_request_hooks(app):
    # リクエストのライフサイクルに合わせた処理を登録
    @app.teardown_appcontext
    def close_db_connection(exception):
        """
        リクエスト終了時に実行される処理
        models.pyなどで管理しているDB接続を安全に閉じるコードをここに記載
        例 from .models import get_db; get_db().close()
        """
        pass


# ====================
# Execution Flow & Roadmap (Guide for Future Self)
# ====================
"""
[ 実行順序とファイル間連携のロードマップ ]

1. 起動時 (Entry Point):
   - ターミナルで `flask run` または `python run.py` を実行。
   - Flaskはパッケージ（projectフォルダ）を見つけると、まずこの `__init__.py` を読み込む。

2. アプリ生成 (Application Factory):
   - `create_app()` が呼び出され、Flaskインスタンス (`app`) が誕生する。
   - `.env` から環境変数が読み込まれ、`app.config` に設定が格納される。

3. ルートの登録 (Blueprint):
   - `from .main import main` により `project/main.py` が参照される。
   - `main.py` 内で定義された @main.route...（URLと関数の紐付け）がアプリに登録される。

4. リクエスト時 (User Request):
   - ユーザーがブラウザでアクセスすると、`main.py` の対応する関数が実行される。
   - その関数内で `from . import models` を通じて `project/models.py` が呼び出される。
   - `models.py` が MySQL データベースへ接続し、データを取得して `main.py` へ返す。

5. 画面表示 (Response):
   - `main.py` が `render_template` を実行。
   - `templates/` フォルダ内の HTML ファイルが読み込まれ、ユーザーの画面に表示される。

[ 次に見るべきファイル ]
- 画面の「動き」や「ロジック」を追いたい場合： `project/main.py`
- データベースの「構造」や「接続」を追いたい場合： `project/models.py`
"""

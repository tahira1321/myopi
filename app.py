# ====================
# Import
# ====================
# Standerd Library
import os
# Import Application Factory from project Package
from project import create_app

# ====================
# Create App Instance
# ====================
app = create_app()

# ====================
# Run Server
# ====================
if __name__ == '__main__':
    # 環境変数からポート番号を取得
    port = int(os.environ.get("PORT", 5000))

    # server 起動設定
    app.run(host='0.0.0.0', port=port)

# ====================
# Execution Flow Note
# ====================
"""
[ このファイルの役割 ]
1. Flaskアプリの起動用エントリーポイント。
2. アプリ本体の設定は `project/__init__.py` (create_app) で完結させる。
3. SQLAlchemyを使わない場合、DB接続のクローズ処理などは `create_app` 内で
   @app.teardown_appcontext を使って共通化しておくと拡張性が高まる。

[ 開発時のTips ]
- 起動: `python app.py` または `flask run`
- 設定管理: .env ファイルに SECRET_KEY や DBパスを記述し、コードから分離する。
"""

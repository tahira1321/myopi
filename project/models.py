# ====================
# Import
# ====================
# Standard Library: OS環境変数の読み込み

# Third-party Library: MySQL接続用ドライバ
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

# --------------------
# Create Instance
# --------------------
db = SQLAlchemy()

# --------------------
# Define Class
# --------------------
class User(db.Model, UserMixin):
    # --- Specify Table ---
    __tablename__ = 'users'

    # --- Specify Column :カラム名 = db.Column(型, 設定) ---
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # --- Insert User ---
    # insert data
    def save(self):
        db.session.add(self)
        db.session.commit()

class Opinion(db.Model):
    __tablename__ = 'opinions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    question_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime,default=datetime.now)

    # 外部キー: usersテーブルとidの紐づけ
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # --- Create & Update ---
    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    # --- Read ---
    @classmethod
    def get_all_active(cls):
        """ 削除されていない主張を降順で全件取得 """
        return cls.query.filter(cls.status != 'deleted').order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, opinion_id):
        """ id指定で1件取得 """
        return cls.query.get(opinion_id)

    # --- Delete ---
    def delete(self):
        """ 論理削除：statusをdeleteにして保存 """
        self.status = 'delete'
        db.session.commit()
        return True

# ====================
# Execution Flow & Roadmap (Guide for Future Self)
# ====================
"""
[ 次にするべきこと ]
1. __init__.py で Flaskアプリとこの db インスタンスを紐付ける。
   (例: db.init_app(app))
2. app.config['SQLALCHEMY_DATABASE_URI'] に接続情報を設定する。
3. main.py 等の views で、Opinion.get_all_active() などを使ってデータを呼び出す。

[ メリット ]
- get_connection() や connection.close() の記述が不要になりました。
- SQL文を直接書かずに、Pythonのメソッドだけで操作が完結します。
- DictCursorを使わなくても、取得したデータは memo.title のように属性でアクセス可能です。
"""

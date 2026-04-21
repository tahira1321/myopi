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

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color_code = db.Column(db.String(7), default='#E3F2FD')
    symbol = db.Column(db.String(10), default='^▽^')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opinions = db.relationship('Opinion', backref='category_rel', lazy=True)

class Opinion(db.Model):
    __tablename__ = 'opinions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)

    question_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    last_reviewed_at = db.Column(db.DateTime,default=datetime.now) # リマインド用
    deadline = db.Column(db.Date, nullable=True) # 期限

    # 外部キー: usersテーブルとidの紐づけ
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # category
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    # 尺度
    priority = db.Column(db.Integer, default=3) # 重要度
    urgency = db.Column(db.Integer, default=3) # 緊急度
    satisfaction = db.Column(db.Integer, default=0) # 納得度
    # 詳細ステータス ('draft': 下書き, 'active': 確定, 'deleted': 削除)
    status = db.Column(db.String(20), nullable=False, default='active')

    # --- Create & Update ---
    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    # --- Read ---
    @classmethod
    def get_all_active(cls, user_id, sort_type='newest'):
        """指定されたユーザーの有効なメモをソートして取得"""
        query = cls.query.filter(cls.user_id == user_id, cls.status != 'deleted')

        # フィルタリング条件の追加
        if sort_type == 'drafts':
            query = query.filter(cls.status == 'draft')
        elif sort_type == 'active_only':
            query = query.filter(cls.status == 'active')

        # ソート順の決定
        if sort_type == 'oldest':
            return query.order_by(cls.created_at.asc()).all()
        elif sort_type == 'title':
            return query.order_by(cls.title.asc()).all()
        else:
            return query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_all_drafts(cls):
        """下書き一覧を取得"""
        return cls.query.filter(
                cls.status ==  'draft'
                ).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, opinion_id):
        """ id指定で1件取得 """
        return cls.query.get(opinion_id)

    # --- Delete ---
    def delete(self):
        """ 論理削除：statusをdeleteにして保存 """
        self.status = 'deleted'
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

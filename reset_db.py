# reset_db.py
from project import create_app, db
from project.models import User, Category, Opinion
from werkzeug.security import generate_password_hash

app = create_app()

def reset_database():
    with app.app_context():
        print("🛠  データベースを初期化中...")
        # 1. 全てのテーブルを削除
        db.drop_all()
        print("🗑  古いテーブルを削除しました。")
        
        # 2. models.py の定義に基づいてテーブルを新規作成
        db.create_all()
        print("✨ 新しいテーブルを作成しました。")

        # 3. サンプルデータの投入
        # ユーザー作成
        test_user = User(
            username="tahira",
            email="tahira@example.com",
            password=generate_password_hash("password123")
        )
        db.session.add(test_user)
        db.session.commit() # IDを確定させるために一度コミット

        # カテゴリ作成
        cat_q = Category(name="疑問", color_code="#E3F2FD", symbol="🤔", user_id=test_user.id)
        cat_o = Category(name="意見", color_code="#FFF3E0", symbol="💡", user_id=test_user.id)
        cat_c = Category(name="子ども", color_code="#E8F5E9", symbol="👶", user_id=test_user.id)
        db.session.add_all([cat_q, cat_o, cat_c])
        db.session.commit()

        # サンプルメモ作成
        sample_op = Opinion(
            title="なぜ空は青いの？",
            content="散乱が関係しているらしい。",
            question_date=app.config.get('CURRENT_DATE', '2026-04-18'), # 仮の日付
            category_id=cat_c.id,
            priority=5,
            urgency=20,
            status='active',
            user_id=test_user.id
        )
        db.session.add(sample_op)
        db.session.commit()
        
        print("✅ 全ての初期設定が完了しました！")

if __name__ == "__main__":
    reset_database()

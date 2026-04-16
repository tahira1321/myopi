# ==================== 
# import
# ==================== 
# Standard Library: (今回はなし)

# Third-party Library: フレームワーク関連
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Opinion, User
from werkzeug.security import check_password_hash

# Local Modules: (循環参照防止のため、関数内でインポート)
from .models import Opinion

# ==================== 
# Blueprint Instance Creation
# ==================== 
# このファイルの処理を、変数：main にまとめる
main = Blueprint('main', __name__)

# ==================== 
# Routes:Auth (認証関連)
# ==================== 
# --- login ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False # ログイン状態を保持

        user = User.query.filter_by(email=email).first()

        # ユーザーが存在しパスワードが一致するか確認
        if user and check_password_hash(user.password, password):
            # ログイン実行　※remember = True でブラウザを閉じても維持
            login_user(user, remember=remember)
            flash("ログインしました", "success")
            return redirect(url_for('main.index'))
        else:
            flash("メールアドレスまたはパスワードが正しくありません", "danger")

    return render_template('auth/login.html')

# --- logout ---
@main.route('/logout')
@login_required # ログイン中のみアクセス可能
def logout():
    logout_user()
    flash("ログアウトしました", "info")
    return redirect(url_for('main.login'))
        
# --- signup ---
@main.route('/signup')
def signup():
    return render_template('auth/signup.html')

# ==================== 
# Routes:View Function
# ==================== 
## --- Home (Memo List & Registration) ---
@main.route('/', methods=['GET', 'POST'])
@login_required # 未ログイン時は自動でログイン画面に遷移する
def index():
    # case POST
    if request.method == 'POST':
        ## formのname属性からデータを取得
        opi_title = request.form.get('title')
        opi_content = request.form.get('content')
        opi_question_date = request.form.get('question_date')

        # インスタンス化
        new_opinion = Opinion(
                title = opi_title, # 左:カラム名 右:フォームから取得したデータが入った変数
                content = opi_content,
                question_date = opi_question_date,
                user_id = current_user.id # usersテーブルのidから取得
                )

        # Save
        try:
            new_opinion.save()
            flash("メモを保存しました", "success")
        except Exception as e:
            flash(f"保存に失敗しました: {e}", "danger")

        return redirect(url_for('main.index'))

    # case GET
    all_opinions = Opinion.get_all_active()
    return render_template('index.html', name=current_user.username,  opinions=all_opinions)

# --- Edit ---
@main.route('/edit/<int:opinion_id>', methods=['GET', 'POST'])
@login_required
def edit_opinion(opinion_id):
    # get opinion's id
    opinion = Opinion.get_by_id(opinion_id)

    if not opinion:
        flash("該当するデータはありません", "warning")
        return redirect(url_for('main.index'))

    # POSTの場合のみ更新処理実行
    if request.method == 'POST':
        opinion.title = request.form.get('title')
        opinion.content = request.form.get('content')
        opinion.question_date = request.form.get('question_date')

        # Save
        opinion.save()
        flash("メモを更新しました", "success")
        return redirect(url_for('main.index'))

    # GETでアクセスされた場合は一覧に戻す
    return redirect(url_for('main.index'))

# --- Delete ---
@main.route('/delete/<int:opinion_id>')
def delete_opinion(opinion_id):
    opinion = Opinion.get_by_id(opinion_id)

    if opinion:
        opinion.delete()
        flash("メモを削除しました", "success")
    return redirect(url_for('main.index'))

# ==================== 
# Error Handling:Blueprint Specific
# ==================== 
###  Blueprint内のみで適応したいエラーハンドリング



# ==================== 
# Execution Flow Note
# ==================== 
"""
[ このファイルの役割 ]
1. URL（/）と実行する関数（index）を紐付ける「窓口」。
2. ユーザーの入力（request）を受け取り、データの加工を models.py に依頼する。
3. 最終的にどの HTML（template）を表示するかを決定する。

[ 開発時のTips ]
- フォームから送られてくる値は `request.form.get('name属性名')` で取得する。
- データの保存（POST）の後は、二重投稿を防ぐために必ず `redirect` させるのがマナー。
- `from . import models` を関数内でインポートしているのは、
  循環参照（お互いにインポートし合って動かなくなる現象）を防ぐための知恵。
"""

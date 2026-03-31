# ==================== 
# import
# ==================== 
# Standard Library: (今回はなし)

# Third-party Library: フレームワーク関連
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Local Modules: (循環参照防止のため、関数内でインポート)

# ==================== 
# Blueprint Instance Creation
# ==================== 
# このファイルの処理を、変数：main にまとめる
main = Blueprint('main', __name__)

# ==================== 
# Routes:View Function
# ==================== 
## --- Home (Memo List & Registration) ---
@main.route('/', methods=['GET', 'POST'])
def index():
    # import models
    from . import models

    # case POST
    if request.method == 'POST':
        ## formのname属性からデータを取得
        title = request.form.get('title')
        content = request.form.get('content')
        question_date = request.form.get('question_date')
        
        ## models.pyを使いDBに保存
        if models.save_memo(title, content, question_date):
            flash("メモを保存しました！", "success")
        else:
            flash("保存に失敗しました", "danger")

        ## 保存後に自分自身にredirect
        return redirect(url_for('main.index'))

    # case GET
    ## modelsで全データを取得
    all_memos = models.get_all_memos()

    ## 所得したデータをHTMLに渡す
    return render_template('index.html', memos=all_memos)

## --- Edit ---
@main.route('/edit/<int:memo_id>', methods=['GET', 'POST'])
def move_to_edit(memo_id):
    memo = models.get_memo_by_id(memo_id)
    return render_template('edit.html', memo=memo)

# データを取得し編集画面に表示
#@main.route('/edit', methods=['GET', 'POST'])
#def display_edit():
#    return 

# 編集を登録
@main.route('/edit/<int:memo_id>', methods=['GET', 'POST'])
def edit_memo(memo_id):
    # import models
    from . import models
    
    # Case POST
    if request.method == 'POST':
        memo_id = request.form.get('id')
        title = request.form.get('title')
        content = request.form.get('content')
        question_date = request.form.get('question_date')

        # update memo
        if models.update_memo(title, content, question_date, memo_id):
            flash("メモの変更完了", "success")
            return redirect(url_for('main.index'))
        else:
            flash("メモの更新に失敗しました", "danger")

        return redirect(url_for('main.index'))

    # Case GET
    memo = models.get_memo_by_id(memo_id)
    if not memo:
        flash("対象のメモが見つかりません", "warning")
        return ridirect(url_for('main.index'))

# --Delete
@main.route('/delete/<int:memo_id>', methods=['GET', 'POST'])
def delete_memo(memo_id):
    from . import models
    models.delete_memo(memo_id)
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

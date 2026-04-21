// --- 編集ボタンの処理 ---
document.querySelectorAll('.edBtn').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // ページ移動を阻止

        var id = this.getAttribute('data-id');
        var card = this.closest('.card');
        
        // カードからデータを取得
        var title = card.querySelector('.card-title').innerText;
        var content = card.querySelector('.card-text').innerText; // vard-textから修正
        var date = card.querySelector('.card-footer small').innerText.trim();

        // モーダルの入力欄に値をセット
        document.getElementById('edit-title').value = title;
        document.getElementById('edit-content').value = content;
        document.getElementById('edit-question_date').value = date;

        // 送信先URLをセット
        document.getElementById('edit-opi-form').action = '/edit/' + id;

        // モーダルを表示
        var editModalElement = document.getElementById('editOpinionModal');
        var modalInstance = new bootstrap.Modal(editModalElement);
        modalInstance.show();
    });
});

// --- 削除ボタンの処理 ---
document.querySelectorAll('.delBtn').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var id = this.getAttribute('data-id');
        if (confirm("本当に削除しますか？")) {
            window.location.href = "/delete/" + id;
        }
    });
});

/**
 * 新規作成モーダル内のカテゴリ切り替え処理
 * @param {string} categoryValue - カテゴリ名（DB保存用）
 * @param {string} guideText - ユーザーに表示するガイドメッセージ
 */
function setCategory(categoryValue, guideText) {
    // 1. フォームの隠しフィールド(hidden)の値を書き換え
    const categoryInput = document.getElementById('selected-category');
    if (categoryInput) {
        categoryInput.value = categoryValue;
    }

    // 2. ガイドテキストを書き換え
    const guideElement = document.getElementById('category-guide');
    if (guideElement) {
        guideElement.innerText = guideText;
    }

    // デバッグログ（開発が終わったら消してもOK）
    console.log("Selected Category ID/Name:", categoryValue);
}

function setCategory(categoryValue, guideText) {
    // 1. 隠しフィールドに値をセット
    document.getElementById('selected-category').value = categoryValue;

    // 2. ガイド文の書き換え
    document.getElementById('category-guide').innerText = guideText;

    // 3. 視覚的変化：全てのタブから「強調クラス」を外して、選んだものだけに付ける
    document.querySelectorAll('.nav-link').forEach(btn => {
        btn.style.transform = "scale(1)"; // 元のサイズ
    });
    event.currentTarget.style.transform = "scale(1.1) translateY(-5px)"; // 1.1倍に大きくして少し浮かせる
}

// 期限の制御
const deadlineInput = document.getElementById('deadline');
const noDeadlineCheck = document.getElementById('no-deadline');

if (noDeadlineCheck) {
    noDeadlineCheck.addEventListener('change', function() {
        if (this.checked) {
            deadlineInput.value = ""; // 値をクリア
            deadlineInput.disabled = true; // 入力不可にする
        } else {
            deadlineInput.disabled = false; // 入力可能にする
        }
    });
}

// Kotlin風トースト
document.addEventListener('DOMContentLoaded', function() {
    // 全てのトースト要素を取得
    const toastElements = document.querySelectorAll('.toast');

    toastElements.forEach(function(element) {
        // 3秒後に非表示にする（Kotlinの Toast.LENGTH_LONG 風）
        setTimeout(function() {
            element.classList.remove('show');
            // 要素自体を消すとガタつきの原因になるので、
            // Bootstrapの機能でフェードアウトさせるのが正解です。
            setTimeout(() => {
                element.style.display = 'none';
            }, 500);
        }, 3000);
    });
});

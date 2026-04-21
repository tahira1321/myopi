function setCategory(category) {
    const categoryInput = document.getElementById('selected-category');
    const guide = document.getElementById('category-guide');
    
    if (categoryInput) categoryInput.value = category;

    if (guide) {
        const messages = {
            'question': '「なぜ？」と思ったことを書き留めましょう。',
            'opinion': '自分の考えや、あるべき姿について整理しましょう。',
            'child': 'お子さんの純粋な問いや、そこからの気づきを記録します。'
        };
        guide.innerText = messages[category] || '';
    }
}

// ページ読み込み完了時の処理
document.addEventListener('DOMContentLoaded', function() {
    // 1. 日付の初期値を設定
    const dateInput = document.getElementById('question_date');
    if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }

    // 2. Flashメッセージの自動消去（3秒後にフェードアウト）
    const flashMessages = document.querySelectorAll('.alert'); // base.htmlのクラス名に合わせる
    flashMessages.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = "opacity 1.0s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 1000);
        }, 2000);
    });
});

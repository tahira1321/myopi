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

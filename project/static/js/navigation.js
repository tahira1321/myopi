// 次へ
const nextBtn = document.getElementById('nextBtn');
if (nextBtn) {
    nextBtn.addEventListener('click', function() {
        window.location.href = '/next';
    });
}

// 前へ
const prevBtn = document.getElementById('prevBtn');
if (prevBtn) {
    prevBtn.addEventListener('click', function() {
        window.history.back();
    });
}

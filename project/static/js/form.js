// Cancel Button
// 1. documentを取得し定数に代入
const cancelBtn = document.getElementById('cancelBtn');
const memoForm = document.getElementById('memo-form');
if (cancelBtn) {
    cancelBtn.addEventListener('click', function() {
        if(confirm('本当にキャンセルしてもよろしいですか？')) {
            memoForm.reset()
        }
    });
}

// Edit Button
// あらゆる「編集ボタン」に機能を付けられるようにする
const edBtns = document.querySelectorAll('.edBtn');
edBtns.forEach(function(Btn) {
    Btn.addEventListener('click', function() {
        const memoId = this.getAttribute('data-id');
        // コンソールで動作確認
        console.log("Edit ID:", memoId);
        if (memoId) {
            window.location.href = "/edit/" + memoId;
        }
    });
});

// Delete Button
const delBtn = document.querySelectorAll('.delBtn');
delBtn.forEach(function(Btn) {
    Btn.addEventListener('click', function() {
        const memoId = this.getAttribute('data-id');
        if (confirm("本当に削除しますか？")) {
            window.location.href = "/delete/" + memoId;
        }
    });
});

/* =================================================================
 * [覚書] 編集ボタンのフロントエンド制御 (Edit Logic)
 * =================================================================
 * [ この処理の役割 ]
1. 画面上の全「編集ボタン」を監視対象にする。
2. クリックされた瞬間に「誰のデータか（ID）」を特定する。
3. 特定した ID を URL に付与して、サーバー（Flask）へ移動する。

[ 情報の流れ（データフロー）の覚書 ]
- HTML: {{ memo.id }} ──(属性として付与)──> data-id="5"
- JS  : data-id ──(getAttributeで取得)──> const memoId
- 遷移 : memoId ──(URL連結)──> window.location.href = "/edit/5"

[ 理由とメリット ]
1. データの特定: `this` を使うことで、複数のボタンがあっても「今押された本人」を確実に識別できる。
2. 安全性: `const` を利用し、取得した ID が処理の途中で書き換わるリスクを排除する。
3. 柔軟性: HTMLの `id` 属性を使わず `data-*` 属性を使うことで、CSS設計や他のJS処理と干渉しない。

[ 実装時のTips ]
- querySelectorAll は「リスト（集団）」を返すため、必ず .forEach で一人ずつに解きほぐす必要がある。
- addEventListener の第1引数は 'click'。'ckick' などのタイポはイベントが発火しない原因になる。
- 遷移先の URL `/edit/` の末尾に `/` があるか、サーバー側のルート設計と一致させること。

[ 構成要素の深掘り備忘録 ]

1. querySelectorAll('.edBtn') : 「全対象のリストアップ」
   - 役割: クラス名が一致する全ての要素を NodeList（配列のようなもの）として取得する。
   - メリット: ボタンが1個でも100個でも、同じコードで一括管理できる。

2. .forEach(function(btn) { ... }) : 「個別への任務付与」
   - 役割: 取得したリストを上から順に走査し、各ボタンに「クリック待ち」という任務を与える。
   - 注意: ここで渡す引数名（btn）を、中の addEventListener の対象として使うこと。

3. this.getAttribute('data-id') : 「本人照合の決め手」
   - 役割: `this` はイベントが発生した「そのボタン自身」を指す。
   - メリット: 「隣のボタンのID」を誤って取得するような事故を防げる。

[ 安全な変数宣言（const vs let vs var）]

1. const (定数):
   - 役割: 再代入（書き換え）を禁止する宣言。
   - 場面: 今回の `memoId` のように、取得した後に値が変わることがない場合に最適。
   - 利点: 意図しない書き換えによるバグを防ぎ、読み手に「この値は変わらない」と安心感を与える。

2. let (変数):
   - 役割: 再代入を許可する宣言。
   - 場面: ループのカウント（i++）や、条件によって中身を入れ替えたい時に使う。

3. var (古い宣言):
   - 役割: 昔のJSで使われていた宣言。
   - 欠点: スコープ（有効範囲）が広すぎて予期せぬ場所でデータが衝突しやすいため、現代の開発（ES6以降）では原則使用しない。

[ 開発者のマインドセット（UXへの配慮）]

1. 実行前のチェック:
   - `if (memoId)` のように、IDが空でないことを確認してから遷移させる。
   - 万が一、HTML側のミスでIDが取れなかった場合に、変なURLへ飛ばさないための防衛策。

2. フィードバック:
   - 必要に応じて `console.log` を残しておく（本番公開時は消す）。
   - 開発中、Vimの画面とブラウザのコンソールを往復して「正しくIDが掴めているか」を確認する習慣が、デバッグ能力を高める。

[ データベース操作への橋渡し ]
- window.location.href: これを実行した瞬間、フロントエンドの仕事は終わり、バトンは Flask（main.py）へ渡される。
- 受け取った Flask は、URLに含まれる ID を models.py の `get_memo_by_id(id)`（これから作成）に渡し、DBから特定の1件を釣り上げる。
 * * ================================================================= */

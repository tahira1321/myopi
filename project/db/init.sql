-- ====================
-- 1. Database & User Setup (環境構築)
-- ====================
-- データベースの作成（存在しない場合のみ）
CREATE DATABASE IF NOT EXISTS project_db;
USE project_db;

-- ====================
-- 2. Table Definition (テーブル作成)
-- ====================
CREATE TABLE IF NOT EXISTS memos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    question_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_question_date (question_date),
    INDEX idx_status (status)
    )  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================
-- 3. Initial Data (サンプルデータ)
-- ====================
-- 動作確認用の初期データ（最初の1件目）
INSERT INTO memos (title, content, question_date, status)
VALUES (
    '開発スタート', 
    '今日からメモアプリの開発を開始しました。', 
    CURDATE(), 
    'published'
);

-- ====================
-- Roadmap & Tips (自分への備忘録)
-- ====================
/*
[ このファイルの役割 ]
1. MySQL導入直後の「まっさらな状態」から、一瞬でアプリを動かせる状態にする。
2. テーブル構造（スキーマ）を定義し、データの型やルールを決定する。

[ 開発時のTips ]
- DATETIME(6): 修正時間が重なった時も区別できるよう、0.000001秒単位まで記録。
- INDEX: データの件数が数千件、数万件と増えた時に、検索が遅くなるのを防ぐための「目次」。
- CHARSET=utf8mb4: 絵文字や特殊な漢字（人名など）も正しく保存できるようにするための設定。

[ 実行コマンド（ターミナル用） ]
mysql -u root -p < init.sql

[ SQL設定の深掘り備忘録 ]
- ENGINE=InnoDB: データの整合性を守る標準エンジン。
- utf8mb4: 絵文字や特殊漢字も保存できる最強の文字セット。
- CURDATE(): 実行時の「今日」を自動入力する便利な関数。
- COLLATE: 文字の比較ルール。検索や並び替えの挙動を決める。
*/

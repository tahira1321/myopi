-- ====================
-- 1. Database & User Setup (環境構築)
-- ====================
-- データベースの作成（存在しない場合のみ）
CREATE DATABASE IF NOT EXISTS project_db;
USE project_db;

-- ====================
-- 2. Table Definition (テーブル作成)
-- ====================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
    );

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    color_code VARCHAR(7) DEFAULT '#3E2EFD',
    symbol VARCHAR(10) DEFAULT '^▽^',
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS opinions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT,

    -- 拡張機能
    category_id INTEGER,   -- 疑問、意見、子どもetc
    priority INTEGER DEFAULT 3,                -- 重要度
    urgency INTEGER DEFAULT 3,                 -- 緊急度
    satisfaction INTEGER DEFAULT 0,            -- 納得度

    -- ステータス管理
    status VARCHAR(50) NOT NULL DEFAULT 'draft',

    -- 時間管理
    question_date DATE NOT NULL,
    deadline DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    last_reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- ユーザー連携
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES catetories (id) ON DEKETE SET NULL
    );
-- ====================
-- 3. Initial Data (サンプルデータ)
-- ====================
-- 1. まずユーザーを作る
INSERT INTO users (username, email, password) 
VALUES ('tahira', 'tahira@example.com', 'pbkdf2:sha256:600000$pZpcAhPqocCg2oAf$8d1faf45c26faee62669bd2769de039de2ad7423324f4f5d2d75e8ca06462c00'); -- パスワードはハッシュ値が必要

-- 2. 次にカテゴリを作る
INSERT INTO categories (name, color_code, symbol, user_id) 
VALUES 
('疑問', '#E3F2FD', '🤔', 1),
('意見', '#FFF3E0', '💡', 1),
('子ども', '#E8F5E9', '👶', 1);

-- 3. 最後にメモ（Opinion）を入れる
-- category_id には、上記で作ったカテゴリの ID (1, 2, 3) を指定します
INSERT INTO opinions (title, content, question_date, category_id, priority, urgency, status, user_id, deadline)
VALUES (
    'なぜ空は青いの？', 
    '散乱が関係しているらしい。', 
    CURRENT_DATE, 
    3,    -- '子ども' カテゴリのID
    5,    -- 重要度
    20,   -- 緊急度 (%)
    'active',
    1,    -- ユーザーID
    '2026-05-01' -- 期限
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

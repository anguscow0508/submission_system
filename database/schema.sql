
-- 建立使用者資料表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    role VARCHAR(10) NOT NULL
        CHECK (role IN ('author', 'editor'))
);

-- 建立投稿資料表
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL
        REFERENCES users(id),
    category VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL
        DEFAULT '編輯中'
        CHECK (status IN ('編輯中', '審查中', '已通過'))
);

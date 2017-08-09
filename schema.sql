create table if not exists reviews (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user` TEXT NOT NULL,
  `review` TEXT NOT NULL,
  `company_id` INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS companies (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL UNIQUE,
  `description` TEXT NOT NULL,
  `details` TEXT NOT NULL,
  `rating` TEXT NOT NULL,
  `logo` TEXT NOT NULL,
  `adress` TEXT NOT NULL UNIQUE,
  `category_id` INTEGER
);


CREATE TABLE IF NOT EXISTS categories (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `type` TEXT NOT NULL UNIQUE
);

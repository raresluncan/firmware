create table if not exists reviews (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id`	INTEGER NOT NULL,
  `review` TEXT NOT NULL,
  `company_id` INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS companies (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL UNIQUE,
  `description` TEXT NOT NULL,
  `details` TEXT NOT NULL,
  `rating` INTEGER NOT NULL,
  `logo` TEXT NOT NULL,
  `adress` TEXT NOT NULL UNIQUE,
  `category_id` INTEGER NOT NULL,
  `added_by_id` INTEGER NOT NULL,
);


CREATE TABLE IF NOT EXISTS categories (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `type` TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS users (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT NOT NULL UNIQUE,
	`password`	TEXT NOT NULL,
	`email`	TEXT NOT NULL UNIQUE,
	`name`	TEXT NOT NULL,
	`surname`	TEXT NOT NULL,
  `avatar`	TEXT NOT NULL,
  `contact`	TEXT NOT NULL,
  `privilege`	TEXT,
	`gender`	INTEGER NOT NULL
);

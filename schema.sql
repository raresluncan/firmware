create table if not exists reviews (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user` TEXT NOT NULL,
  `review` TEXT NOT NULL,
  `company_id` INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS companies (
  `company_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `company_name` TEXT NOT NULL UNIQUE,
  `company_description` TEXT NOT NULL,
  `company_details` TEXT NOT NULL,
  `company_rating` TEXT NOT NULL,
  `company_logo` TEXT NOT NULL,
  `company_adress` TEXT NOT NULL,
  `category_id` INTEGER
);


CREATE TABLE IF NOT EXISTS category (
  `category_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `category_type` TEXT NOT NULL UNIQUE
);

create table if not exists reviews (
<<<<<<< HEAD
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user` TEXT NOT NULL,
  `review` TEXT NOT NULL,
  `company_id` INTEGER NOT NULL
=======
  `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
  `user`	TEXT NOT NULL,
  `review`	TEXT NOT NULL,
  `company_id`	INTEGER NOT NULL
>>>>>>> Changes requested
);


CREATE TABLE IF NOT EXISTS companies (
<<<<<<< HEAD
  `company_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `company_name` TEXT NOT NULL UNIQUE,
  `company_description` TEXT NOT NULL,
  `company_details` TEXT NOT NULL,
=======
  `company_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
  `company_name`	TEXT NOT NULL UNIQUE,
  `company_description` TEXT NOT NULL,
  `company_details`	TEXT NOT NULL,
>>>>>>> Changes requested
  `company_rating` TEXT NOT NULL,
  `company_logo` TEXT NOT NULL
);

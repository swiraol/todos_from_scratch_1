CREATE TABLE lists (
  id SERIAL PRIMARY KEY,
  title text NOT NULL UNIQUE,
);

CREATE TABLE todos (
  id SERIAL PRIMARY KEY,
  title text NOT NULL,
  completed BOOLEAN NOT NULL DEFAULT false,
  list_id REFERENCES lists (id) DELETE ON CASCADE,
);
drop table if exists hash_table;
create table hash_table (
  id integer primary key autoincrement,
  hash text not null,
  block text not null
);

drop table if exists block_table;
create table block_table (
  id integer primary key autoincrement,
  start_hash integer not null,
  end_hash integer,
  closed integer default 0,
  merkle_root text,
  tx_id text
);

INSERT INTO hash_table (hash,block) VALUES ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 1);
INSERT INTO block_table (start_hash) VALUES (1);
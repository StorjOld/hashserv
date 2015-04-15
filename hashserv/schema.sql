drop table if exists hash_table;
create table hash_table (
  id integer primary key autoincrement,
  hash text not null,
  receipt text not null
);
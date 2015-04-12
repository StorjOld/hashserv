drop table if exists files;
create table files (
  id integer primary key autoincrement,
  hash text not null,
  receipt text not null
);
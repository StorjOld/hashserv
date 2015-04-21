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
  end_hash integer not null,
  closed integer  not null,
  merkle_root text not NULL,
  tx_id text not null
)
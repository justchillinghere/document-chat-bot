create table users (
	id serial primary key,
	created_at timestamp default current_timestamp not null,
	telegram_id integer not null unique
)
drop table if exists users;
drop table if exists accounts;
drop table if exists users_accounts;
drop table if exists transactions;
drop table if exists accounts_transactions;
drop table if exists notifications;
drop table if exists users_notifications;

create table users (
	id integer primary key autoincrement,
	username text unique not null,
	email text unique not null,
	otp text not null,
	fullname text not null
);

create table accounts (
	id integer primary key autoincrement,
	iban text unique not null,   -- RO16 FOXB 0000 0000 0000 0000
	currency text not null,      -- EUR, RON, USD, ?
	account_type text not null,  -- checking, savings, ?
	custom_name text             -- 'Car Savings'; name set by user
);

create table users_accounts (
	user_id integer not null,           -- one user can have multiple accounts
	account_id integer UNIQUE not null, -- one account can only have one user
	foreign key (user_id) references users (id),
	foreign key (account_id) references accounts (id)
);

create table transactions (
	id integer primary key autoincrement,
	datetime text not null,
	other_party text not null, -- JSON data describing sender/recipient/etc 
	                           -- depending on transaction type
	status text not null,      -- processed, failed, reverted, pending, etc
	type text not null,        -- send_transfer, receive_transfer, card_payment, fee, ...
	extra text                 -- depending on type, JSON data describing extra info
);

create table accounts_transactions (
	account_id integer not null,
	transaction_id integer UNIQUE not null,
	foreign key (account_id) references accounts (id),
	foreign key (transaction_id) references transactions (id)
);

create table notifications (
	id integer primary key autoincrement,
	body text not null,
	datetime text not null,
	read integer not null
);

create table users_notifications (
	user_id integer not null,
	notification_id integer UNIQUE not null,
	foreign key (user_id) references users (id),
	foreign key (notification_id) references notifications (id)
);

create view V_account_balance as
select 
	accounts_transactions.account_id as "account_id",
	sum(json_extract(transactions.extra, '$.amount')) as "balance"
from transactions
inner join accounts_transactions on accounts_transactions.transaction_id = transactions.id
group by accounts_transactions.account_id;

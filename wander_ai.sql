drop database if exists wander_ai;
create database if not exists wander_ai;
use wander_ai;

drop table if exists user;
drop table if exists suggestion;
drop table if exists user_history;
drop table if exists admin;

create table user(
	account_id varchar(10) primary key,
    password varchar(255) not null,
    nickname varchar(20) not null
);

create table suggestion(
	id int primary key auto_increment,
	account_id varchar(10) not null,
    message text
);

create table user_history(
	id int primary key auto_increment,
    session_id varchar(150) not null,
	account_id varchar(10) not null,
    title varchar(255)
);

create table admin(
	admin_id varchar(10) primary key,
    password varchar(255) not null
);

-- 创建一个默认的管理员账户，密码为 123456
insert into admin values("12345678", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92");
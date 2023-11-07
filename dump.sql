/*Apartment – номера
(id, apart_name)
Client - клиенты
(id, client_name)
Orders – бронь
(id, id_apartment, id_client, beg_date, end_date, vip_status)*/
--create tables
/*не должно быть больше двух одинаковых клиентов
*/
create schema hotel

create table apartment
(id int generated always as identity,
apart_name varchar(30) not null,
primary key(id));

create table client
(id int generated always as identity,
client_name varchar(30),
primary key(id));

create table orders
(id int generated always as identity,
id_apartment int,
id_client int,
beg_date date,
end_date date,
vip_status int,
primary key (id));
--alter table
alter table client set schema hotel;
alter table orders set schema hotel;
alter table hotel.orders add column dismiss_date date;
alter table hotel.orders add constraint
fk_orders_apartmnet foreign key(id_apartment) references hotel.apartment(id);
alter table hotel.orders add constraint
fk_orders_client foreign key(id_client) references hotel.client(id);
--create user
create user hotelapi with password 'hotel123';
grant usage on schema hotel to hotelapi;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA hotel to hotelapi;
set search_path to public, hotel;

--insert
insert into client (client_name) values('client1');
insert into client (client_name) values('client2');
insert into client (client_name) values('client3');
insert into client (client_name) values('client4');

insert into apartment (apart_name) values('apartment1');
insert into apartment (apart_name) values('apartment2');
insert into apartment (apart_name) values('apartment3');
insert into apartment (apart_name) values('apartment4');
insert into apartment (apart_name) values('apartment5');
insert into apartment (apart_name) values('apartment6');
commit;

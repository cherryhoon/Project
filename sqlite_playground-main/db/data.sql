insert into author(name, born) values
('Laurence', '04-12-2010'),
('Jim', '06-10-2010'),
('Carry', '09-11-2011');

insert into author_died(died, author_id) values
('05-05-2023', 1);

insert into country(name) values
('Australia'),
('India'),
('Deutschland'),
('España'),
('La France'),
('中國'); -- 6

insert into category(name) values
('Science'),
('Nature'),
('Wildlife'),
('Biology'),
('Physics'),
('Chemistry'); -- 6

insert into item(name, creation_date, category_id) values
('Attitude', '04-12-2010', 1),
('This is Water', '04-12-2010', 2),
('Why Go Out?', '04-12-2010', 3),
('Why Go Out? Vol 2', '06-12-2010', 3),
('A Star in a Bottle', '04-12-2010', 4),
('How the First Gravitational Waves Were Found', '04-12-2010', 5),
('Thresholds of Violence', '04-12-2010', 6),
('We Are All Confident Idiots', '04-12-2010', 1),
('Fantastic Beasts and How to Rank Them', '04-12-2010', 2),
('What is the Monkeysphere?', '04-12-2010', 3),
('Losing Earth', '04-12-2010', 4),
('The New Abolitionism', '04-12-2010', 5); -- 12

insert into author_country(country_id, author_id) values
(1, 1),
(2, 1),
(3, 2),
(4, 3),
(5, 3),
(6, 3);

insert into author_item(author_id, item_id) values
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(2, 6),
(3, 6),
(2, 7),
(2, 8),
(2, 9),
(3, 10),
(3, 11),
(3, 12),
(2, 12);

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE player (
  id SERIAL PRIMARY KEY,
  name varchar(200)
);

CREATE TABLE match (
  tournament_no integer NOT NULL,
  round_no integer NOT NULL,
  player_1 integer REFERENCES player(id),
  player_2 integer REFERENCES player(id),
  winner integer REFERENCES player(id)
);

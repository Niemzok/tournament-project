  -- Table definitions for the tournament project.
  --
  -- Put your SQL 'create table' statements in this file; also 'create view'
  -- statements if you choose to use it.
  --
  -- You can write comments in this file by starting them with two dashes, like
  -- these lines here.

  DROP DATABASE IF EXISTS tournament;
  CREATE DATABASE tournament;
  \c tournament

  CREATE TABLE player (
    id SERIAL PRIMARY KEY,
    name varchar(200)
  );

  CREATE TABLE match (
    id SERIAL PRIMARY KEY,
    tournament_no integer NOT NULL,
    loser integer REFERENCES player(id) ON DELETE CASCADE,
    winner integer REFERENCES player(id) ON DELETE CASCADE,
    CHECK (winner <> loser)
  );

  CREATE VIEW standings AS SELECT a.id, a.name, COUNT(b.winner) AS wins, a.no_matches AS
              matches from (SELECT player.id, player.name AS name, COUNT(match.winner)
              AS no_matches from player LEFT JOIN match ON (player.id=match.winner
              OR player.id=match.loser) GROUP BY player.id) AS a LEFT JOIN
              match AS b on a.id=b.winner GROUP BY a.id,a.name,a.no_matches
              ORDER BY wins desc;

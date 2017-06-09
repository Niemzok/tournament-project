#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import randint


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM match;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM player;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM player;")
    count = c.fetchone()[0]
    db.close()
    return count



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO player (name) VALUES (%s);" , (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("select a.id, a.name, count(b.winner) as wins, a.no_matches as "
             + "matches from (select player.id, player.name as name, count(match.player_1) "
             + "as no_matches from player LEFT JOIN match ON (player.id=match.player_1 "
             + "OR player.id=match.player_2) group by player.id) as a LEFT JOIN "
             + "match as b on a.id=b.winner group by a.id,a.name,a.no_matches "
             + "order by wins desc;")
    standings = c.fetchall()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO match VALUES (1,1,%s,%s,%s);" % (winner,loser,winner))
    db.commit()
    db.close()




def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT id,name FROM player;")
    results = c.fetchall()
    players = [result for result in results]
    db.close()
    pairings = []
    no_pairings = int(len(players)/2)
    for i in range(no_pairings):
        i1 = randint(0,len(players)-1)
        p1 = players[i1]
        del players[i1]
        i2 = randint(0,len(players)-1)
        p2 = players[i2]
        del players[i2]
        pairings.append((p1+p2))
    return pairings

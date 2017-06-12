#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import randint


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
    except:
        print("<error message>")
    return db, cursor


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute("DELETE FROM match;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute("DELETE FROM player;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db ,c = connect()
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
    db, c = connect()
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
    db, c = connect()
    c.execute("select * from standings;")
    standings = c.fetchall()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    c.execute("INSERT INTO match (tournament_no, winner, loser) VALUES (1,%s,%s);" % (winner,loser))
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
    standings = playerStandings()
    pairings = []
    win_groups = {}
    for player in standings:
        if player[2] in win_groups:
            win_groups[player[2]].append(player)
        else:
            win_groups[player[2]] = [player]
    for key in win_groups:
        players = win_groups[key]
        no_pairings = int(len(players)/2)
        for i in range(no_pairings):
            i1 = randint(0,len(players)-1)
            p1 = (players[i1][0],players[i1][1])
            del players[i1]
            i2 = randint(0,len(players)-1)
            p2 = (players[i2][0],players[i2][1])
            del players[i2]
            pairings.append((p1+p2))
    return pairings

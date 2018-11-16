# 507 Homework 10 Part 2
import sqlite3 as sqlite

#### Part 2 ####
print('\n*********** PART 2 ***********')

# Params: game_id (ie. 1)
# Returns: A string formatted as follows with the game’s information:
# {Round Name}: ({Winner Seed}) {Winner} defeated ({Loser Seed}) {Loser}
# {Winner Score}-{Loser Score}
# Note: You must use only one SQL statement in this function.
def get_info_for_game(game_id):
    # Your code goes here
    conn = sqlite.connect('wuting-wei_big10.sqlite')
    cur = conn.cursor()

    statement = '''
        SELECT r.Name, t.Seed, t.Name, t2.Seed, t2.Name, g.WinnerScore, g.LoserScore
        FROM Games AS g
            JOIN Rounds AS r ON r.Id=g.Round
                JOIN Teams AS t ON g.Winner=t.Id
                    JOIN Teams AS t2 on g.Loser=t2.Id
        WHERE r.Id=?
    '''
    cur.execute(statement, (game_id,))
    fetched_data = cur.fetchone()
    #print(fetched_data)

    output = "{}: ({}){} defeated ({}){} {}-{}".format(fetched_data[0], fetched_data[1], fetched_data[2], fetched_data[3], fetched_data[4], fetched_data[5],fetched_data[6])

    conn.close()
    return output

# Prints all of the round names a team won (sorted from lowest round id to
# highest round id) and the corresponding scores
# Params: team_name (ie. “Michigan”)
# Returns: a combined string like "Michigan won:\nFirst Round: 96-87\nSecond Round: 123-110"
# Note: You must use only one SQL statement in this function.
def print_winning_rounds_for_team(team_name):
    # Your code goes here
    conn = sqlite.connect('wuting-wei_big10.sqlite')
    cur = conn.cursor()

    statement = '''
        SELECT r.Name, g.WinnerScore, g.LoserScore
        FROM Games as g
            JOIN Rounds as r ON r.Id = g.Round
                JOIN Teams as t ON t.Id=g.Winner
        WHERE t.Name=?
    '''
    cur.execute(statement, (team_name, ))
    fetched_data = cur.fetchall()

    output = "{} won:\n".format(team_name)

    for i in fetched_data:
        output += "{}: {}-{}\n".format(i[0], i[1], i[2])

    print(output)
    conn.close()
    return output

# Update the database to include the following Championship game information:
#   Round Name: “Championship”
#   Round Date: “03-04-18”
#   Winner: “Michigan”
#   Loser: “Purdue”
#   WinnerScore: 75
#   LoserScore: 66
#   Time: “4:30pm”
# Params: None
# Returns: Success string (detailed in spec)
# Note: You will need to update the ‘Games’ and ‘Rounds’ tables with the above
# data.  You are permitted to use multiple SQL statements in this function.
def add_championship_info():
    # Your code goes here
    conn = sqlite.connect('wuting-wei_big10.sqlite')
    cur = conn.cursor()

    statement = '''
        DELETE FROM Games
        WHERE Round="5"
    '''
    cur.execute(statement)

    statement = '''
            DELETE FROM Rounds
            WHERE Name='Championship'
        '''
    cur.execute(statement)


    statement = '''
        SELECT t.Id
        FROM Games AS g
            JOIN Teams AS t ON t.Id = g.Winner
        WHERE t.Name="Michigan"
    '''
    cur.execute(statement)
    winner_id_tup = cur.fetchone()
    print(winner_id_tup)

    statement = '''
        SELECT t.Id
        FROM Games AS g
            JOIN Teams AS t ON t.Id = g.Winner
        WHERE t.Name="Purdue"
    '''
    cur.execute(statement)
    loser_id_tup = cur.fetchone()
    print(loser_id_tup)


    statement = '''
            INSERT INTO Rounds(Name, Date)
            VALUES (?, ?)
        '''
    insertion = ("Championship", "03-04-18")
    cur.execute(statement, insertion)

    statement = '''
            SELECT Id FROM Rounds
            WHERE Name="Championship"
        '''
    cur.execute(statement)
    round_id_tup = cur.fetchone()
    print(round_id_tup)

    statement = '''
        INSERT INTO Games (Round, Winner, Loser, WinnerScore, LoserScore, Time)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    cur.execute(statement, (round_id_tup[0], winner_id_tup[0], loser_id_tup[0], 75, 66, "4:30pm"))


    conn.commit()
    conn.close()

    return "Added game."


if __name__ == "__main__":
    game_info = get_info_for_game(1)
    print(game_info)
    print("-"*15)

    print_winning_rounds_for_team("Michigan")
    print("-"*15)

    status = add_championship_info()
    print(status)
    print("-"*15)

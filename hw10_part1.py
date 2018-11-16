# 507 Homework 10 Part 1
import csv
import sqlite3 as sqlite

#### Part 1 ####
print('\n*********** PART 1 ***********')

# Creates a database called yourlastnamefirstname_big10.sqlite
def create_tournament_db():
    # Your code goes here
    try:
        conn = sqlite.connect('wuting-wei_big10.sqlite')
        cur = conn.cursor()

        # Code below provided for your convenience to clear out the big10 database
        # This is simply to assist in testing your code.  Feel free to comment it
        # out if you would prefer
        statement = '''
                DROP TABLE IF EXISTS 'Teams';
            '''
        cur.execute(statement)

        statement = '''
                DROP TABLE IF EXISTS 'Games';
            '''
        cur.execute(statement)

        statement = '''
                DROP TABLE IF EXISTS 'Rounds';
            '''
        cur.execute(statement)
        conn.commit()

    except:
        print("Can't create a database")

# Populates big10.sqlite database using csv files
def populate_tournament_db():

    # Connect to big10 database
    conn = sqlite.connect('wuting-wei_big10.sqlite')
    cur = conn.cursor()


    # Your code goes here
    # HINTS:
    # Column order in teams.csv file: Seed,Name,ConfRecord
    # Column order in games.csv file: Winner,Loser,WinnerScore,LoserScore,Round,Time
    # Column order in rounds.csv file: Name,Date

    statement = '''
        CREATE TABLE 'Teams'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Seed' INTEGER NOT NULL,
            'Name' TEXT NOT NULL,
            'ConfRecord' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    with open('teams.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            statement = '''
                INSERT INTO Teams
                VALUES (?, ?, ?, ?)
            '''
            insertion = (None, row[0], row[1], row[2])
            cur.execute(statement, insertion)


    statement = '''
                CREATE TABLE 'Games'(
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'Winner' INTEGER NOT NULL,
                    'Loser' INTEGER NOT NULL,
                    'WinnerScore' INTEGER NOT NULL,
                    'LoserScore' INTEGER NOT NULL,
                    'Round' INTEGER NOT NULL,
                    'Time' TEXT NOT NULL
                );
            '''
    cur.execute(statement)

    with open('games.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            insertion = (row[0], row[1], row[2], row[3], row[4], row[5])
            statement = "INSERT INTO Games (Winner, Loser, WinnerScore, LoserScore, Round, Time)"
            statement += 'VALUES (?, ?, ?, ?, ? ,?)'
            cur.execute(statement, insertion)


    statement = '''
                    CREATE TABLE 'Rounds'(
                        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                        'Name' TEXT NOT NULL,
                        'Date' DATE NOT NULL
                    );
                '''
    cur.execute(statement)

    with open('rounds.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            insertion = (row[0], row[1])
            statement = "INSERT INTO Rounds (Name, Date)"
            statement += 'VALUES (?, ?)'
            cur.execute(statement, insertion)

    # Close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tournament_db()
    print("Created big10 Database")
    populate_tournament_db()
    print("Populated big10 Database")

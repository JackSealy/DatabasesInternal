import sqlite3, tabulate, csv, random

con = sqlite3.connect('pokemon.db')
cur = con.cursor()

# For creating the database, only used once at the beginning or if I want to restart the database
def createDB():
    # Dropping the tables so I don't have 2 of each
    cur.execute("DROP TABLE IF EXISTS 'Pokemon';")
    cur.execute("DROP TABLE IF EXISTS 'Players';")
    
    # Creatibng the player table, only need first name and last name, age is not required
    cur.execute("""
    CREATE TABLE Players( 
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Age INTEGER
    );
    """)

    # Creating the pokemon table, needs a name, atleast one type, all the stats, as well 
    # as what generation it was from, if it is a legendary, its cost and its Owner's ID
    cur.execute("""
    CREATE TABLE Pokemon(
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,    
        Type1 TEXT NOT NULL,
        Type2 TEXT,
        StatsTotal INT NOT NULL, 
        HP INT NOT NULL,
        Attack INTEGER NOT NULL,
        Defense INTEGER NOT NULL,
        SpAtk INTEGER NOT NULL,
        SpDef INTEGER NOT NULL,
        Speed INTEGER NOT NULL,
        Generation INTEGER NOT NULL,
        Legendary TEXT NOT NULL,
        Cost INTEGER NOT NULL,
        OwnerID INTEGER NOT NULL,
        FOREIGN KEY (OwnerID) REFERENCES Players(ID)
    );
    """)
    InsertCSV("players")
    InsertCSV("pokemon")

def InsertCSV(name):
    with open((name + ".csv"), 'r') as file:
        reader = csv.reader(file)
        for row in reader: 
            if name == "players":
                cur.execute("INSERT INTO Players (ID, FirstName, LastName, Age) VALUES (?, ?, ?, ?);", (row[0], row[1], row[2], row[3]))
            if name == "pokemon":
                cur.execute("""INSERT INTO Pokemon 
                (ID, Name, Type1, Type2, StatsTotal, HP, Attack, Defense, SpAtk, SpDef, Speed, Generation, Legendary, Cost, OwnerID) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], 
                round(random.uniform(1.0, 50.0),2), random.randint(1,10))) # Money and OwnerID, randomly selected because I don't want to go through it manually

createDB()

cur.execute("""
SELECT Pokemon.ID, Pokemon.Name, Pokemon.Type1, Pokemon.Type2, Pokemon.StatsTotal, Pokemon.HP, Pokemon.Attack, Pokemon.Defense, Pokemon.SpAtk,
Pokemon.SpDef, Pokemon.Speed, Pokemon.Generation, Pokemon.Legendary, Pokemon.Cost, Players.FirstName FROM Pokemon
INNER JOIN Players ON Pokemon.OwnerID = Players.ID
ORDER BY Pokemon.ID
""")

headers = ["ID", "Name", "Type1", "Type2", "Total", "HP", "Atk", "Def", "SpAtk", "SpDef", "Speed", "Gen", "Legend", "Cost", "Owner"]
print(tabulate.tabulate(cur.fetchall(), headers, tablefmt = 'github'))

con.commit()
con.close()
import sqlite3, tabulate, csv, random

# Connecting to the database and creating a cursor to execute queries
con = sqlite3.connect('pokemon.db')
cur = con.cursor()

# Declaring some variables
validTypes = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dark", "Dragon", "Steel", "Fairy"]

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
        Cost FLOAT(4,2) NOT NULL,
        OwnerID INTEGER NOT NULL,
        FOREIGN KEY (OwnerID) REFERENCES Players(ID)
    );
    """)
    InsertCSV("players")
    InsertCSV("pokemon")

# A function to insert a CSV file into the database
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
                round(random.uniform(1.0, 50.0),2), random.randint(1,20))) # Money and OwnerID, randomly selected because I don't want to go through it manually

# This function checks if the stat is below the max, if it isn't it raises an exception that gets called in addPokemon
def validCheck(stat, max):
    if stat > max or stat < 0:
        raise Exception("Sorry, no numbers below zero or above the max")

# This function asks the user what they would want to do
def navigation():
    try:
        choice = input("What would you like to do? type 'n' to add a new pokemon, 'r' to remove something from the database, 'p' to print the database or 's' to search for something and press\n")
        if choice == "n":
            addPokemon()
        if choice == "r":
            removeData()
        if choice == "p":
            printPokemon()
        if choice == "s":
            searchDatabase()
    except:
        print("An error has occured, try again.\n")
        navigation()

# This function is used to insert a pokemon that is created with user input into the database, as well as the user who entered it
def addPokemon():
    ## Make sure that required fields are not empty

    try:
        existTest = input("Are you an existing user? (Y|N) ").upper()
        if existTest == "N":
            userfirstname = input("What is your first name? ") # 
            userlastname = input("What is your last name? ") # 
            userage = input("What is your age? (Press Enter if your would rather leave it blank) ")
        elif existTest == "Y":
            ownerid = int(input("What is your OwnerID? "))
        else:
            raise Exception("Error while checking for existing user")

        name = input("What is the name of your pokemon? ") #
        type1 = input("What is type is your pokemon? ").title()  #
        if type1 in validTypes:
            pass
        else: 
            raise Exception("Sorry, that is an invalid type")
        type2 = input("What is your pokemon's second type? (Press Enter if empty) ").title() 
        if type2 in validTypes:
            pass
        elif type2 == "":
            pass
        else: 
            raise Exception("Sorry, that is an invalid type")
        hp = int(input("How much health does your pokemon have? (Max = 150) ")) #
        validCheck(hp, 150)
        attack = int(input("How much attack does your pokemon have? (Max = 150) ")) #
        validCheck(attack, 150)
        defense = int(input("How much defense does your pokemon have? (Max = 150) ")) #
        validCheck(defense, 150)
        spatk = int(input("How much special attack does your pokemon have? (Max = 150) ")) #
        validCheck(spatk, 150)
        spdef = int(input("How much special defense does your pokemon have? (Max = 150) ")) #
        validCheck(spdef, 150)
        speed = int(input("How fast is your pokemon? (Max = 150) ")) #
        validCheck(speed, 150)
        total = hp + attack + defense + spatk + spdef + speed
        generation = int(input("What generation is your pokemon from? (Max = 8) ")) #
        validCheck(generation, 8)
        legendary = input("Is your pokemon a legendary (True/False) ").title() #
        if legendary == "True" or legendary == "False":
            pass
        else:
            raise Exception("Error with legendary typing")
        cost = round(float(input("How much is your pokemon card worth? (Max = $50.00) ")),2) #
        validCheck(cost, 50)
    
        if existTest == "N":
            if userage != "":
                userage = int(userage)
                cur.execute("INSERT INTO Players (FirstName, LastName, Age) VALUES (?, ?, ?);", (userfirstname, userlastname, int(userage)))
            elif userage == "":
                cur.execute("INSERT INTO Players (FirstName, LastName) VALUES (?, ?);", (userfirstname, userlastname))

            cur.execute("SELECT ID FROM Players ORDER BY ID DESC LIMIT 1")
            ownerid = str(cur.fetchall())
            disallowed_characters = "[(,)]"
            for character in disallowed_characters:
                ownerid = ownerid.replace(character, "")

        if type2 != "":
            cur.execute("""INSERT INTO Pokemon (Name, Type1, Type2, StatsTotal, HP, Attack, Defense, SpAtk, SpDef, Speed, Generation, Legendary, Cost, OwnerID) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (name, type1, type2, total, hp, attack, defense, spatk, spdef, speed, generation, legendary, cost, ownerid))
        elif type2 == "":
            cur.execute("""INSERT INTO Pokemon (Name, Type1, StatsTotal, HP, Attack, Defense, SpAtk, SpDef, Speed, Generation, Legendary, Cost, OwnerID) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (name, type1, total, hp, attack, defense, spatk, spdef, speed, generation, legendary, cost, ownerid)) 
    except:
        print("An error has occured, try again.\n")
        addPokemon()

    repeat()

def removeData():
    table = input("What table do you want to remove from? (Players or Pokemon) ")
    if table == "Players":
        playerID = input("What player do you want to remove? (ID) ")
        cur.execute("SELECT * FROM Players WHERE ID = " + playerID)
        data = str(cur.fetchall())
        disallowed_characters = "()"
        for character in disallowed_characters:
                data = data.replace(character, "")

        confirmation = input("Are you sure you want to remove " + data + " from the database? (Y|N) ").upper()
        if confirmation == "Y":
            cur.execute("DELETE FROM Players WHERE ID = " + playerID)
        elif confirmation == "N":
            navigation()
        else:
            raise Exception("Exception")

    elif table == "Pokemon":
        pokeID = input("What pokemon do you want to remove? (ID) ")
        cur.execute("SELECT * FROM Pokemon WHERE ID = " + pokeID)
        data = str(cur.fetchall())
        disallowed_characters = "()"
        for character in disallowed_characters:
                data = data.replace(character, "")

        confirmation = input("Are you sure you want to remove " + data + " from the database? (Y|N) ").upper()
        if confirmation == "Y":
            cur.execute("DELETE FROM Pokemon WHERE ID = " + pokeID)
        elif confirmation == "N":
            navigation()
        else:
            raise Exception("Exception")
    else:
        raise Exception("Exception")

    repeat()

def printPokemon():
    # Assigning variables to user input which can choose what to sort and wether to sort it ascending or descending
    sortby = input("""What do you want to sort by? (Be cautious of spelling and grammar)\nOptions: Pokemon.ID, Pokemon.Name, Pokemon.Type2, Pokemon.StatsTotal, Pokemon.HP, Pokemon.Attack, Pokemon.Defense, Pokemon.SpAtk, Pokemon.SpDef, Pokemon.Speed, Pokemon.Generation,\nPokemon.Legendary, Pokemon.Cost, Players.FirstName: """)
    order = input("Do you want to sort by ascending values or descending values? (ASC or DESC) ")
    # The variable containing the code that will join the tables into one select, and order it by whatever the user says
    printpokemon = """SELECT Pokemon.ID, Pokemon.Name, Pokemon.Type1, Pokemon.Type2, Pokemon.StatsTotal, Pokemon.HP, Pokemon.Attack, Pokemon.Defense, Pokemon.SpAtk,
                    Pokemon.SpDef, Pokemon.Speed, Pokemon.Generation, Pokemon.Legendary, Pokemon.Cost, Players.FirstName FROM Pokemon
                    INNER JOIN Players ON Pokemon.OwnerID = Players.ID
                    ORDER BY """ + str(sortby)

    if order == "ASC":
        printpokemon += " ASC"
        cur.execute(printpokemon)
    elif order == "DESC":
        printpokemon += " DESC"
        cur.execute(printpokemon)
    else:
        raise Exception("Problem")

    # Presenting it in a way that looks nice and more like a table without having to print it line by line
    headers = ["ID", "Name", "Type1", "Type2", "Total", "HP", "Atk", "Def", "SpAtk", "SpDef", "Speed", "Gen", "Legend", "Cost", "Owner"]
    print(tabulate.tabulate(cur.fetchall(), headers, tablefmt = 'simple'))

    repeat()

def searchDatabase():
    
    repeat()

def repeat():
    temp = input("Do you want to continue (Y|N) ").upper()
    if temp == "Y":
        navigation()
    elif temp == "N":
        pass
    else:
        raise Exception("Exception")

# createDB()

navigation()

con.commit()
con.close()
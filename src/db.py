import sqlite3

def getDBResult():
    connection = sqlite3.connect("gta.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gta (
            release_year INTEGER
            , release_name TEXT
            , city TEXT
            , UNIQUE(release_year, release_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS city (
            gta_city TEXT
            , real_city TEXT
            , UNIQUE(gta_city)
        )
    """)

    #populate gta games
    release_list = [
        (1997, "Grand Theft Auto", "state of New Guernsey"),
        (1999, "Grand Theft Auto 2", "Anywhere, USA"),
        (2001, "Grand Theft Auto 3", "Liberty City"),
        (2002, "Grand Theft Auto 4", "Vice City"),
        (2004, "Grand Theft Auto 5", "State of San Adreas"),
        (2008, "Grand Theft Auto 6", "Liberty City"),
        (2013, "Grand Theft Auto 7", "Los Santos")
    ]
    cursor.executemany("INSERT OR IGNORE INTO gta VALUES (?,?,?)", release_list)
    connection.commit()

    #populate cities
    cursor.execute("INSERT OR IGNORE INTO city VALUES (:g, :r)", {"g": "Liberty City", "r": "New York"})
    cursor.execute("INSERT OR IGNORE INTO city VALUES  (:g, :r)", {"g": "Los Santos", "r": "Los Angeles"})
    connection.commit()

    #print db rows
    print("print db rows")
    for row in cursor.execute("SELECT * FROM gta"):
        print(row)

    #print specific rows
    print("print specific rows")
    cursor.execute("SELECT * FROM gta WHERE city=:c", {"c": "Liberty City"})
    gta_search = cursor.fetchall()
    print(gta_search)
    
    #print city rows
    print("print city rows")
    cursor.execute("select * from city ")
    city_search = cursor.fetchall()
    print(city_search)
    
    #print real city new york gta games with sql
    print("print real city new york gta games")
    for row in cursor.execute("""
        select g.release_year 
            , g.release_name
            , g.city as "gta_city"
            , c.real_city as "real_city"
        from gta g
        join city c on c.gta_city = g.city
        where c.real_city = :r
    """, {"r": "New York"}):
        print(row)
    
    #print real city new york gta games with python
    print("print real city new york gta games with python")
    for i in gta_search:
        adjusted = [city_search[0][1] if value==city_search[0][0] else value for value in i]
        print(adjusted)

    connection.close()
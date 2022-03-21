import sqlite3

def createMovieDBifNotExists():
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Title (
            spi_code TEXT
            , title_type TEXT
            , year INTEGER
            , title_original TEXT
            , language_original TEXT
            , imdb_id TEXT
            , director TEXT
            , genre TEXT
            , cast TEXT
            , imdb_score REAL
            , editor_score REAL
            , duration_minutes INTEGER 
            , URL_webapp TEXT
            , URL_paywall TEXT
            , notes TEXT
            , isImdbSearched INTEGER
            , gotImdbDetails INTEGER
            , URL_imdb TEXT
        	, imdbLastUpdateDate TEXT
            , UNIQUE(spi_code)
        )
    """)
    connection.close()

def insertMovieIfNotExists(movies):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.executemany("INSERT OR IGNORE INTO Title VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", movies)
    connection.commit()

def updateMovie(title):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Title 
        SET
            title_type = :title_type
            , year = :year
            , title_original = :title_original
            , language_original = :language_original
            , imdb_id = :imdb_id
            , director = :director
            , genre = :genre
            , cast = :cast
            , imdb_score = :imdb_score
            , editor_score = :editor_score
            , duration_minutes = :duration_minutes
            , URL_webapp = :URL_webapp
            , URL_paywall = :URL_paywall
            , notes = :notes
            , isImdbSearched = :isImdbSearched
            , URL_imdb = :URL_imdb
            , gotImdbDetails = :gotImdbDetails
        	, imdbLastUpdateDate = :imdbLastUpdateDate
        WHERE
            spi_code = :spi_code
    """, {
        "spi_code": title.spi_code
        , "title_type": title.title_type
        , "year": title.year
        , "title_original": title.title_original
        , "language_original": title.language_original
        , "imdb_id": title.imdb_id
        , "director": title.director
        , "genre": title.genre
        , "cast": title.cast
        , "imdb_score": title.imdb_score
        , "editor_score": title.editor_score
        , "duration_minutes": title.duration_minutes
        , "URL_webapp": title.url_webapp
        , "URL_paywall": title.url_paywall
        , "notes": title.notes
        , "isImdbSearched": "1" if title.isImdbSearched == True else "0"
        , "gotImdbDetails": "1" if title.gotImdbDetails == True else "0"
        , "URL_imdb": str(title.url_imdb)
        , "imdbLastUpdateDate": str(title.imdbLastUpdate)
        }
    )
    connection.commit()

def getImdbSearchList():
    #print specific rows
    print("get all movies to search imdb basic info")
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Title WHERE isImdbSearched=0")
    imdbSearchMovies = cursor.fetchall()
    print(f"{str(len(imdbSearchMovies))} titles to search on imdb.")
    return(imdbSearchMovies)

### learning
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
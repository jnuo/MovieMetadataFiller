import sqlite3

def createMovieDBifNotExists():
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Title (
            spi_code TEXT
            , spi_identifiers TEXT
            , spi_title_type TEXT
            , spi_year INTEGER
            , spi_titles TEXT
            , spi_title_original TEXT
            , spi_description TEXT
            , spi_editorial_note TEXT
            , spi_fb_regions TEXT
            , spi_age TEXT
            , spi_series_title TEXT
            , spi_series_original_title TEXT
            , spi_series_season_title TEXT
            , spi_position TEXT
            , spi_publish_date TEXT
            , spi_release_date TEXT
            , spi_directors TEXT
            , spi_writer TEXT
            , spi_producer TEXT
            , spi_cast TEXT
            , spi_tags TEXT
            , spi_imdb_score REAL
            , spi_editors_score REAL
            , spi_duration_minutes INTEGER
            , spi_slug TEXT
            , spi_url_webapp TEXT
            , spi_url_paywall TEXT
            , notes TEXT
            , is_imdb_searched INTEGER
            , is_imdb_found INTEGER
            , got_imdb_details INTEGER
            , imdb_id TEXT
            , imdb_url TEXT
            , imdb_imdb_score REAL
            , imdb_genre TEXT
            , imdb_directors TEXT
            , imdb_cast TEXT
            , imdb_duration_minutes INTEGER
            , imdb_last_update_date TEXT
            , UNIQUE(spi_code)
        )
    """)
    connection.close()

def insertOrIgnoreTitle(movies):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT OR IGNORE INTO Title VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
    , movies)
    connection.commit()

def insertOrIgnoreTitle2(title):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    note = ""
    imdb_cast = imdb_directors = imdb_genre = imdb_url = imdb_id = ""
    imdb_imdb_score = 0
    imdb_duration = 0
    imdbLastUpdate = ""
    cursor.execute("""
        INSERT OR IGNORE INTO Title VALUES(
            :spi_code
            , :spi_identifiers
            , :spi_title_type
            , :spi_year
            , :spi_titles
            , :spi_title_original
            , :spi_description
            , :spi_editorial_note
            , :spi_fb_regions
            , :spi_age
            , :spi_series_title
            , :spi_series_original_title
            , :spi_series_season_title
            , :spi_position
            , :spi_publish_date
            , :spi_release_date
            , :spi_directors
            , :spi_writer
            , :spi_producer
            , :spi_cast
            , :spi_tags
            , :spi_imdb_score
            , :spi_editors_score
            , :spi_duration_minutes
            , :spi_slug
            , :spi_url_webapp
            , :spi_url_paywall
            , :notes
            , :is_imdb_searched
            , :is_imdb_found
            , :got_imdb_details
            , :imdb_id
            , :imdb_url
            , :imdb_imdb_score
            , :imdb_genre
            , :imdb_directors
            , :imdb_cast
            , :imdb_duration_minutes
            , :imdb_last_update_date
        )
    """, {
        "spi_code": title.spi_code
        , "spi_identifiers": title.spi_identifiers
        , "spi_title_type": title.spi_title_type
        , "spi_year": title.spi_year
        , "spi_titles": title.spi_titles
        , "spi_title_original": title.spi_title_original
        , "spi_description": title.spi_description
        , "spi_editorial_note": title.spi_editorial_note
        , "spi_fb_regions": title.spi_fb_regions
        , "spi_age": title.spi_age
        , "spi_series_title": title.spi_series_title
        , "spi_series_original_title": title.spi_series_original_title
        , "spi_series_season_title": title.spi_series_season_title
        , "spi_position": title.spi_position
        , "spi_publish_date": title.spi_publish_date
        , "spi_release_date": title.spi_release_date
        , "spi_directors": title.spi_directors
        , "spi_writer": title.spi_writer
        , "spi_producer": title.spi_producer
        , "spi_cast": title.spi_cast
        , "spi_tags": title.spi_tags
        , "spi_imdb_score": str(title.spi_imdb_score)
        , "spi_editors_score": str(title.spi_editors_score)
        , "spi_duration_minutes": str(title.spi_duration_minutes)
        , "spi_slug": title.spi_slug
        , "spi_url_webapp": title.spi_url_webapp
        , "spi_url_paywall": title.spi_url_paywall
        , "notes": note
        , "is_imdb_searched": "0"
        , "is_imdb_found": "0"
        , "got_imdb_details": "0"
        , "imdb_id": imdb_id
        , "imdb_url": imdb_url
        , "imdb_imdb_score": imdb_imdb_score
        , "imdb_genre": imdb_genre
        , "imdb_directors": imdb_directors
        , "imdb_cast": imdb_cast
        , "imdb_duration_minutes": imdb_duration
        , "imdb_last_update_date": imdbLastUpdate
        }
    )
    connection.commit()

def update_title_CMS_data(title):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Title 
        SET
            spi_identifiers = :spi_identifiers
            , spi_title_type = :spi_title_type
            , spi_year = :spi_year
            , spi_titles = :spi_titles
            , spi_title_original = :spi_title_original
            , spi_description = :spi_description
            , spi_editorial_note = :spi_editorial_note
            , spi_fb_regions = :spi_fb_regions
            , spi_age = :spi_age
            , spi_series_title = :spi_series_title
            , spi_series_original_title = :spi_series_original_title
            , spi_series_season_title = :spi_series_season_title
            , spi_position = :spi_position
            , spi_publish_date = :spi_publish_date
            , spi_release_date = :spi_release_date
            , spi_directors = :spi_directors
            , spi_writer = :spi_writer
            , spi_producer = :spi_producer
            , spi_cast = :spi_cast
            , spi_tags = :spi_tags
            , spi_imdb_score = :spi_imdb_score
            , spi_editors_score = :spi_editors_score
            , spi_duration_minutes = :spi_duration_minutes
            , spi_slug = :spi_slug
            , spi_url_webapp = :spi_url_webapp
            , spi_url_paywall = :spi_url_paywall
        WHERE
            spi_code = :spi_code
    """, {
        "spi_code": title.spi_code
        , "spi_identifiers": title.spi_identifiers
        , "spi_title_type": title.spi_title_type
        , "spi_year": title.spi_year
        , "spi_titles": title.spi_titles
        , "spi_title_original": title.spi_title_original
        , "spi_description": title.spi_description
        , "spi_editorial_note": title.spi_editorial_note
        , "spi_fb_regions": title.spi_fb_regions
        , "spi_age": title.spi_age
        , "spi_series_title": title.spi_series_title
        , "spi_series_original_title": title.spi_series_original_title
        , "spi_series_season_title": title.spi_series_season_title
        , "spi_position": title.spi_position
        , "spi_publish_date": title.spi_publish_date
        , "spi_release_date": title.spi_release_date
        , "spi_directors": title.spi_directors
        , "spi_writer": title.spi_writer
        , "spi_producer": title.spi_producer
        , "spi_cast": title.spi_cast
        , "spi_tags": title.spi_tags
        , "spi_imdb_score": title.spi_imdb_score
        , "spi_editors_score": title.spi_editors_score
        , "spi_duration_minutes": title.spi_duration_minutes
        , "spi_slug": title.spi_slug
        , "spi_url_webapp": title.spi_url_webapp
        , "spi_url_paywall": title.spi_url_paywall
        }
    )
    connection.commit()

def updateTitle(title):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Title 
        SET
            spi_identifiers = :spi_identifiers
            , spi_title_type = :spi_title_type
            , spi_year = :spi_year
            , spi_titles = :spi_titles
            , spi_title_original = :spi_title_original
            , spi_description = :spi_description
            , spi_editorial_note = :spi_editorial_note
            , spi_fb_regions = :spi_fb_regions
            , spi_age = :spi_age
            , spi_series_title = :spi_series_title
            , spi_series_original_title = :spi_series_original_title
            , spi_series_season_title = :spi_series_season_title
            , spi_position = :spi_position
            , spi_publish_date = :spi_publish_date
            , spi_release_date = :spi_release_date
            , spi_directors = :spi_directors
            , spi_writer = :spi_writer
            , spi_producer = :spi_producer
            , spi_cast = :spi_cast
            , spi_tags = :spi_tags
            , spi_imdb_score = :spi_imdb_score
            , spi_editors_score = :spi_editors_score
            , spi_duration_minutes = :spi_duration_minutes
            , spi_slug = :spi_slug
            , spi_url_webapp = :spi_url_webapp
            , spi_url_paywall = :spi_url_paywall
            , notes = :notes
            , is_imdb_searched = :is_imdb_searched
            , is_imdb_found = :is_imdb_found
            , got_imdb_details = :got_imdb_details
            , imdb_id = :imdb_id
            , imdb_url = :imdb_url
            , imdb_imdb_score = :imdb_imdb_score
            , imdb_genre = :imdb_genre
            , imdb_directors = :imdb_directors
            , imdb_cast = :imdb_cast
            , imdb_duration_minutes = :imdb_duration_minutes
            , imdb_last_update_date = :imdb_last_update_date
        WHERE
            spi_code = :spi_code
    """, {
        "spi_code": title.spi_code
        , "spi_identifiers": title.spi_identifiers
        , "spi_title_type": title.spi_title_type
        , "spi_year": title.spi_year
        , "spi_titles": title.spi_titles
        , "spi_title_original": title.spi_title_original
        , "spi_description": title.spi_description
        , "spi_editorial_note": title.spi_editorial_note
        , "spi_fb_regions": title.spi_fb_regions
        , "spi_age": title.spi_age
        , "spi_series_title": title.spi_series_title
        , "spi_series_original_title": title.spi_series_original_title
        , "spi_series_season_title": title.spi_series_season_title
        , "spi_position": title.spi_position
        , "spi_publish_date": title.spi_publish_date
        , "spi_release_date": title.spi_release_date
        , "spi_directors": title.spi_directors
        , "spi_writer": title.spi_writer
        , "spi_producer": title.spi_producer
        , "spi_cast": title.spi_cast
        , "spi_tags": title.spi_tags
        , "spi_imdb_score": title.spi_imdb_score
        , "spi_editors_score": title.spi_editors_score
        , "spi_duration_minutes": title.spi_duration_minutes
        , "spi_slug": title.spi_slug
        , "spi_url_webapp": title.spi_url_webapp
        , "spi_url_paywall": title.spi_url_paywall
        , "notes": title.notes
        , "is_imdb_searched": "1" if title.is_imdb_searched == True else "0"
        , "is_imdb_found": "1" if title.is_imdb_found == True else "0"
        , "got_imdb_details": "1" if title.got_imdb_details == True else "0"
        , "imdb_id": title.imdb_id
        , "imdb_url": title.imdb_url
        , "imdb_imdb_score": title.imdb_imdb_score
        , "imdb_genre": title.imdb_genre
        , "imdb_directors": title.imdb_directors
        , "imdb_cast": title.imdb_cast
        , "imdb_duration_minutes": title.imdb_duration_minutes
        , "imdb_last_update_date": title.imdb_last_update_date.isoformat()
        }
    )
    connection.commit()

def getImdbSearchList():
    #print specific rows
    print("get all movies to search imdb basic info")
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM Title
    """)
    imdbSearchMovies = cursor.fetchall()
    print(f"{str(len(imdbSearchMovies))} titles to search on imdb.")
    return(imdbSearchMovies)

def getTitleBySpiCode(spi_code):
    connection = sqlite3.connect("spi_movies.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM Title
        WHERE
            spi_code = :spi_code
    """, {
        "spi_code": spi_code
    })
    imdbSearchMovies = cursor.fetchall()
    return imdbSearchMovies

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
from contextlib import nullcontext
from datetime import datetime
from numpy import True_
import excel
import imdbpy as im
import time
import math
import db
import Models.Title as Title
from difflib import SequenceMatcher

# Target 1: checking the following information from IMDB, updating them on CMS.
#   1. IMDB Score
#   2. Genre
#   3. Directors
#   4. Cast
#   5. Duration

# Target 2: getting local title-name & synopsis text from content websites for each title, compare with ours, update if necessary.
#   1. Local title names
#   2. Local synopsis text

def insertSpiTitlesToDB():
    start_time = time.time()

    db.createMovieDBifNotExists()
    movies = excel.read_filmbox_movies()

    size = len(movies)
    bucket_size = 500
    buckets = math.ceil(size / bucket_size)
    print(f'size: {size} & buckets: {buckets}')

    for i in range(buckets):
        
        bucket_start_time = time.time()
        bucket_start_index = i * bucket_size
        print(f"bucket #{i} starting with item {bucket_start_index}")
        
        # create the bucket to work on
        bucket_end_index = bucket_start_index + bucket_size
        if bucket_start_index + bucket_size > size:
            bucket_end_index = size
        bucket_movies = movies[bucket_start_index:bucket_end_index]

        for j in range(bucket_size):
            currentItem = bucket_start_index + j
            if currentItem >= size:
                break
            
            movieStartTime = time.time()
            
            spi_code = ""
            try:
                spi_code = bucket_movies['SPICode*'][currentItem]
                if(spi_code.strip()==""):
                    continue
                else:
                    spi_code = spi_code.split("_")[0]
                    spi_code = spi_code.split("-")[0]
            except:
                print("Movie #" + str(currentItem) + " executed in %.2f seconds but SPI Code is empty." % (time.time() - movieStartTime))
                note = "SPI Code is empty."
                continue
            
            titleType = "Movie" if spi_code.startswith("SPI") else "Series"
            year = 0 if bucket_movies['ReleaseDate*'][currentItem] == "" else int(bucket_movies['ReleaseDate*'][currentItem][0:4])
            title_original = bucket_movies['EnglishTitle*'][currentItem]
            director = bucket_movies['Director'][currentItem]
            writer = bucket_movies['Writer'][currentItem]
            producer = bucket_movies['Producer'][currentItem]
            genre = bucket_movies['Tags*'][currentItem]
            actor = bucket_movies['Actor'][currentItem]
            spiImdbScore = bucket_movies['ImdbScore'][currentItem]
            spiEditorsScore = bucket_movies['EditorScore'][currentItem]
            url_webapp = bucket_movies['Webapp URL'][currentItem]
            url_paywall = bucket_movies['Paywall URL'][currentItem]
            d = bucket_movies['Duration*'][currentItem].split(":")
            duration_minutes = int(d[0])*60 + int(d[1])
            spi_slug = bucket_movies['Content Slug'][currentItem]
            note = ""
            isImdbSearched = 0
            isImdbFound = 0
            gotImdbDetails = 0
            imdb_cast = imdb_directors = imdb_genre = imdb_url = imdb_id = ""
            imdb_imdb_score = 0
            imdb_duration = 0
            imdbLastUpdate = ""
            
            if title_original == "":
                print("Movie #" + str(currentItem) + " executed in %.2f seconds but Title is empty." % (time.time() - movieStartTime))
                note = "Title is empty."
                continue
            
            # insert movie with CMS data to the db
            movie = [
                (spi_code
                    , bucket_movies['Identifier*'][currentItem]
                    , titleType
                    , year
                    , ""
                    , title_original
                    , "",  "", "", "",  "", "", "",  "", "", ""
                    , director, writer, producer
                    , actor
                    , genre
                    , spiImdbScore
                    , spiEditorsScore
                    , duration_minutes
                    , spi_slug
                    , url_webapp, url_paywall
                    , note
                    , isImdbSearched, isImdbFound, gotImdbDetails
                    , imdb_id, imdb_url, imdb_imdb_score, imdb_genre, imdb_directors, imdb_cast, imdb_duration
                    , imdbLastUpdate)
            ]
            db.insertOrIgnoreTitle(movie)
            print(f"Movie # {str(currentItem)} executed in %.2f seconds" % (time.time() - movieStartTime))

        print(f"bucket #{i} for {bucket_size} has ended in %.2f seconds." % (time.time() - bucket_start_time))

    print("Total execution time --- %.2f minutes ---" % ((time.time() - start_time)/60))

def getImdbInfo():
    start_time = time.time()
    titles = getTitlesFromDBRows(db.getImdbSearchList())
    print(f'getImdbInfo() starts for {str(len(titles))} titles.')
    
    for t in titles:
        movie_search_start_time = time.time()
        imdbSearchResults = []
        try:
            imdbSearchResults = im.searchMovie(t.spi_title_original)
        except:
            print("searchMovie() throws exception for : " + t.spi_title_original)
        
        t.is_imdb_searched = True

        if len(imdbSearchResults)==0:
            t.notes += "Title not found on IMDB."
        
        t.is_imdb_found = False

        for imdbResult in imdbSearchResults:
            nameSimilarityRatio = SequenceMatcher(None, imdbResult["title"].lower(), t.spi_title_original.lower()).ratio()
            #print("imdbResult[title]: " + imdbResult["title"] + "\t t.spi_title_original: " + t.spi_title_original + "\t ratio: " + str(nameSimilarityRatio))
            if nameSimilarityRatio <= 0.8:
                continue
            
            # 1. get movie details
            imdbId = imdbResult.getID()
            imdbMovieDetails = im.getMovie(imdbId)
            imdbUrl = im.getMovieURL(imdbResult)

            # 2. compare year, name, director
            try:
                t.imdb_imdb_score = imdbMovieDetails['rating']
            except:
                continue
            if t.spi_year != imdbMovieDetails["year"]:
                continue
            try:
                directorSimilarityRatio = SequenceMatcher(None, imdbMovieDetails["directors"][0]["name"].lower(), t.spi_directors.split(",")[0].lower()).ratio()
                if directorSimilarityRatio <= 0.8:
                    continue
            except:
                continue
            
            # horray, found the movie!
            t.is_imdb_found = True
            t.got_imdb_details = True
            t.imdb_id = imdbId
            t.imdb_url = imdbUrl

            # 3. when found -> update imdb information of Title in the DB
            # IMBD Rating
            try:
                t.imdb_imdb_score = imdbMovieDetails['rating']
            except:
                t.imdb_imdb_score = 0
                t.notes += "IMDB Rating is missing. "
            
            # IMDB Genre
            try:
                genresStr = ', '.join(map(str, imdbMovieDetails['genres']))
                t.imdb_genre = genresStr
            except:
                t.imdb_genre = ""
                t.notes += "IMDB genre info is missing. "
            
            # IMDB Directors
            try:
                t.imdb_directors = ', '.join(map(str, imdbMovieDetails['directors']))
            except:
                t.imdb_directors = ""
                t.notes += "IMDB director info is missing. "
            
            # IMDB Cast
            try:
                imdbCastArray = imdbMovieDetails['cast']
                imdbCastStrArray = []
                for imdbCastInfo in imdbCastArray:
                    ic = imdbCastInfo['name']
                    imdbCastStrArray.append(ic)
                imdbCast = ', '.join(map(str, imdbCastStrArray))
                t.imdb_cast = imdbCast
            except:
                t.imdb_cast = ""
                t.notes += "IMDB cast info is missing. "

            # IMDB Duration
            # get imdb duration and save it
            break
        
        if not(t.is_imdb_found):
            t.note = "Movie NOT FOUND on IMDB."

        t.imdb_last_update_date = datetime.now()
        db.updateTitle(t)
        print(f'Searching for movie {t.spi_code} on IMDB takes %.2f seconds.' % (time.time() - movie_search_start_time))
    print(f'getBasicImdbInfo() total execution time --- %.2f minutes & %s results ---' % ((time.time() - start_time)/60, str(len(titles))))

def getTitlesFromDBRows(dbTitles):
    titles = []
    for row in dbTitles:
        title = Title.Title(row[0])
        title.spi_identifiers = row[1]
        title.spi_title_type = row[2]
        title.spi_year = int(row[3])
        title.spi_titles = row[4]
        title.spi_title_original = row[5]
        title.spi_description = row[6]
        title.spi_editorial_note = row[7]
        title.spi_fb_regions = row[8]
        title.spi_age = row[9]
        title.spi_series_title = row[10]
        title.spi_series_original_title = row[11]
        title.spi_series_season_title = row[12]
        title.spi_position = row[13]
        title.spi_publish_date = row[14]
        title.spi_release_date = row[15]
        title.spi_directors = row[16]
        title.spi_writer = row[17]
        title.spi_producer = row[18]
        title.spi_cast = row[19]
        title.spi_tags = row[20]
        title.spi_imdb_score = 0 if str(row[21])=='None' else float(row[21])
        title.spi_editors_score = 0 if str(row[22])=='None' else float(row[22])
        title.spi_duration_minutes = int(row[23])
        title.spi_slug = row[24]
        title.spi_url_webapp = row[25]
        title.spi_url_paywall = row[26]
        title.notes = row[27]
        title.is_imdb_searched = bool(row[28])
        title.is_imdb_found = bool(row[29])
        title.got_imdb_details = bool(row[30])
        title.imdb_id = row[31]
        title.imdb_url = row[32]
        title.imdb_imdb_score = row[33]
        title.imdb_genre = row[34]
        title.imdb_directors = row[35]
        title.imdb_cast = row[36]
        title.imdb_duration_minutes = int(row[37])
        title.imdb_last_update_date = nullcontext if row[38] == "" else datetime.strptime(row[38])
        
        titles.append(title)

    return titles
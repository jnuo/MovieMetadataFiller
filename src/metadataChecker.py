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
            title = bucket_movies['EnglishTitle*'][currentItem]
            director = bucket_movies['Director'][currentItem]
            genre = bucket_movies['Tags*'][currentItem]
            actor = bucket_movies['Actor'][currentItem]
            url_webapp = bucket_movies['Webapp URL'][currentItem]
            url_paywall = bucket_movies['Paywall URL'][currentItem]
            note = ""
            isImdbSearched = 0
            gotImdbDetails = 0
            imdbLastUpdate = ""
            
            if title == "":
                print("Movie #" + str(currentItem) + " executed in %.2f seconds but Title is empty." % (time.time() - movieStartTime))
                note = "Title is empty."
                continue
            
            # insert movie with CMS data to the db
            movie = [
                (spi_code, titleType, year, title, "", "", director, genre
                , actor, 0, 0, 0, url_webapp, url_paywall, note, isImdbSearched, gotImdbDetails, imdbLastUpdate)
            ]
            db.insertMovieIfNotExists(movie)
            print(f"Movie # {str(currentItem)} executed in %.2f seconds" % (time.time() - movieStartTime))

        print(f"bucket #{i} for {bucket_size} has ended in %.2f seconds." % (time.time() - bucket_start_time))

    print("Total execution time --- %.2f minutes ---" % ((time.time() - start_time)/60))

def getBasicImdbInfo():
    start_time = time.time()
    titles = getTitlesFromDBRows(db.getImdbSearchList())
    print(f'getBasicImdbInfo() starts for {str(len(titles))} titles.')
    
    for t in titles:
        imdbSearchResults = im.searchMovie(t.title_original)

        if len(imdbSearchResults)==0:
            t.notes += "Title not found on IMDB."
        
        #imdbSimilarNameResults = filter() imdbSearchResults.where()
        imdbSimilarNameResults = [x for x in imdbSearchResults if SequenceMatcher(None, x["title"], t.title_original).ratio() >= 0.8]

        for imdbResult in imdbSearchResults:
            nameSimilarityRatio = SequenceMatcher(None, imdbResult["title"].lower(), t.title_original.lower()).ratio()
            print("imdbResult[title]: " + imdbResult["title"] + "\t t.title_original: " + t.title_original + "\t ratio: " + str(nameSimilarityRatio))
            if nameSimilarityRatio <= 0.8:
                continue
            
            # 1. get movie details
            imdbId = imdbResult.getID()
            imdbMovieDetails = im.getMovie(imdbId)
            imdbUrl = im.getMovieURL(imdbResult)

            # 2. compare year, name, director
            if t.year != imdbMovieDetails["year"]:
                continue
            directorSimilarityRatio = SequenceMatcher(None, imdbMovieDetails["directors"][0]["name"].lower(), t.director.split(",")[0].lower()).ratio()
            if directorSimilarityRatio <= 0.8:
                continue
            
            # 3. if same -> add new row as imdbTitle table & save
            imdbDirector = imdbMovieDetails['directors'][0]['name']
            imdbDirectorStr = ', '.join(map(str, imdbMovieDetails['directors']))
            
            t.language_original = ""
            t.imdb_id = imdbId
            t.director = ""
            t.genre = ""
            t.cast = ""
            t.imdb_score = imdbMovieDetails["imdb_score"]
            t.duration_minutes = ""
            t.notes = ""
            t.isImdbSearched = True
            t.gotImdbDetails = True
            t.imdb_url = imdbUrl
            t.imdbLastUpdate = time.time()
            db.updateMovie(t)
            break
        
    print("getBasicImdbInfo() total execution time --- %.2f minutes & %s results ---" % ((time.time() - start_time)/60, str(len(titles))))

def getTitlesFromDBRows(dbTitles):
    titles = []
    for row in dbTitles:
        title = Title.Title(row[0])
        title.year = int(row[2])
        title.title_original = row[3]
        title.language_original = row[4]
        title.imdb_id = row[5]
        title.director = row[6]
        title.genre = row[7]
        title.cast = row[8]
        title.imdb_score = float(row[9])
        title.editor_score = float(row[10])
        title.duration_minutes = int(row[11])
        title.url_webapp = row[12]
        title.url_paywall = row[13]
        title.notes = row[14]
        title.isImdbSearched = bool(row[15])
        title.gotImdbDetails = bool(row[16])
        title.imdbLastUpdate = nullcontext if row[17] == "" else datetime.strptime(row[17])
        titles.append(title)
    return titles
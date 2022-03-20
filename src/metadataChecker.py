from numpy import True_
import excel
import imdbpy as im
import time
import math
import db

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
            print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
            note = "SPI Code is empty."
            continue
        
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
            print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
            note = "Title is empty."
            continue
        
        # insert movie with CMS data to the db
        movie = [
            (spi_code, "Movie", year, title, "", "", director, genre
            , actor, 0, 0, 0, url_webapp, url_paywall, note, isImdbSearched, gotImdbDetails, imdbLastUpdate)
        ]
        db.insertMovieIfNotExists(movie)

        # try:
        #     imdbSearchResults = im.searchMovie(title)
        # except:
        #     print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
        #     note = "Exception on finding on IMDB."
        #     continue

        # if len(imdbSearchResults)==0:
        #     print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
        #     note = "Not found on IMDB."
        #     continue

        found = False

        # for imdbResult in imdbSearchResults:
        #     try:
        #         imdbId = imdbResult.getID()
        #         imdbMovieDetails = im.getMovie(imdbId)
        #         imdbUrl = im.getMovieURL(imdbResult)
        #     except:
        #         continue  
            
        #     try: 
        #         imdbTitle = imdbMovieDetails['title']
        #     except: 
        #         continue
            
        #     try:
        #         imdbYear = imdbMovieDetails['year']
        #     except:
        #         imdbYear = ""
            
        #     try:
        #         imdbDirector = imdbMovieDetails['directors'][0]['name']
        #         imdbDirectorStr = ', '.join(map(str, imdbMovieDetails['directors']))
        #     except:
        #         imdbDirector = ""
        #         imdbDirectorStr = ""
            
        #     if "movie" in imdbResult['kind'] and (imdbDirector == director or director in imdbDirectorStr) and year[0:4] == str(imdbYear):
        #         try:
        #             imdbRating = imdbMovieDetails['rating']
        #         except:
        #             imdbRating = ""
        #         try:
        #             imdbSynopsis = imdbMovieDetails['synopsis'][0]
        #         except:
        #             imdbSynopsis = ""
        #         try:
        #             imdbPlotOutline = imdbMovieDetails['plot outline'][0]
        #         except:
        #             imdbPlotOutline = ""
        #         try:
        #             imdbCastArray = imdbMovieDetails['cast']
        #             imdbCastStrArray = []
        #             for imdbCastInfo in imdbCastArray:
        #                 ic = imdbCastInfo['name']
        #                 imdbCastStrArray.append(ic)
        #             imdbCast = ', '.join(map(str, imdbCastStrArray))
        #         except:
        #             imdbCast = ""
        #         try:
        #             imdbCountryCodes = ', '.join(map(str, imdbMovieDetails['country codes']))
        #         except:
        #             imdbCountryCodes = ""
        #         try:
        #             imdbLanguageCodes = ', '.join(map(str, imdbMovieDetails['language codes']))
        #         except:
        #             imdbLanguageCodes = ""
        #         try:
        #             imdbRuntimes = ', '.join(map(str, imdbMovieDetails['runtimes']))
        #         except:
        #             imdbRuntimes = ""
        #         try:
        #             imdbColors = ', '.join(map(str, imdbMovieDetails['color info']))
        #         except:
        #             imdbColors = ""
        #         try:
        #             genresStr = ', '.join(map(str, imdbMovieDetails['genres']))
        #             imdbGenre = genresStr
        #         except:
        #             imdbGenre = ""
        #         found = True
        #         break
        print(f"Movie # {str(currentItem)} executed in {time.time() - movieStartTime} seconds and was found = {found}")
    print(f"bucket #{i} for {bucket_size} has ended in {time.time() - bucket_start_time} seconds.")

print("Total execution time --- %s minutes ---" % ((time.time() - start_time)/60))

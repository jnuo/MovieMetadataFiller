from numpy import True_
import excel
#import request_operations as ro
#import scrapeImdb as si
import imdbpy as im
import time
import math

start_time = time.time()

movies = excel.read_filmbox_movies()
#movies = movies[:3]

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
    
    imdbScores = []
    imdbGenres = []
    imdbURLs = []
    imdbSynopsises = []
    imdbDirectors = []
    imdbPlotOutlines = []
    imdbCasts = []
    imdbCountryCodesList = []
    imdbLanguageCodesList = []
    imdbRuntimesList = []
    imdbColorsList = []

    for j in range(bucket_size):
        currentItem = bucket_start_index + j
        if currentItem >= size:
            break
        
        movieStartTime = time.time()
        imdbScore = imdbGenre = imdbURL = imdbSynopsis = imdbDirector = imdbPlotOutline = ""
        
        title = bucket_movies['EnglishTitle*'][currentItem]
        director = bucket_movies['Director'][currentItem]
        year = bucket_movies['ReleaseDate*'][currentItem]
        
        if title == "":
            imdbScores.append("")
            imdbGenres.append("")
            imdbURLs.append("")
            imdbSynopsises.append("")
            imdbDirectors.append("")
            imdbPlotOutlines.append("")
            imdbCasts.append("")
            imdbCountryCodesList.append("")
            imdbLanguageCodesList.append("")
            imdbRuntimesList.append("")
            imdbColorsList.append("")
            print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
            continue
        
        try:
            imdbSearchResults = im.searchMovie(title)
        except:
            imdbScores.append("")
            imdbGenres.append("")
            imdbURLs.append("")
            imdbSynopsises.append("")
            imdbDirectors.append("")
            imdbPlotOutlines.append("")
            imdbCasts.append("")
            imdbCountryCodesList.append("")
            imdbLanguageCodesList.append("")
            imdbRuntimesList.append("")
            imdbColorsList.append("")
            print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
            continue

        if len(imdbSearchResults)==0:
            imdbScores.append("")
            imdbGenres.append("")
            imdbURLs.append("")
            imdbSynopsises.append("")
            imdbDirectors.append("")
            imdbPlotOutlines.append("")
            imdbCasts.append("")
            imdbCountryCodesList.append("")
            imdbLanguageCodesList.append("")
            imdbRuntimesList.append("")
            imdbColorsList.append("")
            print("Movie #" + str(currentItem) + " executed in %s seconds and was not found." % (time.time() - movieStartTime))
            continue

        found = False

        for imdbResult in imdbSearchResults:
            try:
                imdbId = imdbResult.getID()
                imdbMovieDetails = im.getMovie(imdbId)
                imdbUrl = im.getMovieURL(imdbResult)
            except:
                continue
            
            try: 
                imdbTitle = imdbMovieDetails['title']
            except: 
                continue
            try:
                imdbYear = imdbMovieDetails['year']
            except:
                imdbYear = ""
            try:
                imdbDirector = imdbMovieDetails['directors'][0]['name']
                imdbDirectorStr = ', '.join(map(str, imdbMovieDetails['directors']))
            except:
                imdbDirector = ""
                imdbDirectorStr = ""
            
            if "movie" in imdbResult['kind'] and (imdbDirector == director or director in imdbDirectorStr) and year[0:4] == str(imdbYear):
                try:
                    imdbRating = imdbMovieDetails['rating']
                except:
                    imdbRating = ""
                try:
                    imdbSynopsis = imdbMovieDetails['synopsis'][0]
                except:
                    imdbSynopsis = ""
                try:
                    imdbPlotOutline = imdbMovieDetails['plot outline'][0]
                except:
                    imdbPlotOutline = ""
                try:
                    imdbCastArray = imdbMovieDetails['cast']
                    imdbCastStrArray = []
                    for imdbCastInfo in imdbCastArray:
                        ic = imdbCastInfo['name']
                        imdbCastStrArray.append(ic)
                    imdbCast = ', '.join(map(str, imdbCastStrArray))
                except:
                    imdbCast = ""
                try:
                    imdbCountryCodes = ', '.join(map(str, imdbMovieDetails['country codes']))
                except:
                    imdbCountryCodes = ""
                try:
                    imdbLanguageCodes = ', '.join(map(str, imdbMovieDetails['language codes']))
                except:
                    imdbLanguageCodes = ""
                try:
                    imdbRuntimes = ', '.join(map(str, imdbMovieDetails['runtimes']))
                except:
                    imdbRuntimes = ""
                try:
                    imdbColors = ', '.join(map(str, imdbMovieDetails['color info']))
                except:
                    imdbColors = ""
                try:
                    genresStr = ', '.join(map(str, imdbMovieDetails['genres']))
                    imdbGenre = genresStr
                except:
                    imdbGenre = ""            
                
                imdbScores.append(imdbRating)
                imdbGenres.append(imdbGenre)
                imdbURLs.append(imdbUrl)
                imdbSynopsises.append(imdbSynopsis)
                imdbDirectors.append(imdbDirectorStr)
                imdbPlotOutlines.append(imdbPlotOutline)
                imdbCasts.append(imdbCast)
                imdbCountryCodesList.append(imdbCountryCodes)
                imdbLanguageCodesList.append(imdbLanguageCodes)
                imdbRuntimesList.append(imdbRuntimes)
                imdbColorsList.append(imdbColors)
                
                found = True
                break

        # if FilmBox+ Movie is not found in IMDB, then we add empty values to the arrays
        if found == False:
            imdbScores.append("")
            imdbGenres.append("")
            imdbURLs.append("")
            imdbSynopsises.append("")
            imdbDirectors.append("")
            imdbPlotOutlines.append("")
            imdbCasts.append("")
            imdbCountryCodesList.append("")
            imdbLanguageCodesList.append("")
            imdbRuntimesList.append("")
            imdbColorsList.append("")    
        print(f"Movie # {str(currentItem)} executed in {time.time() - movieStartTime} seconds and was found = {found}")

    print(f"bucket #{i} for {bucket_size} has ended in {time.time() - bucket_start_time} seconds.")
    bucket_movies['imdbScores'] = imdbScores
    bucket_movies['imdbGenres'] = imdbGenres
    bucket_movies['imdbUrls'] = imdbURLs
    bucket_movies['imdbSynopsis'] = imdbSynopsises
    bucket_movies['imdbDirectors'] = imdbDirectors
    bucket_movies['imdbPlotOutlines'] = imdbPlotOutlines
    bucket_movies['imdbCasts'] = imdbCasts
    bucket_movies['imdbCountryCodes'] = imdbCountryCodesList
    bucket_movies['imdbLanguageCodes'] = imdbLanguageCodesList
    bucket_movies['imdbRuntimes'] = imdbRuntimes
    bucket_movies['imdbColors'] = imdbColorsList
            
    sheet_name = f"sheet{i}"
    excel.write_movies_to_excel_in_buffers(bucket_movies, sheet_name)

print("Total execution time --- %s minutes ---" % (time.time() - start_time))

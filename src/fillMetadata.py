from numpy import True_
import excel
import request_operations as ro
import scrapeImdb as si
import imdbpy as im
import time


start_time = time.time()

movies = excel.read_filmbox_movies()

imdbScores = []
imdbGenres = []
imdbURLs = []

for i in range(len(movies)):
    movieStartTime = time.time()
    imdbScore = imdbGenre = imdbURL = ""
    
    title = movies['EnglishTitle*'][i]
    if title == "":
        imdbScores.append("")
        imdbGenres.append("")
        imdbURLs.append("")
        print("Movie #" + str(i) + "   executed in %s seconds ---" % (time.time() - movieStartTime))
        continue
    
    director = movies['Director'][i]

    imdbSearchResults = im.searchMovie(title)
    if len(imdbSearchResults)==0:
        imdbScores.append("")
        imdbGenres.append("")
        imdbURLs.append("")
        print("Movie #" + str(i) + "   executed in %s seconds ---" % (time.time() - movieStartTime))
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
            imdbRating = imdbMovieDetails['rating']
        except:
            imdbRating = ""
        try:
            imdbDirector = imdbMovieDetails['directors'][0]['name']
        except:
            imdbDirector = ""     
        try:
            genresStr = ', '.join(map(str, imdbMovieDetails['genres']))
            imdbGenre = genresStr
        except:
            imdbGenre = ""
        
        if "movie" in imdbResult['kind'] and imdbDirector == director:
            imdbScores.append(imdbRating)
            imdbGenres.append(imdbGenre)
            imdbURLs.append(imdbUrl)
            found = True
            break

    # if FilmBox+ Movie is not found in IMDB, then we add empty values to the arrays
    if found == False:
        imdbScores.append("")
        imdbGenres.append("")
        imdbURLs.append("")
    
    print("Movie #" + str(i) + "   executed in %s seconds ---" % (time.time() - movieStartTime))

movies['imdbScores'] = imdbScores
movies['imdbGenres'] = imdbGenres
movies['imdbUrls'] = imdbURLs

excel.write_movies_to_excel(movies)
print("Total executuib time --- %s minutes ---" % (time.time() - start_time/60))

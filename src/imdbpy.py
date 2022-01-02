import imdb 

def searchMovie(movieName):
    im = imdb.IMDb()
    movies = im.search_movie(movieName)
    return movies 

def getMovie(id):
    im = imdb.IMDb()
    movie = im.get_movie(id)
    return movie
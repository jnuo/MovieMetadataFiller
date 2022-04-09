import imdb 

def searchMovie(movieName):
    im = imdb.IMDb()
    movies = im.search_movie(movieName)
    return movies 

def getMovie(id):
    im = imdb.IMDb()
    movie = im.get_movie(id)
    return movie

def getMovieURL(movie):
    im = imdb.IMDb()
    url = im.get_imdbURL(movie)
    return url

def getMovieParentsGuide(imdbId):
    im = imdb.IMDb()
    sth = im.get_movie_parents_guide(imdbId)
    return sth
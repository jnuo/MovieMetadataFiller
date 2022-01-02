import excel
import request_operations as ro
import scrapeImdb as si
import imdbpy as im

####
## Venv
####
# Create Virtual Environment        >python3 -m venv .venv
# Activate Virtual Environment      >source .venv/bin/activate
# Install a package into the Env    >python3 -m pip install openpyxl
# De-activate Virtual Environment   >deactivate

####
## git commands
####
# git init
# git status
# git add 'filename'
# git commit 'filename'
# git push

ro.time_to_first_byte()

#tenet_url = "https://www.imdb.com/title/tt6723592/"
#m = si.getMovieScore(tenet_url)
#print("IMDB score for the URL is " + m)

#movieName = input("Enter movie name to search: ")
#movieName = "The Matrix"
#movies = im.searchMovie(movieName)
#for movie in movies:
#    title = movie['title']
#    year = movie['year']
#    kind = movie['kind']
#    print(f'Basic movie info from search: {kind} - {title} - {year}')
#    id = movie.getID()
#    movieDetails = im.getMovie(id)
#    title2 = movieDetails['title']
#    year2 = movieDetails['year']
#    rating = movieDetails['rating']
#    directors = movieDetails['directors']
#    casting = movieDetails['cast']
#    direcStr = ' '.join(map(str, directors))
#    print(f'Movie Detail info from getMovie: {title2} - {year2} - {direcStr} - {rating}')


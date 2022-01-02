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

#kariyer_jobads = excel.read_kariyer_jobads()
#f3 = kariyer_jobads[:3]
#print(f3)

#ro.time_to_first_byte()

#tenet_url = "https://www.imdb.com/title/tt6723592/"
#m = si.getMovieScore(tenet_url)
#print("IMDB score for the URL is " + m)

#movieName = input("Enter movie name to search: ")
# movieName = "The Matrix"
# movies = im.searchMovie(movieName)
# for movie in movies:
#     title = movie['title']
#     year = movie['year']
#     kind = movie['kind']
#     print(f'Basic movie info from search: {kind} - {title} - {year}')
    
#     id = movie.getID()
#     movieDetails = im.getMovie(id)
#     title2 = movieDetails['title']
#     year2 = movieDetails['year']
#     rating = movieDetails['rating']
#     directors = movieDetails['directors']
#     casting = movieDetails['cast']
#     direcStr = ' '.join(map(str, directors))
#     print(f'Movie Detail info from getMovie: {title2} - {year2} - {direcStr} - {rating}')

movies = filmboxMovies = excel.read_filmbox_movies()
#print(movies)
# for i in range(3):
#     id = movies['SPICode*'][i]
#     title = movies['EnglishTitle*'][i]
#     director = movies['Director'][i]
#     imdbScore = movies['ImdbScore'][i]
    #print(f'SPI Code: {id}, title: {title}, director: {director} & IMDB Score: {imdbScore} & Onur Score: {onurScore}')

movies = movies[:3]
onurScores = [5,6,7]
movies['onurScore'] = onurScores
print(movies)

excel.write_movies_to_excel(movies)
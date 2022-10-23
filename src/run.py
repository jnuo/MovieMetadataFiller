import request_operations as ro
import metadataChecker as meta
import translationChecker as tc

# translation thing
tc.checkForChangedTranslation()

#metadata thing
# 1. Create DB, parse excel, store in DB
#meta.insertSpiTitlesToDB()

# 2. Search for all movies on IMDB, store in DB
#meta.getImdbInfo()

# 3. Create the new excel with difference data & REPORT CHANGE
#meta.createCMSExcel()

# 4. upload to CMS & be happy about it
# ok :)

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
# git pull

##
# to get original file and overwrite local changes
##
#git fetch
#git checkout origin/master <filepath>


####
## datetime -> string & vice
####
# my_date_string = datetime.datetime.utcnow().isoformat()
# my_date = datetime.datetime.fromisoformat(my_date_string)
# print(my_date)


#ro.time_to_first_byte()

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

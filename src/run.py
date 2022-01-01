import excel
import request_operations as ro
import scrapeImdb as im

# Create Virtual Environment        >python3 -m venv .venv
# Activate Virtual Environment      >source .venv/bin/activate
# Install a package into the Env    >python3 -m pip install openpyxl
# De-activate Virtual Environment   >deactivate

# git init
# git status
# git add 'filename'
# git commit 'filename'
# git push

#msg = "hola mundo"
#print(msg)

#kariyer_jobads = excel.read_kariyer_jobads()
#f3 = kariyer_jobads[:3]
#print(f3)

#ro.time_to_first_byte()


tenet_url = "https://www.imdb.com/title/tt6723592/"
m = im.getMovieScore(tenet_url)
print(m)

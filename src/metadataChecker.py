from datetime import datetime
from datetime import date
from numpy import True_
import excel
import imdbpy as im
import time
import math
import db
import Models.Title as Title
from difflib import SequenceMatcher

# Target 1: checking the following information from IMDB, updating them on CMS.
#   1. IMDB Score - ok
#   2. Genre - ok
#   3. Directors - ok
#   4. Cast - ok
#   5. Duration
#   6. Age Rating for all Countries

# Target 2: getting local title-name & synopsis text from content websites for each title, compare with ours, update if necessary.
#   1. Local title names
#   2. Local synopsis text

# Task1: CMS Excel data insert to DB
def insertSpiTitlesToDB():
    print(f'insertSpiTitlesToDB_2 begins')
    start_time = time.time()

    db.createMovieDBifNotExists()
    titles = excel.read_filmbox_titles()
    print(f'insertSpiTitlesToDB_2 movies size: {len(titles)}.')

    for t in titles:
        movieStartTime = time.time()
        db.insertOrIgnoreTitle2(t)
        db.update_title_CMS_data(t)
        print(f"insertSpiTitlesToDB_2: Movie # {t.spi_code} executed in %.2f seconds" % (time.time() - movieStartTime))
    
    print(f"insertSpiTitlesToDB_2 Total Time: %.2f seconds" % (time.time() - start_time))

# Task2: Find Movies on IMDB, get their data into the DB
def getImdbInfo():
    print(f'getImdbInfo() starts.')
    start_time = time.time()
    imdbSearchList = db.getImdbSearchList()
    titles = getTitlesFromDBRows(imdbSearchList)
    titles_to_search_on_imdb = [] 
    #= filter(lambda title: date(datetime.now()) - date(title.imdb_last_update_date) > 30)
    for t in titles:
        if t.imdb_last_update_date == None:
            titles_to_search_on_imdb.append(t)
        elif (date.today() - t.imdb_last_update_date.date()).days > 1:
            titles_to_search_on_imdb.append(t)

    print(f'getImdbInfo() starts for {str(len(titles_to_search_on_imdb))} titles.')
    
    for t in titles_to_search_on_imdb:
        movie_search_start_time = time.time()
        imdbSearchResults = []
        try:
            imdbSearchResults = im.searchMovie(t.spi_title_original)
        except:
            t.notes += "im.searchMovie() exception. "
            print("searchMovie() throws exception for : " + t.spi_title_original)
        
        t.is_imdb_searched = True

        if len(imdbSearchResults)==0:
            t.notes += "Title not found on IMDB."
        
        t.is_imdb_found = False

        for imdbResult in imdbSearchResults:
            nameSimilarityRatio = SequenceMatcher(None, imdbResult["title"].lower(), t.spi_title_original.lower()).ratio()
            #print("imdbResult[title]: " + imdbResult["title"] + "\t t.spi_title_original: " + t.spi_title_original + "\t ratio: " + str(nameSimilarityRatio))
            if nameSimilarityRatio <= 0.8:
                continue
            
            # 1. get movie details
            imdbId = imdbResult.getID()
            imdbMovieDetails = im.getMovie(imdbId)
            imdbUrl = im.getMovieURL(imdbResult)

            # 2. compare year, name, director
            try:
                t.imdb_imdb_score = imdbMovieDetails['rating']
                if t.spi_year != imdbMovieDetails["year"]:
                    #t.notes += "Compare with imdb result: YEAR problem. "
                    continue
                directorSimilarityRatio = SequenceMatcher(None, imdbMovieDetails["directors"][0]["name"].lower(), t.spi_directors.split(",")[0].lower()).ratio()
                if directorSimilarityRatio <= 0.8:
                    #t.notes += "Compare with imdb result: DIRECTOR problem. "
                    continue
            except:
                #t.notes += "Compare with imdb result throws exception. "
                continue
            
            # horray, found the movie!
            t.is_imdb_found = True
            t.got_imdb_details = True
            t.imdb_id = imdbId
            t.imdb_url = imdbUrl

            # 3. when found -> update imdb information of Title in the DB
            
            # IMBD Rating
            try:
                t.imdb_imdb_score = imdbMovieDetails['rating']
            except:
                t.imdb_imdb_score = 0
                t.notes += "IMDB Rating is missing. "
            
            # IMDB Genre
            try:
                genresStr = ', '.join(map(str, imdbMovieDetails['genres']))
                t.imdb_genre = genresStr
            except:
                t.imdb_genre = ""
                t.notes += "IMDB genre info is missing. "
            
            # IMDB Directors
            try:
                t.imdb_directors = ', '.join(map(str, imdbMovieDetails['directors']))
            except:
                t.imdb_directors = ""
                t.notes += "IMDB director info is missing. "
            
            # IMDB Cast
            try:
                imdbCastArray = imdbMovieDetails['cast']
                imdbCastStrArray = []
                for imdbCastInfo in imdbCastArray:
                    ic = imdbCastInfo['name']
                    imdbCastStrArray.append(ic)
                imdbCast = ', '.join(map(str, imdbCastStrArray))
                t.imdb_cast = imdbCast
            except:
                t.imdb_cast = ""
                t.notes += "IMDB cast info is missing. "

            # IMDB Duration
            # get imdb duration and save it
            
            # IMDB Age Rating
            try:
                parentsGuide = im.getMovieParentsGuide(imdbId)
                guides = parentsGuide["data"]["certification"] #[' Germany:6', ' United Kingdom:12', ' (video)', ' United States:TV-PG']
                t.imdb_age_rating = ', '.join(map(str, guides))
            except:
                t.imdb_age_rating = ""
                t.notes += "IMDB age rating info not found. "

            break
        
        if not(t.is_imdb_found):
            t.notes = "Movie NOT FOUND on IMDB."
            #print(t.notes)

        t.imdb_last_update_date = datetime.now()
        db.updateTitle(t)
        print(f'Searching for movie {t.spi_code} on IMDB takes %.2f seconds with status: {str(t.is_imdb_found)} ' % (time.time() - movie_search_start_time))
    print(f'getBasicImdbInfo() total execution time --- %.2f minutes & %s results ---' % ((time.time() - start_time)/60, str(len(titles))))

# Task3: Create new excel to upload to the CMS
def createCMSExcel():
    start_time = time.time()
    print("createCMSExcel() begins.")
    excelMovies_df = excel.read_filmbox_movies()
    size = len(excelMovies_df)
    
    imdbScoreChanged = []
    directorsChanged = []
    castChanged = []
    
    for i in range(size):
        spi_code = ""
        db_titles = None
        title = None
        try:
            spi_code = excelMovies_df['SPICode*'][i]
            if(spi_code.strip()==""):
                continue
            else:
                spi_code = spi_code.split("_")[0]
                spi_code = spi_code.split("-")[0]
            
            db_titles = db.getTitleBySpiCode(spi_code)
            title = getTitlesFromDBRows(db_titles)[0]
        except:
            imdbScoreChanged.append(0)
            directorsChanged.append(0)
            castChanged.append(0)
            continue
        
        # imdb score comparison
        try:
            imdb_score = float(excelMovies_df["ImdbScore"][i])
            if title.imdb_imdb_score != None and title.imdb_imdb_score != 0 and title.imdb_imdb_score != imdb_score:
                excelMovies_df["ImdbScore"][i] = str(title.imdb_imdb_score)
                imdbScoreChanged.append(1)
            else:
                imdbScoreChanged.append(0)
        except:
            imdbScoreChanged.append(0)
            continue
        
        # directors comparison
        try:
            directors = excelMovies_df["Director"][i]
            if title.imdb_directors != None and title.imdb_directors != "" and title.imdb_directors != directors:
                excelMovies_df["Director"][i] = title.imdb_directors
                directorsChanged.append(1)
            else:
                directorsChanged.append(0)
        except:
            directorsChanged.append(0)
            continue
        
        # cast comparison
        try:
            actors = excelMovies_df["Actor"][i]
            if title.imdb_cast != None and title.imdb_cast != "" and title.imdb_cast != actors:
                excelMovies_df["Actor"][i] = title.imdb_cast
                castChanged.append(1)
            else:
                castChanged.append(0)
        except:
            castChanged.append(0)
            continue
        print(f"createCMSExcel() - compared excel w/ DB. Result: imdbChanged = {imdbScoreChanged[i]}, directorChanged = {directorsChanged[i]}, castChanged = {castChanged[i]}.")

    excelMovies_df["imdbScoreChanged"] = imdbScoreChanged
    excelMovies_df["directorsChanged"] = directorsChanged
    excelMovies_df["castChanged"] = castChanged
    excel.write_movies_to_excel(excelMovies_df)
    print("createCMSExcel() total execution time --- %.2f seconds ---" % (time.time() - start_time))

# helper functions
def getTitlesFromDBRows(dbTitles):
    titles = []
    for row in dbTitles:
        title = Title.Title(row[0])
        title.spi_identifiers = row[1]
        title.spi_title_type = row[2]
        title.spi_year = int(row[3])
        title.spi_titles = row[4]
        title.spi_title_original = row[5]
        title.spi_description = row[6]
        title.spi_editorial_note = row[7]
        title.spi_fb_regions = row[8]
        title.spi_age = row[9]
        title.spi_series_title = row[10]
        title.spi_series_original_title = row[11]
        title.spi_series_season_title = row[12]
        title.spi_position = row[13]
        title.spi_publish_date = row[14]
        title.spi_release_date = row[15]
        title.spi_directors = row[16]
        title.spi_writer = row[17]
        title.spi_producer = row[18]
        title.spi_cast = row[19]
        title.spi_tags = row[20]
        title.spi_imdb_score = None if str(row[21])=='None' else float(row[21])
        title.spi_editors_score = None if str(row[22])=='None' else float(row[22])
        title.spi_duration_minutes = int(row[23])
        title.spi_slug = row[24]
        title.spi_url_webapp = row[25]
        title.spi_url_paywall = row[26]
        title.notes = row[27]
        title.is_imdb_searched = bool(row[28])
        title.is_imdb_found = bool(row[29])
        title.got_imdb_details = bool(row[30])
        title.imdb_id = row[31]
        title.imdb_url = row[32]
        title.imdb_imdb_score = row[33]
        title.imdb_genre = row[34]
        title.imdb_directors = row[35]
        title.imdb_cast = row[36]
        title.imdb_duration_minutes = int(row[37])
        title.imdb_age_rating = row[38]
        title.imdb_last_update_date = None if row[39] == "" else datetime.fromisoformat(row[39])
        titles.append(title)
        
    return titles
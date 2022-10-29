import time
import pandas as pd
import Models.Title as Title

#EXCEL_INPUT_FILE = "docs/export_video_version_138_1649234405.xlsx"
EXCEL_INPUT_FILE = "docs/Missing-Meta.xlsx"
EXCEL_OUTPUT_FILE = "docs/output-Missing-Meta.xlsx"

TRANSLATION_INPUT_FILE =  "docs/translationChecker/export_translation_version_1667085575.xlsx"
TRANSLATION_OUTPUT_FILE = "docs/translationChecker/output.xlsx"

def read_translations():
    global TRANSLATION_INPUT_FILE
    df = pd.read_excel(TRANSLATION_INPUT_FILE)
    return df

def read_filmbox_movies():
    global EXCEL_INPUT_FILE
    df = pd.read_excel(EXCEL_INPUT_FILE)
    #df = pd.read_excel('docs/filmbox_export_videos_last3days.xlsx')
    return df

def write_translations_to_excel(df):
    global TRANSLATION_OUTPUT_FILE
    df.to_excel(TRANSLATION_OUTPUT_FILE, index=False)

def write_movies_to_excel(df):
    global EXCEL_OUTPUT_FILE
    with pd.ExcelWriter(EXCEL_OUTPUT_FILE) as writer:
        df.to_excel(writer)

def read_filmbox_titles():
    start_time = time.time()
    print("excel.read_filmbox_titles() started.")
    global EXCEL_INPUT_FILE
    df = pd.read_excel(EXCEL_INPUT_FILE)
    titles = []
    
    for i in range(len(df)):
        spi_code = ""
        try:
            spi_code = df['SPICode*'][i]
            if(spi_code.strip()==""):
                continue
            else:
                spi_code = spi_code.split("_")[0]
                spi_code = spi_code.split("-")[0]
        except:
            print("SPI Code is empty for movie #" + str(i) + ".")
            continue
        
        t = Title.Title(spi_code)
        t.spi_identifiers = df['Identifier*'][i]
        t.spi_year = 0 if df['ReleaseDate*'][i] == "" else int(df['ReleaseDate*'][i][0:4])
        t.spi_title_original = df['EnglishTitle*'][i]
        if t.spi_title_original == "":
            print("Title of the movie w/ SPI Code: " + t.spi_code + " is empty.")
            continue
        t.spi_titles = df['Title*'][i]
        t.spi_directors = df['Director'][i]
        t.spi_writer = df['Writer'][i]
        t.spi_producer = df['Producer'][i]
        t.spi_tags = df['Tags*'][i]
        t.spi_cast = df['Actor'][i]
        t.spi_imdb_score = 0 if str(df['ImdbScore'][i])=='None' else float(df['ImdbScore'][i])
        t.spi_editors_score = 0 if str(df['EditorScore'][i])=='None' else float(df['EditorScore'][i])
        t.spi_url_paywall = df['Webapp URL'][i]
        t.spi_url_webapp = df['Paywall URL'][i]
        d = df['Duration*'][i].split(":")
        duration_minutes = int(d[0])*60 + int(d[1])
        t.spi_duration_minutes = duration_minutes
        t.spi_slug = df['Content Slug'][i]
        t.spi_description = df['Description*'][i]
        t.spi_editorial_note = df['EditorialNote'][i]
        t.spi_fb_regions = df['Regions*'][i]
        t.spi_age = df['Age*'][i]
        t.spi_series_title = df['SeriesTitle'][i]
        t.spi_series_original_title = df['SeriesEnglishTitle'][i]
        t.spi_series_season_title = df['SeasonTitle'][i]
        t.spi_position = df['Position'][i]
        t.spi_publish_date = df['PublishDate*'][i]
        t.spi_release_date = df['ReleaseDate*'][i]
        titles.append(t)
        
    print(f"excel.read_filmbox_titles() ended in %.2f seconds." % (time.time() - start_time))
    return titles

def write_movies_to_excel_in_buffers(df, sheetName):
    filePath = "docs/output/filmboxMoviesOutput_" + sheetName + ".xlsx"
    with pd.ExcelWriter(filePath) as writer:  
        df.to_excel(writer)

#kariyer_jobads = excel.read_kariyer_jobads()
#f3 = kariyer_jobads[:3]
#print(f3)

#for i in range(1):
#    jobad_id = f3['Ilan Kodu'][i]
#    jobad_text = f3['AllText'][i]
#    #print("Job ad ID: " + str(jobad_id) + ", Job ad text: " + jobad_text)
#    ro.get_jobad_risk_score('kariyer', jobad_id, jobad_text)

#for job_ad in first_3_kariyer_jobads:
#    print(job_ad)
#    print("\n")

#excel.read_isinolsun_jobads()
def read_kariyer_jobads():
    print("reading kariyer job ads......")
    df = pd.read_excel('docs/ilan_ornekleri.xlsx', "kariyer")
    print("reading kariyer job ads...... DONE!\n\n")
    return df

def read_isinolsun_jobads():
    print("reading isinolsun job ads......")
    df = pd.read_excel('docs/ilan_ornekleri.xlsx', "IO")
    print("reading isinolsun job ads...... DONE!")

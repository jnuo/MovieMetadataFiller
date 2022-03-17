import pandas as pd

def read_kariyer_jobads():
    print("reading kariyer job ads......")
    df = pd.read_excel('docs/ilan_ornekleri.xlsx', "kariyer")
    print("reading kariyer job ads...... DONE!\n\n")
    return df

def read_isinolsun_jobads():
    print("reading isinolsun job ads......")
    df = pd.read_excel('docs/ilan_ornekleri.xlsx', "IO")
    print("reading isinolsun job ads...... DONE!")

def read_filmbox_movies():
    df = pd.read_excel('docs/filmbox_export_videos.xlsx')
    #df = pd.read_excel('docs/filmbox_export_videos_last3days.xlsx')
    return df

def write_movies_to_excel(df):
    with pd.ExcelWriter('docs/filmboxMoviesOutput.xlsx') as writer:  
        df.to_excel(writer)

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

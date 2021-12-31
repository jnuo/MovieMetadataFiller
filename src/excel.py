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

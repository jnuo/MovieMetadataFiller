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

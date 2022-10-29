from matplotlib.transforms import composite_transform_factory
from numpy import True_
import excel
import imdbpy as im
import time
import googleSheet as gs
import pandas as pd


# Task1: CMS Excel data insert to DB
def checkForChangedTranslation():
    print(f'checkForChangedTranslation begins')
    start_time = time.time()

    cms_translations = excel.read_translations() # type: pandas dataframe
    print(f'cms_translations file size: {len(cms_translations)}.')

    cloud_translations = gs.readDavitsFile() #type: list
    print(f'cloud_translations file size: {len(cloud_translations)}.')

    dfResult = {
        "key": [],
        "English": [],
        "Turkish": [],
        "isEnglishChanged": [],
        "isTurkishChanged": [],
        "notes": []
    }

    for i in range(len(cms_translations)):
        # key
        key = cms_translations["key"][i]
        en = ""
        tr = ""
        isEnglishChaned = False
        isTurkishChanged = False
        note = ""

        # get relevant index from Davit's file
        for ct in cloud_translations:
            if ct[0]=="key":
                continue
            if ct[0]==key:
                try:
                    en = ct[3]  # assuming en is in 3rd column in the cloud file
                    tr = ct[10] # assuming tr is in 10th column in the cloud file
                    if en != cms_translations["English"][i]:
                        isEnglishChaned = True
                    if tr != cms_translations["Turkish"][i]:
                        isTurkishChanged = True
                except:
                    note = "Exception in key: " + key
                break
        dfResult["key"].append(key)
        dfResult["English"].append(en)
        dfResult["Turkish"].append(tr)
        dfResult["isEnglishChanged"].append(isEnglishChaned)
        dfResult["isTurkishChanged"].append(isTurkishChanged)
        dfResult["notes"].append(note)
        print(f"checkForChangedTranslation complete for key: " + key)
    data = pd.DataFrame(dfResult)
    excel.write_translations_to_excel(data)
    print(f"checkForChangedTranslation Total Time: %.2f seconds" % (time.time() - start_time))

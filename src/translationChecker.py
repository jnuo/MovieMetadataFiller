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
        "Bulgarian": [],
        "Czech": [],
        "Hungarian": [],
        "Polish": [],
        "Romanian": [],
        "Slovak": [],
        "Korean": [],
        "Serbian": [],
        "Croatian": [],
        "Macedonian": [],
        "Albanian": [],
        "isEnglishChanged": [],
        "isTurkishChanged": [],
        "isBgChanged": [],
        "isCzChanged": [],
        "isHuChanged": [],
        "isPlChanged": [],
        "isRoChanged": [],
        "isSlChanged": [],
        "isKrChanged": [],
        "isSrChanged": [],
        "isCrChanged": [],
        "isMaChanged": [],
        "isAlChanged": [],
        "notes": []
    }
     
    for i in range(len(cms_translations)):
        # key
        key = cms_translations["key"][i]
        en = ""
        tr = ""
        bg = ""
        cz = ""
        hu = ""
        pl = ""
        ro = ""
        sl = ""
        kr = ""
        sr = ""
        cr = ""
        ma = ""
        al = ""
        isEnglishChaned = False
        isTurkishChanged = False
        isBgChanged = False
        isCzChanged = False
        isHuChanged = False
        isPlChanged = False
        isRoChanged = False
        isSlChanged = False
        isKrChanged = False
        isSrChanged = False
        isCrChanged = False
        isMaChanged = False
        isAlChanged = False
        note = ""

        # get relevant index from Davit's file
        for ct in cloud_translations:
            if ct[0]=="key":
                continue
            if ct[0]==key:
                try:
                    en = ct[3]  # assuming en is in 3rd column in the cloud file
                    bg = ct[4]
                    cz = ct[5]
                    hu = ct[6]
                    pl = ct[7]
                    ro = ct[8]
                    sl = ct[9]
                    tr = ct[10] # assuming tr is in 10th column in the cloud file
                    kr = ct[11]
                    sr = ct[12]
                    cr = ct[13]
                    ma = ct[14]
                    al = ct[15]
                    
                    if en != cms_translations["English"][i]:
                        isEnglishChaned = True
                    if tr != cms_translations["Turkish"][i]:
                        isTurkishChanged = True
                    if bg != cms_translations["Bulgarian"][i]:
                        isBgChanged = True
                    if cz != cms_translations["Czech"][i]:
                        isCzChanged = True
                    if hu != cms_translations["Hungarian"][i]:
                        isHuChanged = True
                    if pl != cms_translations["Polish"][i]:
                        isPlChanged = True
                    if ro != cms_translations["Romanian"][i]:
                        isRoChanged = True
                    if sl != cms_translations["Slovak"][i]:
                        isSlChanged = True
                    if kr != cms_translations["Korean"][i]:
                        isKrChanged = True
                    if sr != cms_translations["Serbian"][i]:
                        isSrChanged = True
                    if cr != cms_translations["Croatian"][i]:
                        isCrChanged = True
                    if ma != cms_translations["Macedonian"][i]:
                        isMaChanged = True
                    if al != cms_translations["Albanian"][i]:
                        isAlChanged = True
                except:
                    note = "Exception in key: " + key
                break
        dfResult["key"].append(key)
        dfResult["English"].append(en)
        dfResult["Turkish"].append(tr)
        dfResult["Bulgarian"].append(bg)
        dfResult["Czech"].append(cz)
        dfResult["Hungarian"].append(hu)
        dfResult["Polish"].append(pl)
        dfResult["Romanian"].append(ro)
        dfResult["Slovak"].append(sl)
        dfResult["Korean"].append(kr)
        dfResult["Serbian"].append(sr)
        dfResult["Croatian"].append(cr)
        dfResult["Macedonian"].append(ma)
        dfResult["Albanian"].append(al)
        dfResult["isEnglishChanged"].append(isEnglishChaned)
        dfResult["isTurkishChanged"].append(isTurkishChanged)
        dfResult["isBgChanged"].append(isBgChanged)
        dfResult["isCzChanged"].append(isCzChanged)
        dfResult["isHuChanged"].append(isHuChanged)
        dfResult["isPlChanged"].append(isPlChanged)
        dfResult["isRoChanged"].append(isRoChanged)
        dfResult["isSlChanged"].append(isSlChanged)
        dfResult["isKrChanged"].append(isKrChanged)
        dfResult["isSrChanged"].append(isSrChanged)
        dfResult["isCrChanged"].append(isCrChanged)
        dfResult["isMaChanged"].append(isMaChanged)
        dfResult["isAlChanged"].append(isAlChanged)
        dfResult["notes"].append(note)
        print(f"checkForChangedTranslation complete for key: " + key)
    data = pd.DataFrame(dfResult)
    excel.write_translations_to_excel(data)
    print(f"checkForChangedTranslation Total Time: %.2f seconds" % (time.time() - start_time))


def checkForNewKeys():
    print(f'checkForNewKeys begins')
    start_time = time.time()

    cms_translations = excel.read_translations() # type: pandas dataframe
    print(f'cms_translations file size: {len(cms_translations)}.')

    cloud_translations = gs.readDavitsFile() #type: list
    print(f'cloud_translations file size: {len(cloud_translations)}.')

    dfResult = {
        "new_key": [],
        "English": []
    }
     
    for i in range(len(cms_translations)):
        # key
        cms_key = cms_translations["key"][i]
        cms_en = cms_translations["English"][i]
        
        # search for the key on the cloud file
        isFound = False
        for ct in cloud_translations:
            if ct[0] == cms_key:
                isFound = True
                break
        if(not(isFound)):
            dfResult["new_key"].append(cms_key)
            dfResult["English"].append(cms_en)
        print(f"checkForNewKeys complete for key: " + cms_key)
    data = pd.DataFrame(dfResult)
    #print(data["new_key"])
    excel.write_new_keys_from_cms_to_excel(data)
    print(f"checkForNewKeys Total Time: %.2f seconds" % (time.time() - start_time))

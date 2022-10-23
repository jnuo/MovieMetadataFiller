from numpy import True_
import excel
import imdbpy as im
import time
import googleSheet as gs

# Task1: CMS Excel data insert to DB
def checkForChangedTranslation():
    print(f'checkForChangedTranslation begins')
    start_time = time.time()

    translations = excel.read_translations()
    print(f'checkForChangedTranslation file size: {len(translations)}.')
    gs.readDavitsFile()
    print(f"insertSpiTitlesToDB_2 Total Time: %.2f seconds" % (time.time() - start_time))

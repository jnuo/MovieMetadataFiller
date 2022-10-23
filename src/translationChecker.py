from numpy import True_
import excel
import imdbpy as im
import time
import googleSheet as gs

# Task1: CMS Excel data insert to DB
def checkForChangedTranslation():
    print(f'checkForChangedTranslation begins')
    start_time = time.time()

    cms_translations = excel.read_translations()
    print(f'cms_translations file size: {len(cms_translations)}.')

    cloud_translations = gs.readDavitsFile()
    print(f'cloud_translations file size: {len(cloud_translations)}.')
    
    print(f"checkForChangedTranslation Total Time: %.2f seconds" % (time.time() - start_time))

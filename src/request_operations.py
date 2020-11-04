import time
import requests

def time_to_first_byte():
    #from urllib import request

    #host = "https://www.kariyer.net/"
    host = "https://tr.indeed.com/?r=us"

    opener = request.build_opener()
    request = request.Request(host)
    request.add_header('user-agent', 'firefox')
    start = time.time()
    resp = opener.open(request)
    resp.read(1)
    ttfb = time.time()-start

    print("Time to first byte of " + host + " is: " + str(ttfb))

def get_jobad_risk_score(jobad_platform, jobad_id, jobad_text):
    print("Platform: " + jobad_platform + ", Job ad ID: " + str(jobad_id) + ", Text: " + jobad_text)

#    jobad_text = "guzel bir ilan"

    url = "http://riskli-ilan.isinolsun.com/jobAdRiskScore"
    payload="{\n    \"jobAdPlatform\": \"" + jobad_platform + "\",\n    \"jobAdText\": \"" + jobad_text + "\",\n    \"jobAdId\": \"" + str(jobad_id) + "\"\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.encoding)
    print(response.text)


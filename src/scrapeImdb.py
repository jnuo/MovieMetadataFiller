from bs4 import BeautifulSoup
import requests

def getMovieScore(url):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'html.parser')
    x6 = soup.find("span",{'class':'AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'})
    return x6.string


def getMovieDetails(url):
    data = {}
    r = requests.get(url=url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')

    # document.getElementsByClassName('AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV')[1].innerHTML

    #page title
    title = soup.find('title')

    x6 = soup.find("span",{'class':'AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'})
    print(x6.string)
    
    data["title"] = title.string

    # rating
    ratingValue = soup.find("span", {"ratingsSummary" : "aggregateRating"})
    data["ratingValue"] = ratingValue.string

    # no of rating given
    ratingCount = soup.find("span", {"itemprop" : "ratingCount"})
    data["ratingCount"] = ratingCount.string

    # name
    titleName = soup.find("div",{'class':'titleBar'}).find("h1")
    data["name"] = titleName.contents[0].replace(u'\xa0', u'')

    # additional details
    subtext = soup.find("span",{'class':'AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'})
    data["subtext"] = ""
    for i in subtext.contents:
        data["subtext"] += i.string.strip()

    # summary
    summary_text = soup.find("div",{'class':'summary_text'})
    data["summary_text"] = summary_text.string.strip()

    credit_summary_item = soup.find_all("div",{'class':'credit_summary_item'})
    data["credits"] = {}
    for i in credit_summary_item:
        item = i.find("h4")
        names = i.find_all("a")
        data["credits"][item.string] = []
        for i in names:
            data["credits"][item.string].append({
                "link": i["href"],
                "name": i.string
            })
    return data


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

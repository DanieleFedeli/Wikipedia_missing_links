from listOfTitles import returnTitles
import requests
import time

start_time = time.time()

# Const url used for the requests
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"


def GetBacklink(session, title):
    #List of all the backlinks of the title
    #Initally empty
    backlinks = []

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "backlinks",
        "bltitle": title,
        "bllimit": "max",
        #"blredirect": "true"
        "blnamespace": "0"
    }

    response = session.get(url=WIKI_API_URL, params=PARAMS)
    DATA = response.json()

    BACKLINKS = DATA["query"]["backlinks"]

    if len(BACKLINKS) < 1: print('{} non ha backlinks.'.format(title))
    backlinks.extend(map(lambda x: x["title"], BACKLINKS))

    while "continue" in DATA:
        blcontinue = DATA["continue"]["blcontinue"]
        PARAMS["blcontinue"] = blcontinue
        response = session.get(url=WIKI_API_URL, params=PARAMS)
        DATA = response.json()
        BACKLINKS = DATA["query"]["backlinks"]
        backlinks.extend(map(lambda x: x["title"], BACKLINKS))
    return backlinks



# Const path of the output folder path
OUTPUT_PATH = "./output/"

print('Starting.')
session = requests.Session()
listOfTitles = returnTitles("dataset.csv")
done = 0

for title in listOfTitles:
    print(title)
    filename = OUTPUT_PATH+title+'.txt'
    with open(filename, "w", encoding="UTF-8") as out_file:
        backlinks = GetBacklink(session, title)
        print(backlinks, file=out_file)
        done = done+1
    print('We did the {percent:.2f}%'.format(percent=100 * done/len(listOfTitles)))

print('API CALLED %d TIMES' % len(listOfTitles))
print('Finish.')
print("--- %s seconds ---" % (time.time() - start_time))

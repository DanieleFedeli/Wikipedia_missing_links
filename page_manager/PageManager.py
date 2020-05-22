
import xml.dom.minidom

# Const url used for the requests
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

# Used to return a list of all dataset's page's title
def SetOfPages(filename):
    doc = xml.dom.minidom.parse(filename)
    pages = doc.getElementsByTagName("page")

    # Empty list
    listOfTitles = []

    # Iterate through all the pages
    for page in pages:
        # Retrieve title of the current page
        title = page.getElementsByTagName("title")[0].firstChild.data
        # we build the list of the title
        listOfTitles.append(title)

    return listOfTitles

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
        "blnamespace": "0"
        #"blredirect": "true"
        
    }

    response = session.get(url=WIKI_API_URL, params=PARAMS)
    DATA = response.json()

    BACKLINKS = DATA["query"]["backlinks"]

    #if len(BACKLINKS) < 1: print('{} non ha backlinks.'.format(title))
    backlinks.extend(map(lambda x: x["title"], BACKLINKS))

    while "continue" in DATA:
        blcontinue = DATA["continue"]["blcontinue"]
        PARAMS["blcontinue"] = blcontinue
        response = session.get(url=WIKI_API_URL, params=PARAMS)
        DATA = response.json()
        BACKLINKS = DATA["query"]["backlinks"]
        backlinks.extend(map(lambda x: x["title"], BACKLINKS))
    return backlinks

def FillTheFile(title, backlinks, out_file):

    print('\n'.join(backlinks), file=out_file)
    
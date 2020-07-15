from nltk.corpus import stopwords
import requests
import re
import nltk
nltk.download('stopwords')


WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
inputTitleRepr = './ShortReprLists'


def retrieveCategoryFromJson(pages, optimize=False):
    categories = []
    for k, v in pages.items():

        for cat in v['categories']:
            titleCategory = cat['title'].replace('Category:', '')
            if 'All' in titleCategory:
                continue
            if 'Pages' in titleCategory:
                continue
            if 'Articles' in titleCategory:
                continue
            if 'Wikipedia' in titleCategory:
                continue
            if 'Wikidata' in titleCategory:
                continue
            categories.append(titleCategory)
            splitted = re.findall(r"([A-Za-z]{3,})", titleCategory)
            if(optimize):
                categories.extend(
                    x.capitalize() for x in splitted if x not in stopwords.words('english'))

    return list(set(categories))


def FindCategory(session, title, optimize=False):
    category = []
    PARAMS = {
        "action": "query",
        "format": "json",

        "prop": "categories",
        "titles": title
    }

    response = session.get(url=WIKI_API_URL, params=PARAMS)

    data = response.json()

    pages = data['query']['pages']
    category.extend(retrieveCategoryFromJson(pages, optimize))

    while "continue" in data:

        clcontinue = data["continue"]["clcontinue"]
        PARAMS["clcontinue"] = clcontinue
        response = session.get(url=WIKI_API_URL, params=PARAMS)
        data = response.json()
        pages = data['query']['pages']
        category.extend(retrieveCategoryFromJson(pages, optimize))
    return list(set(category))


def getAllBacklinksFromFile(filename):
    backlinks = []
    row_number = 0
    with open(inputTitleRepr+'/'+filename+'.txt.txt', 'r') as f:
        for row in f:
            row_number += 1
            splitted = row.split(' -')
            splitted = splitted[0].split(' ')
            backlinks.extend(splitted)
    return (row_number, backlinks)


def routine(session, title, optimize=False):
    print('Processing {}...'.format(title))
    categoryOfTitle = FindCategory(session, title, optimize)
    dictOfCategories = {el.capitalize(): 0 for el in categoryOfTitle}
    infoFromBacklinks = getAllBacklinksFromFile(title)
    backlinksNumber = infoFromBacklinks[0]
    backlinks = infoFromBacklinks[1]
    for bl in backlinks:
        blCategories = FindCategory(session, bl, optimize)
        for cat in blCategories:

            if cat.capitalize() in dictOfCategories:
                #print('{} is in'.format(cat.capitalize()))

                dictOfCategories[cat.capitalize()] += 1
        # print('--------')
    maxCat = max(dictOfCategories, key=dictOfCategories.get)
    cSim = dictOfCategories[maxCat]/backlinksNumber
    print('{}\t{}\t{}'.format(title, maxCat, round(cSim, 2)), file=f)


session = requests.Session()
titles = ['Official_(tennis)', 'Maria_Pepe', 'SEAT_Arona', 'Dodge_Coronet',
          'Christmas_window', 'Last.fm', 'Traditional_bluegrass']

with open('output.txt', 'w') as f:
    print('Entity\t\tCategory\t\tc-Similarity\n', file=f)
    for title in titles:
        routine(session, title)

    print('\nOPTIMIZED ROUTINE\n', file=f)

    print('Entity\t\tCategory\t\tc-Similarity\n', file=f)
    for title in titles:
        routine(session, title, True)

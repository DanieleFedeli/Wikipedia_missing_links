def returnTitles(filename):
    blacklist = ['/', '&', '"']
    fin = open(filename, "r", encoding = "utf-8")
    listOfTitles = []
    firstRow = fin.readline()
    for row in fin:
        row = row.strip().split(';')
        title = row[0]
        incomingLinks = row[1]
        if(checkTitle(title, blacklist)):
            listOfTitles.append(title)
    
    return listOfTitles


def checkTitle(title, blacklist):
    for char in title:
        for elem in blacklist:
            if(char == elem):
                return False
    return True

myList = returnTitles("dataset.csv")
    

from getMatrix import getDB
import Levenshtein


def main():
    global db
    db = getDB("database.txt")
    res = searchByQuery("ghoul")
    printTitleManga(res)


def getUserPref(user):
    global db
    db = getDB("database.txt")
    tim = [db[10], db[0], db[62]]
    john = [db[28], db[46], db[39]]
    susan = [db[56], db[2], db[54]]
    if user == "tim":
        return tim
    if user == "john":
        return john
    if user == "susan":
        return susan

#********************** Different searching manners ********************#

def searchByTitle(title):
    global db
    db = getDB("database.txt")
    distance = {}
    mangasTitle = []
    mangasDict = []
    res = {}
    for manga in db:
        distance[manga['title']] = Levenshtein.distance(title, manga['title'])
    sortedDict = {k: v for k, v in sorted(distance.items(), key=lambda item: item[1])}
    for manga, distance in sortedDict.items():
        if distance < len(title)/2:
            mangasTitle.append(manga)
    for elem in mangasTitle:
        mangasDict.append(getDictByTitle(elem))
    additionalRes = getSimilar(mangasDict, db)
    for elem in additionalRes:
        mangasDict.append(getDictByTitle(elem))
    return mangasDict


def searchByCategory(category, pref):
    global db
    db = getDB("database.txt")
    allCat = getAllCategories()
    distance = {}
    tmp = []
    res = []
    for refCat in allCat:
        distance[refCat] = Levenshtein.distance(category, refCat) #get distance
    sortedDict = {k: v for k, v in sorted(distance.items(), key=lambda item: item[1])}
    goalCat = list(sortedDict.keys())[0]
    print("Here are the result for "+goalCat+" category")
    for mangas in db:
        if goalCat in getArrayCategories(mangas['categories']):
            tmp.append(mangas)

    if len(tmp) < 10:
        print("<10")
        accurateRes = getSimilar(pref, db)
        for manga in tmp:
            res.append(manga)
    else:
        accurateRes = getSimilar(pref, tmp)
    for mangas in accurateRes:
        res.append(getDictByTitle(mangas))
    return res


def searchByPopularity():
    global db
    db = getDB("database.txt")
    print("Here are the most popular manga: ")
    res = []
    res = db[0:10]
    return res


def searchGuided(pref):
    global db
    db = getDB("database.txt")
    res = []
    resTmp = getSimilar(pref, db)
    for elem in resTmp:
        res.append(getDictByTitle(elem))
    return res


def searchByQuery(query):
    global db
    db = getDB("database.txt")
    synopClean = getData() #array with cleaned synopsis
    scores = {}
    res = []
    i = 0
    for synopsis in synopClean:
        words = synopsis.split(" ")
        score = []
        for word in words:
            score.append(Levenshtein.distance(word, query))
        scores[i] = min(score)
        i += 1
    sortedDict = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    getMin = list(sortedDict.values())[0]
    for index, score in sortedDict.items():
        if score <= getMin:
            res.append(db[index])
    addRes = getSimilar(res, db)
    for mangas in addRes:
        res.append(getDictByTitle(mangas))
    return res

#***********************************************************************#

#********************** get score and most accurate manga **************#

def getSimilar(listRef, listTest): #listRef: we want manga similar to them, listTest: the future similar manga are in this list
    restmp = {}
    modifiedDB = getModifiedDB(listRef, listTest)#= listTest without manga in the listRef
    for ref in listRef:
        for manga in modifiedDB:
            score = 0
            score += getCategoryScore(ref, manga)
            score += getPopularityScore(manga)
            score += getLengthScore(ref, manga)
            score = round(score, 2)
            restmp[manga['title']] = score
    res = getBestElem(restmp)
    return res


def getModifiedDB(listToRemove, basedList): #remove manga from list to db for comparison
    res = basedList.copy()
    for elem in listToRemove:
        try:
            res.remove(elem)
        except:
            pass
    return res


def getCategoryScore(ref, test): #return a score from 0 to 70
    scores = []
    testCategories = getArrayCategories(test['categories'])
    score = 0
    refCategories = getArrayCategories(ref['categories'])
    for testCategory in testCategories:
        if testCategory in refCategories:
            score += 1
    scoreF = (score/len(testCategories))*70
    return scoreF


def getArrayCategories(string):
    array = string.split(',')
    res = []
    for elem in array:
        elem = elem.replace('[', "")
        elem = elem.replace(']', "")
        elem = elem.replace('\'', "")
        if elem[0] == " ":
            elem = elem.replace(" ","", 1)
        res.append(elem)
    return res


def getPopularityScore(test): #return a score from 0 to 20
    global db
    rank = test['rank']
    score = (20*float(rank) - 20*len(db))/(1-len(db)) #we have 2 points: (1, 10), (len(db),0)
    score = round(score, 3)
    return score


def getLengthScore(ref, test): #return a score from 0 to 10. 10 is when number of tome of "test" is similar to number of tomes of "ref"
    if(ref['tomes'] == 'None' or test['tomes'] == 'None'):
        return 10
    else:
        refTomes = int(ref['tomes'])
        testTomes = int(test['tomes'])
        difference = abs(refTomes-testTomes)/((refTomes+testTomes)/2)*10
        if(difference > 10):
            return 0
        return difference


def getBestElem(dict):
    res={}
    sortedDict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}
    for manga, score in sortedDict.items():
        if len(res) < 10:
            res[manga] = score
        else:
            return res

#***********************************************************************#

#****************************** tools **********************************#
def printTitleManga(res):
    for mangas in res:
        print(mangas['title'])


def getDictByTitle(title):
    global db
    for manga in db:
        if manga['title'] == title:
            return manga


def getAllCategories():
    global db
    res = []
    for mangas in db:
        array = getArrayCategories(mangas['categories'])
        for elem in array:
            if elem not in res:
                res.append(elem)
    sort = sorted(res)
    return sort

def getData():
    f = open("cleanData.txt", "r")
    content = f.read()
    splited = content.split("\n\n")[:-1]
    return splited

db = []

if __name__ == "__main__":
	main()

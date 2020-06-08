from getMatrix import getDB
import Levenshtein

def main():
    global db
    db = getDB("database.txt")
    res = searchByPopularity()
    print("searching for 'Narutio'")
    searchByTitle('Narutio')
    print("\n\nsearching for 'Attac titan'")
    searchByTitle('Attac titan')
    print("\n\nsearching for 'full matal elachemis'")
    searchByTitle('full matal elachemis')
    #getModifiedDB(res)
    #getSimilar(res)
    #getCategoryScore(res, db[0])

def searchByTitle(title):
    global db
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
    print("the user is looking for:")
    print(mangasTitle)

    for elem in mangasTitle:
        mangasDict.append(getDictByTitle(elem))

    additionalRes = getSimilar(mangasDict)
    for elem in additionalRes:
        mangasDict.append(getDictByTitle(elem))
    print("mangadvisor recommends:")
    for elem in mangasDict:
        print(elem['title'])
    return res

def getDictByTitle(title):
    global db
    for manga in db:
        if manga['title'] == title:
            return manga



def searchByCategory(category):
    global db
    res = []

    return res


def searchByPopularity():
    global db
    #db = getDB("database.txt")
    res = []
    res = db[0:5]
    return res


def getSimilar(listRef):
    global db
    restmp = {}
    modifiedDB = getModifiedDB(listRef)#= database without manga in the list Ref
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


def getModifiedDB(list): #remove manga from list to db for comparison
    global db
    res = db.copy()
    for elem in list:
        res.remove(elem)
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



def printTitleManga(res):
    for mangas in res:
        print(mangas['title'])





db = []

if __name__ == "__main__":
	main()

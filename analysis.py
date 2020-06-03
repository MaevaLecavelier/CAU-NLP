import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import string
import re

#if you try to run this code for the first time, use this:
#import nltk
#nltk.download('stopwords')
#nltk.download('punkt') #takes time

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def main():
    global dicManSyn
    db = getDB("database.txt")
    dicManSyn = mangaSynopsis(db)
    dtm = getDTMatrix(dicManSyn)
    print(dtm)


#get content from file made by kitsuapi
def getDB(file):
    f = open(file, "r")
    content = f.read()
    f.close()
    db = stringToList(content)
    return db

#transform content file to list, for easier manipulation
def stringToList(str):
    db = []
    mangas = str.split("{")
    for manga in mangas[1:]:
        x = {}
        attributes = manga.split("$")
        for details in attributes[1:]:
            item = details.split("->")
            key = item[0]
            if key == "tomes":
                value = item[1][0:-2]
            else:
                value = item[1]
            x[key] = value
        db.append(x)
    return db

#get a dict with key: title, value: synopsis
def mangaSynopsis(database):
    data = {}
    for mangas in database:
        data[mangas['title']] = mangas['synopsis']
    return data


#********************** get Document-Term matrix **************************#

def getDTMatrix(dict):
    names = getIndex(dict)
    data = getData(dict)
    dataCleaned = cleanData(data)
    vec = CountVectorizer()
    X = vec.fit_transform(dataCleaned)
    df = pd.DataFrame(X.toarray(), index=names, columns=vec.get_feature_names())
    return df


    ##### parameters of the matrix #####
#return an array with the title of each manga
def getIndex(dict):
    res = []
    for key in dict:
        res.append(key)
    return res


#return an array with the synopsis of each mangas
def getData(dict):
    res = []
    for datas in dict.values():
        res.append(datas)
    return res

    #############################

    ##### clean data for the matrix #####
def cleanData(list):
    global stop
    clean = []
    allWords = []
    i = 1
    nb_round = 2
    while i <= nb_round:
        for datas in list:
            data = removePonct(datas)
            str = ""
            tokens = word_tokenize(data)
            filtered = [w for w in tokens if not w in stop]
            allWords.append(filtered)
            if i == nb_round: #add words only at the final iteration, to have clean result.
                for words in filtered:
                    if removeDigit(words):
                        str += words+" "
                clean.append(str)
        if i < nb_round: #update stopWord for each iteration except the last one
            removeCommonWords(allWords)
        i += 1
    return clean



        # remove ponctuation
def removePonct(str):
    exclude = ['!','"','#','%','$','&','\'','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','\\','^','_','`','{','}','|','~','\\n']
    res = ''.join(char for char in str if char not in exclude)
    return res

        # remove digit
def removeDigit(str):
    pattern = '^([A-Za-z]|-)+$'
    regex = re.compile(pattern)
    if regex.match(str):
        return str
    else:
        return ""

        ###########################

#******************** end get Document-Term Matrix  **********************#

#******************* clean data ******************************************#

def removeCommonWords(listOfList):
    global dicManSyn
    global stop
    global toAdd
    tmp_result = {} #key: word, value: number of document where they appear
    for listOfWords in listOfList:
        for word in listOfWords:
            tmp_result[word] = 0
            for synopsis in dicManSyn.values():
                if word in synopsis:
                    tmp_result[word] += 1
    for k, v in tmp_result.items():
        if (v >= len(listOfList)/2):
            toAdd.append(k)
    stop = updateStopWord(stop,toAdd)

#******************* end clean data **************************************#


#********************* init and global variables *************************#

toAdd = ["year", "years"]
#define the stop words list with more words, according to special case
def updateStopWord(listStopWords, listToAdd):
    for elem in listToAdd:
        if elem not in listStopWords:
            listStopWords.append(elem)
    return listStopWords

stop = updateStopWord(stopwords.words('english'), toAdd )
dicManSyn = {}
#************************************************************************#

if __name__ == "__main__":
	main()

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


#define the stop words list with more words, according to special case
def updateStopWord(list):
    toAdd = ['years','year']
    for elem in toAdd:
        list.append(elem)
    return list

stop = updateStopWord(stopwords.words('english'))



def main():
    db = getDB("database.txt")
    dicManSyn = mangaSynopsis(db)
    getDTMatrix(dicManSyn)



def getDB(file):
    f = open(file, "r")
    content = f.read()
    f.close()
    db = stringToList(content)
    return db


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


def mangaSynopsis(database):
    data = {}
    for mangas in database:
        data[mangas['title']] = mangas['synopsis']
    return data


def getDTMatrix(dict):
    names = getIndex(dict)
    data = getData(dict)
    dataCleaned = cleanData(data)
    vec = CountVectorizer()
    X = vec.fit_transform(dataCleaned)
    df = pd.DataFrame(X.toarray(), index=names, columns=vec.get_feature_names())
    print(df)


def removePonct(str):
    exclude = ['!','"','#','%','$','&','\'','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','\\','^','_','`','{','}','|','~']
    res = ''.join(char for char in str if char not in exclude)
    return res

def removeDigit(str):
    pattern = '^([A-Za-z]|-)+$'
    regex = re.compile(pattern)
    if regex.match(str):
        return str
    else:
        return ""


def cleanData(list):
    global stop
    clean = []
    for datas in list:
        data = removePonct(datas)
        str = ""
        tokens = word_tokenize(data)
        filtered = [w for w in tokens if not w in stop]
        for words in filtered:
            if removeDigit(words):
                str += words+" "
        clean.append(str)
    return clean


def getIndex(dict):
    res = []
    for key in dict:
        res.append(key)
    return res

def getData(dict):
    res = []
    for datas in dict.values():
        res.append(datas)
    return res


if __name__ == "__main__":
	main()

import requests
import json
from lazr.restfulclient.errors import ServerError

api = "https://kitsu.io/api/edge/manga?sort=popularityRank&page[limit]=1&page[offset]="
header = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json'
        }
limit = 10

def main():
	responses = getResponses()
	db = getDataBase(responses)
	# db[0]["title"] -> title of the first manga
	# work for title, synopsis, rank and tomes

def getDataBase(responses):
	db = []
	for data in responses:
		x = {}
		x["title"] = data["data"][0]["attributes"]["canonicalTitle"]
		x["synopsis"] = data["data"][0]["attributes"]["synopsis"]
		x["rank"] = data["data"][0]["attributes"]["popularityRank"]
		x["tomes"] = data["data"][0]["attributes"]["chapterCount"]
		print(x["title"])
		db.append(x)

def getResponses():
	responses = []
	for i in range(0,limit):
		response = getAttributes(i)
		if response != None:
			responses.append(json.loads(response))
	return responses

def getAttributes(id):
	r = requests.get(api + "{}".format(id), headers=header)
	if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
	return r.text


if __name__ == "__main__":
	main()
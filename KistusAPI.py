import requests
import json
from lazr.restfulclient.errors import ServerError

api = "https://kitsu.io/api/edge/manga"
header = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json'
        }
limit = 10 # Determine the number of mangas

def main():
	responses = getResponses()
	db = getDataBase(responses)
	# db[0]["title"] -> title of the first manga
	# Work for title, synopsis, rank, tomes,
	# categories (string[]) and comments (string[])

def getDataBase(responses):
	db = []
	for data in responses:
		x = {}
		x["title"] = data["attributes"]["canonicalTitle"]
		x["synopsis"] = data["attributes"]["synopsis"]
		x["rank"] = data["attributes"]["popularityRank"]
		x["rating"] = data["attributes"]["averageRating"]
		x["tomes"] = data["attributes"]["chapterCount"]
		x["categories"] = getCategories(data["id"])
		x["comments"] = getComments(data["id"])
		db.append(x)

def getResponses():
	responses = []
	for i in range(0,limit):
		response = getAttributes("?sort=popularityRank&page[limit]=1&page[offset]={}".format(i))
		if response != None:
			responses.append(json.loads(response)["data"][0])
	return responses

def getAttributes(path):
	r = requests.get(api + path, headers=header)
	if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
	return r.text

def getCategories(id):
	categories = []
	response = getAttributes("/{}/categories?page[limit]=20".format(id))
	if response != None:
			responses = json.loads(response)
	else:
		return categories
	for data in responses["data"]:
		categories.append(data["attributes"]["title"])
	return categories

def getComments(id):
	comments = []
	response = getAttributes("/{}/reviews?page[limit]=20".format(id))
	if response != None:
			responses = json.loads(response)
	else:
		return comments
	for data in responses["data"]:
		comments.append(data["attributes"]["content"])
	return comments

if __name__ == "__main__":
	main()
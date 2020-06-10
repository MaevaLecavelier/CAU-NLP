import sys
import getResult

def main():
    user = getUser()
    welcome(user)
    userPref = getResult.getUserPref(user)
    try:
        while True:
            request = getRequest()
            handleRequest(request, userPref)
    except KeyboardInterrupt:
        print("Thank you for using MangAdivsor! See you soon")
        exit()


def getUser():
    if(len(sys.argv) == 1):
        print("You should give your username as an argument. Please retry")
        exit()
    elif sys.argv[1] not in ['john', 'tim', 'susan']:
        print("Unknown user.")
        exit()
    else:
        return sys.argv[1]

def welcome(name):
    print("Welcome to MangAdvisor "+name+".")
    print("To start you journey, enter one of the following request:")
    print("\t -'title' if you want to search by title.")
    print("\t -'category' if you want to search by category.")
    print("\t -'popularity' if you want to search by popularity.")
    print("\t -'other' if you want to search by key words for example (ninja, ghoul...)")
    print("\t -'guided' if you want to discover new things...")
    print("\t - to leave enter CTR-C\n")

def getRequest():
    request = input("What do you want?\n")
    expected = ['title', 'category', 'popularity', 'guided', 'other']
    while request not in expected:
        request = input("Bad input. Please try again:\n")
    return request


def handleRequest(request, pref):
    res = []
    if(request == 'title'):
        title = input("Which title? \n")
        res = getResult.searchByTitle(title)
        print("\nresult: ")
        getResult.printTitleManga(res)

    if(request == 'category'):
        category = input("Which category? \n")
        res = getResult.searchByCategory(category, pref)
        print("\nresult: ")
        getResult.printTitleManga(res)

    if(request == 'popularity'):
        res = getResult.searchByPopularity()
        print("\nresult: ")
        getResult.printTitleManga(res)

    if(request == 'other'):
        query = input("Enter a keyword: ")
        res = getResult.searchByQuery(query)
        print("\nresults:")
        getResult.printTitleManga(res)

    if(request == 'guided'):
        res = getResult.searchGuided(pref)
        print("\nresult: ")
        getResult.printTitleManga(res)
    print("\n\n")
    return res



if __name__ == "__main__":
	main()

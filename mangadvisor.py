import sys
import getResult

def main():
    user = getUser()
    welcome(user)
    request = getRequest()
    handleRequest(request)



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
    print("\t -'guided' if you want to discover new things...\n")

def getRequest():
    request = input("What do you want?\n")
    expected = ['title', 'category', 'popularity', 'guided']
    while request not in expected:
        request = input("Bad input. Please try again:\n")
    return request

def handleRequest(request):
    res = []
    if(request == 'title'):
        print("search title")
    if(request == 'category'):
        print("search category")
    if(request == 'popularity'):
        res = getResult.searchByPopularity()
    if(request == 'guided'):
        print("search guided")
    return res



if __name__ == "__main__":
	main()

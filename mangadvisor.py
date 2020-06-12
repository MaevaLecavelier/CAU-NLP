import sys
import subprocess
import webbrowser
import os
import getResult

def main():
    user = getUser()
    welcome(user)
    userPref = getResult.getUserPref(user)
    try:
        while True:
            request = getRequest()
            result = handleRequest(request, userPref)
            createWebPage(result)
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

def createWebPage(results):

    print("Building Web page...")
    content = """
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    """

    content += """
        <table class="table table-striped table-dark">
            <thead>
                <b>
                    <th text-align="center">Title</th>
                    <th text-align="center">Synopsis</th>
                    <th text-align="center">Rank</th>
                    <th text-align="center">Rating</th>
                    <th test-align="center">Likeness</th>
                </b>
            </thead>
    """

    for elem in results:
        content += """
            <tr>
                <td>""" + elem["title"] + """</td>
                <td>""" + elem["synopsis"] + """</td>
                <td>""" + elem["rank"] + """</td>"""
        if (float(elem["rating"]) > 70.0):
            content += """<td><p class="text-success">""" + elem["rating"] + """</p></td>"""
        elif (float(elem["rating"]) > 45.0):
            content += """<td><p class="text-warning">""" + elem["rating"] + """</p></td>"""
        else:
            content += """<td><p class="text-danger">""" + elem["rating"] + """</p></td>"""
        try:
            content += """<td> <div style="color:#ff7d91;text-align:center;"> """ + elem['score'] + """%</div></td>"""
        except:
            pass
        content += """</tr>"""
    content += """</table> """

    html_file = open('result.html',"w")
    html_file.write(content)
    html_file.close()

    url = "result.html"

    new = 2

    webbrowser.open(url, new=new)

if __name__ == "__main__":
	main()

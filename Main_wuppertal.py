# Import BeautifulSoup
from bs4 import BeautifulSoup as bs

content = []
import csv

# Read the XML file
with open("stolpersteine_wuppertal.xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")
result = bs_content.find("text")

String = str(result)
string_list = String.splitlines()

# function takes a string and checks which kind of informations it holds
def check_type(string):

    if string.rfind("Gedenkbuch") != (-1):
        return "informationen"

    elif string.find("Internetquelle") != (-1):
        return "infoleer"

    elif len(string) == 1:
        return "infoleer"

    elif string.find("landmark") != (-1):
        return "adresse"

    elif string.find("[[Datei") != (-1):
        return "weiter"

    elif len(string) == 1:
        return "weiter"

    elif string.find("]]" , 0 ,40) != (-1):
        return "stadt"

    elif string.find("data-sort-value") != (-1):
        return "name"

    elif string.rfind("Gedenkbuch") != (-1):
        return "informationen"

    elif len(string) == 2:
        return "nextperson"

    else:
        if len(string) > 20:
            return ("weiter")
        else:
            return "datum"

# checks if string contains substring "rowspan"
# if yes, if removes it
def check_rowspan(string):
    if string.find("rowspan") != (-1):
        liste = list(string)
        del liste[0:14]
        newstring = ""
        newstring = newstring.join(liste)
        return newstring
    else:
        return string

global_list = []
temporary_list = [0, 0, 0, 0, 0,0]

# checks which kind of information the string holds an removes the unnecessary signs
# adds the clean information to the temporary list
# whenever the function detects, that the following information is about the next person, to temporary_list
# is added to the global_list

def funktion(string_list):

    global temporary_list
    global global_list

    for x in string_list:
        x = check_rowspan(x)

        if check_type(x) == "weiter":
            continue

        elif check_type(x) == "adresse":
            x = x.split("&lt")[0]
            liste1 = list(x)
            del liste1[0]
            x = ""
            x = x.join(liste1)
            temporary_list[0] = x

        elif check_type(x) == "stadt":
             x = x.replace("[[", " ")
             x = x.replace("]]", " ")
             x = x.replace('''|''', " ")
             temporary_list[1] = x

        elif check_type(x) == "datum":
            x = x.replace('''|''', " ")
            temporary_list[2] = x

        elif check_type(x) == "name":
            name = x.replace('''| align="center" data-sort-value="''' , " ")
            name = name.split('''"''')[0]

            inschrift = x.split('''|''')[3]
            inschrift = inschrift.replace("&lt;br /&gt" , " ")
            inschrift = inschrift.replace("}}","")
            inschrift = inschrift.replace("{{" , "")
            inschrift = inschrift.replace("\'\'\'", "")
            inschrift = inschrift.replace(";", "\n")

            temporary_list[3] = name
            temporary_list[5] = inschrift

        elif check_type(x) == "informationen":
            x = x.split("&lt")[0]
            liste1 = list(x)
            del liste1[0]
            x = ""
            x = x.join(liste1)
            x = x.replace("[[", " ")
            x = x.replace("]]", " ")
            temporary_list[4]  = x

        elif check_type(x) == "infoleer":
            temporary_list[4]  = " "

        elif check_type(x) == "nextperson":
            global_list.append(temporary_list.copy())

        else:
            pass

    return global_list

# create the final list
liste = funktion(string_list)


# create csv file
with open('liste_der_stolpersteine_in_wuppertal.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for x in liste:
        list_csv = x
        writer.writerow(list_csv)














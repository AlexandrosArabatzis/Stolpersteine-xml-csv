import pandas as pd
import re
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "de_DE")

'''This programs purpose is to convert raw xml-data to csv. The different information types (name, adress, birthdate etc)
we need are not in different tags. Instead all the information is in one tag. The raw data we are working with 
looks like this:

.
.
|-
| 66 {{Anker|Wilhelm Kratz}}
| {{PersonZelle|'''Wilhelm|Kratz'''|nl=1}}
| Stresemannstr. 23&lt;br /&gt;{{Coordinate|simple=y|text=ICON0|NS=51.182293|EW=7.041579|type=landmark|region=DE-NW|name=Stolperstein Wilhelm Kratz}}
| style="text-align:center;"| Hier wohnte&lt;br /&gt;Wilhelm Kratz &lt;br /&gt;Jg. 1906&lt;br /&gt;im Widerstand&lt;br /&gt;verhaftet 1.1.1942&lt;br /&gt;hingerichtet 5.10.1942&lt;br /&gt;Gefängnis Köln-Klingelpütz
|[[Datei:SG Stolperstein - Wilhelm Kratz.jpg|140px]]
| Wilhelm Kratz wurde 1906 in Solingen geboren. Bereits 1933 wurde er wegen Bandendiebstahls zu 7 Monaten Haft verurteilt und floh danach in die Niederlande. 1934 wurde er wegen Hochverrat und Waffenbesitz verurteilt und zur Fahndung ausgeschrieben. 1935 befand er sich illegal in Solingen, um innerhalb der [[KPD]] über die [[Brüsseler Konferenz der KPD|Brüsseler Konferenz]] zu berichten. 1937 wurden 17 Solinger Bürger zu Haftstrafen verurteilt, weil sie ihm nahe standen, darunter seine Ehefrau Elfriede. Nach dem Überfall auf die Niederlande 1942 zog Kratz nach Belgien und wurde am 1. Januar 1942 dort entdeckt. Bei der Verhaftung erschoss Kratz einen Polizisten und einen Wehrmachtsangehörigen, wobei er selbst verletzt wurde. Am 31. August wurde Kratz vom Sondergericht [[Essen]] zum viermaligen Tod verurteilt und am 5. Oktober 1942 durch das [[Fallbeil]] im Polizeigefängnis [[Klingelpütz]] in Köln hingerichtet.&lt;ref&gt;[https://www.solingen.de/de/archiv/stolperstein-kratz-wilhelm-94066/ ''Wilhelm Kratz''] auf Solingen.de&lt;/ref&gt;

|-
| 78
| {{PersonZelle|'''Georg|Bethke'''|nl=1}}
| Rosenkamper Str. 10b&lt;br /&gt;{{Coordinate|simple=y|text=ICON0|NS=51.179680|EW=7.039050|type=landmark|region=DE-NW|name=Stolperstein Georg Bethke}}
| style="text-align:center;"| Hier wohnte&lt;br /&gt;Georg Bethke &lt;br /&gt;Jg. 1893&lt;br /&gt;verhaftet 1937&lt;br /&gt;KZ Mauthausen&lt;br /&gt;ermordet 20.4.1944
|[[Datei:SG Stolperstein - Georg Bethke.jpg|140px]]
.
.


The information we want to extract is:
- First Name
- Last Name
- Adress
- Date of Birth
- Place of Birth
- Date of Death
- Day of Deportation

Every block contains information about one individual. In each case we will extract

First Name and Last Name                --> 3rd. line
Adress                                  --> 4th. line
Place of Birth                          --> 7th line
Date of Death and Day of Deportation    --> 7th line if possible, else from 4th line
Date of Birth                           --> 7th line if possible, else from 5th line

Because every line ist different, but still has some reoccuring patterns, we will use Regular Expressions to extract the
relevant data. Then we will store the clean information in a DataFrame and export it to csv.'''

# Read the file.
file = open("all_stolpersteine_solingen_xml/stolpersteine_solingen-mitte.xml")
content = file.read()
file.close()

list_fname = []
list_lname = []
list_adresse = []
list_geburtstag = []
list_todestag = []
list_geburtsort = []
list_deprtationstag = []
list_inschrift = []

# split the the raw string into substrings which contain information about one person each
content = content.split("\n\n")

for person in content:
    info = person.splitlines()

    while(len(info)<=7):
        info.append("empty")

    # Last Name
    lname_re = re.search('((?<=\'\'\' )|(?<=\'\'\'))[a-z ]*', info[2], flags=re.IGNORECASE)
    lname = lname_re.group()
    lname = lname.strip()

    # first name
    fname_re = re.search('[a-z üäö]*(?=\'\'\'\|nl=1)', info[2], flags=re.IGNORECASE)
    fname = fname_re.group()
    fname = fname.strip()

    # Adresse
    adresse = info[3].split("&lt")[0]
    adresse = adresse[2:]

    # Geburtstag
    geburtstag_re = re.search('[0-9]{1,2}\.\D*[0-9]{4}(?=\D* geboren)', info[6])
    if geburtstag_re:
        x = geburtstag_re.group()
        geburtstag = datetime.strptime(x, "%d. %B %Y")

    else:
        geburtstag_re_inschrift = re.search('((Jg\.)|(geb\.)) [0-9]{4}', info[4])
        if(geburtstag_re_inschrift):
            x = geburtstag_re_inschrift.group()
            x = x[-4:]
            geburtstag = datetime.strptime(x, "%Y")
        else:
         geburtstag = None

    # Todestag
    todestag_re = re.search('[0-9]{1,2}\.\D*[0-9]{4}(?=\D* ermordet|hingerichtet)', info[6])
    if todestag_re:
        y = todestag_re.group()
        todestag = datetime.strptime(y, "%d. %B %Y")
    else:
        todestag_re_inschrift = re.search('((?<=ermordet )|(?<=tod )|(?<=tot ))[\d]*\.[\d]*\.[\d]*', info[3],
                                          flags=re.IGNORECASE)
        if(todestag_re_inschrift):
            y = todestag_re_inschrift.group()
            todestag = datetime.strptime(y, "%Y")
        else:
            todestag = None

    # Geburtsort
    geburtsort_re = re.search('(?<= in )\D*(?= geboren)', info[6])
    if geburtsort_re:
        geburtsort = geburtsort_re.group()
        geburtsort = geburtsort.replace('''[''' , "")
        geburtsort = geburtsort.replace(''']''' , "")
    else:
        geburtsort = None


    # Debortationsdatum
    deportationsdatum_re = re.search('(([0-9]{1,2}\.\D*[0-9]{4})|([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}))(?=[\D]*deportiert)'
                                     , info[6])
    if deportationsdatum_re:
        z = deportationsdatum_re.group()
        deportationsdatum = datetime.strptime(z, "%d. %B %Y")
    else:
        deportationsdatum_re_inschrift = re.search('(?<=deportiert )[\d]*', info[3],
                                          flags = re.IGNORECASE)
        if (deportationsdatum_re_inschrift):
            z = deportationsdatum_re_inschrift.group()
            deportationsdatum = datetime.strptime(z, "%Y")
        else:
            deportationsdatum = None

    # add the extracted data to lists
    list_lname.append(fname)
    list_fname.append(lname)
    list_adresse.append(adresse)
    list_geburtstag.append(geburtstag)
    list_todestag.append(todestag)
    list_geburtsort.append(geburtsort)
    list_deprtationstag.append(deportationsdatum)


# create Series from the lists
fnameSeries = pd.Series(list_fname, index = list_lname)
adresseSeries = pd.Series(list_adresse, index = list_lname)
geburtstagSeries = pd.Series(list_geburtstag, index = list_lname)
todestagSeries = pd.Series(list_todestag, index = list_lname)
geburtsortSeries = pd.Series(list_geburtsort, index = list_lname)
deportationsdatumSeries = pd.Series(list_deprtationstag, index = list_lname)


# Make DataFrame from Series and export to CSV
df = pd.DataFrame({"Vorname" : fnameSeries, "Adresse Stolperstein" : adresseSeries, "Geburtstag" : geburtstagSeries,
                   "Geburtsort" :
    geburtsortSeries, "Todestag" : todestagSeries, "Deportationsdatum" : deportationsdatumSeries})
df.index.name = "Nachname"
df.to_csv(r'Stolpersteine_Solingen.csv')




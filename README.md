# Stolpersteine-xml-csv


**What the program is about** <br/>

Stolpersteine are memorial plaques in memory of WW2. There is a list of Stolpersteine from Wuppertal ( Northrhine-Westfalia, Germany) with information on wikipedia. I extracted information from xml file and converted it to csv. These csv will support the Historia-App.



Links:

Stolpersteine on Wikipedia <br>
https://de.wikipedia.org/wiki/Liste_der_Stolpersteine_in_Wuppertal


Historia-App<br>
https://historia-app.de


**How the Code works** <br/>
This programs purpose is to convert raw xml-data to csv. The different information types (name, adress, birthdate etc)
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

 - First Name and Last Name                --> 3rd. line
 - Adress                                  --> 4th. line
 - Place of Birth                          --> 7th line
 - Date of Death and Day of Deportation    --> 7th line if possible,
   else from 4th line
 - Date of Birth                           --> 7th line if possible,
   else from 5th line

Because every line ist different, but still has some reoccuring patterns, we will use Regular Expressions to extract the
relevant data. Then we will store the clean information in a DataFrame and export it to csv.

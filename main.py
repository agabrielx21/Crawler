from bs4 import BeautifulSoup
import concurrent.futures
import requests
import time

start_time = time.time()
baseURL = 'https://www.olx.ro/d/electronice-si-electrocasnice/?page='
olxLINK = 'http://olx.ro'
links = []
nrPages = 25
j=0
finalList = []
tuplu = ()

def generateLinks():
    for j in range(nrPages):
        url = baseURL + str(j)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        anunturi = soup.find_all('div', class_='css-19ucd76')
        for anunt in anunturi:
            for link in anunt.find_all('a'):
                linkurl = link.get('href')
                if linkurl not in links:
                    links.append(linkurl)

def extract(link):
    descriere = ''
    titlu = ''
    pret = ''
    stare = ''
    url = olxLINK + link
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    if soup.find('div', class_='css-g5mtbi-Text'):
        descriere = soup.find('div', class_='css-g5mtbi-Text').text
    if soup.find('div', class_='css-1wws9er'):
        titlu = soup.find('div', class_='css-1wws9er').h1.text
    if soup.find('div', class_='css-dcwlyx'):
        pret = soup.find('div', class_='css-dcwlyx').h3.text
    if soup.find('p', class_='css-xl6fe0-Text eu5v0x0'):
        stare = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')[-2].text
    tuplu = (descriere, titlu, pret, stare)
    return tuplu


a = ["DESCRIERE","TITLU","PRET","STARE"]

generateLinks()
with concurrent.futures.ThreadPoolExecutor() as executor:
    with open("op1.txt", "w", encoding="utf-8", errors="ignore") as f:
        list = executor.map(extract, links)
        i=1
        for tuple in list:
            f.write(str(i) + '\n')
            xz = 0
            if tuple:
                for item in tuple:
                    f.write(a[xz] + '\n')
                    f.write(item + '\n')
                    i += 1
                    xz += 1

# print("--- %s seconds ---" % (time.time() - start_time))
from flask import Flask, render_template
import re
cnt = 0
flagOras = 0
apple, lenovo, samsung, asus, sony, huawei, xiaomi, dell, test = 0, 0, 0, 0, 0, 0, 0, 0, 0

nou, utilizat = 0, 0

lei, euro = 0, 0

telefon, televizor, laptop, pc, tableta, casti, consola = 0, 0, 0, 0, 0, 0, 0

bucuresti, cluj, timisoara, iasi, galati, constanta = 0, 0, 0, 0, 0, 0

preturi = []

filters = {
    "Marca": {
        "Samsung": [],
        "Apple": [],
        "Huawei": [],
        "Xiaomi": [],
        "Sony": [],
        "Lenovo": [],
        "Asus": [],

    },
    "Tip device": {
        "Televizor": [],
        "Telefon": [],
        "Laptop": [],
        "PC": [],
        "Tabletă": [],
        "Căști": [],
        "Consolă": [],

    },
    "Stare": {
        "Nou" : [],
        "Utilizat" : []
    },
    "Moneda": {
        "Lei" : [],
        "Euro" : []
    },
    "Preț": {
        "0-100" : [],
        "101-500": [],
        "501-1000": [],
        "1001-5000": [],
        "5001+": []
    },
    "Oraș": {
        "București" : [],
        "Cluj-Napoca": [],
        "Timișoara": [],
        "Iași": [],
        "Galați": [],
        "Constanța": [],
        "Alte orase": []
    }

}

with open("op1.txt", "r", encoding="utf-8") as f:
    for linie in f:
        flagOras = 0
        line = linie.lower()
        #Filtru 1 stare
        if re.match("Stare: Nou",linie):
            nou += 1
            filters["Stare"]["Nou"] = [nou]
        if re.match("Stare: Utilizat",linie):
            utilizat += 1
            filters["Stare"]["Utilizat"] = [utilizat]
        #Filtru 2,3 preturi
        if linie == "PRET" + "\n":
            cnt += 1
            line = f.readline()
            matches = re.finditer("\d+(?=\s*lei)", line)
            if re.match("\d*\s€",line):
                euro += 1
                filters["Moneda"]["Euro"] = euro
            else:
                lei += 1
                filters["Moneda"]["Lei"] = lei
            for match in matches:
                preturi.append(match.group())
        #Filtru 4
        if linie == "TITLU" + "\n":
            line = f.readline().lower()
            if re.search("sa(m|n)su(m|n)g*",line):
                samsung += 1
                filters["Marca"]["Samsung"] = [samsung]
            if re.search("ap*le",line):
                apple += 1
                filters["Marca"]["Apple"] = [apple]
            if re.search("a*iphone",line):
                apple += 1
                filters["Marca"]["Apple"] = [apple]
            if re.search("lenovo",line):
                lenovo += 1
                filters["Marca"]["Lenovo"] = [lenovo]
            if re.search("asus",line):
                asus += 1
                filters["Marca"]["Asus"] = [asus]
            if re.search("son(y|i)",line):
                sony += 1
                filters["Marca"]["Sony"] = [sony]
            if re.search("hu*a(w|u)ei",line):
                huawei += 1
                filters["Marca"]["Huawei"] = [huawei]
            if re.search("xia*omi",line):
                xiaomi += 1
                filters["Marca"]["Xiaomi"] = [xiaomi]
            if re.search("dell",line):
                dell += 1
                filters["Marca"]["Dell"] = [dell]
            #Filtru 5
            if re.search("tablet(a|e|ă)",line):
                tableta += 1
                filters["Tip device"]["Tabletă"] = [tableta]
            if re.search("telefo(n|ane)",line):
                telefon += 1
                filters["Tip device"]["Telefon"] = [telefon]
            if re.search("l(a|e)pt(a|o)p",line):
                laptop += 1
                filters["Tip device"]["Laptop"] = [laptop]
            if re.search("(tv|televizo(are|r))",line):
                televizor += 1
                filters["Tip device"]["Televizor"] = [televizor]
            if re.search("(pc|calculator|computer)", line):
                pc += 1
                filters["Tip device"]["PC"] = [pc]
            if re.search("c(a|ă)(s|ș)ti", line):
                casti += 1
                filters["Tip device"]["Căști"] = [casti]
            if re.search("con*sol(a|ă)", line):
                consola += 1
                filters["Tip device"]["Consolă"] = [consola]
            #Filtru 6 ORAS
        if re.search("bucure(s|ș)ti", line) and flagOras == 0:
            bucuresti +=1
            flagOras = 1
        if re.search("cluj", line) and flagOras == 0:
            cluj += 1
            flagOras = 1
        if re.search("timi(s|ș)oara", line) and flagOras == 0:
            timisoara += 1
            flagOras = 1
        if re.search("ia(s|ș)i", line) and flagOras == 0:
            iasi += 1
            flagOras = 1
        if re.search("gala(t|ț)i", line) and flagOras == 0:
            galati += 1
            flagOras = 1
        if re.search("constan(t|ț)a", line) and flagOras == 0:
            constanta += 1
            flagOras = 1


filters["Oraș"]["București"] = [bucuresti]
filters["Oraș"]["Cluj-Napoca"] = [cluj]
filters["Oraș"]["Timișoara"] = [timisoara]
filters["Oraș"]["Iași"] = [iasi]
filters["Oraș"]["Galați"] = [galati]
filters["Oraș"]["Constanța"] = [constanta]


counter1, counter2, counter3, counter4, counter5 = 0, 0, 0, 0, 0
#Filtru3
for item in preturi:
    if int(item) < 101:
        counter1 += 1
    elif int(item) < 501:
        counter2 += 1
    elif int(item) < 1001:
        counter3 += 1
    elif int(item) < 5001:
        counter4 += 1
    else:
        counter5 +=1

    filters["Preț"]["0-100"] = [counter1]
    filters["Preț"]["101-500"] = [counter2]
    filters["Preț"]["501-1000"] = [counter3]
    filters["Preț"]["1001-5000"] = [counter4]
    filters["Preț"]["5001+"] = [counter5]

print(filters["Oraș"])

app = Flask(__name__)
@app.route("/")
def home():
  return render_template('index.html', filters = filters)

if __name__ == "__main__":
  app.run()
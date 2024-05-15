import csv
from pprint import pprint
import json

with open("article.csv") as csvdata:
    csvRead = csv.reader(csvdata, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    csvDataList = [row for row in csvRead]

    jsondata = [[],[],[]]

    for i in range(len(csvDataList)):
        dict = {'name':csvDataList[i][1], 'url': csvDataList[i][2]}
        if int(csvDataList[i][0]) % 2 == 1:
            jsondata[2].append(dict)

        if int(csvDataList[i][0])  >= 4:
            jsondata[0].append(dict)

            if int(csvDataList[i][0]) - 4 >= 2:
                jsondata[1].append(dict)

        elif int(csvDataList[i][0]) >= 2:
            jsondata[1].append(dict)
    
    jsondumpdata = {
        "master": jsondata[0],
        "hard": jsondata[1], 
        "normal": jsondata[2]
    }

    with open("article.json", "w") as f:
        json.dump(jsondumpdata, f)
        print("compile sucsess")
import mycsv
import json

def csv2json(header, data):
    basics = {"headers":[],"data":[]}
    for i in range(len(header)):
        basics["headers"].append(header[i])
    list_dict = list()
    for i in range(len(data)):
        dict_row = dict()
        for j in range(len(header)):
            dict_row[header[j]] = data[i][j]
        list_dict.append(dict_row)
    for i in range(len(list_dict)):
        basics["data"].append(list_dict[i])
    output = str(basics).replace("'", '"')
    print(output)

header,data = mycsv.readcsv(mycsv.getdata())
csv2json(header,data)
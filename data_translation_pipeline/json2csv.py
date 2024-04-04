import json
import mycsv

data = mycsv.getdata()
def json2csv(jsontxt):
    data = json.loads(jsontxt)
    header_c = ",".join(data['headers'])
    rows = [header_c]
    for i in range(len(data['data'])):
        list_data = []
        for j in range(len(data['headers'])):
            list_data.append(data['data'][i][data['headers'][j]])
        row = ",".join(list_data)
        rows.append(row)
    rows_csv = '\n'.join(rows)
    print(rows_csv)

json2csv(data)
import mycsv

def csv2html(header, data):
    ht_header=['<th>'+i+'</th>' for i in header]
    ht_data1 = [['<td>'+i+'</td>' for i in j] for j in data]
    ht_total = [ht_header] + ht_data1
    ht_trs = ['<tr>'+"".join(i)+'</tr>' for i in ht_total]
    basics = ['<html>','<body>','<table>','</table>','</body>','</html>']
    for i in range(len(ht_trs)):
        basics.insert(-3,ht_trs[i])
    output = "\n".join(basics)
    print(output)

header,data = mycsv.readcsv(mycsv.getdata())
csv2html(header,data)
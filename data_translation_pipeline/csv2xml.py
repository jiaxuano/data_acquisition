import mycsv
def csv2xml(header, data):
    header2 = [i.replace(" ","_") for i in header]
    data_lines = []
    for i in range(len(data)):
        line_secs = []
        for j in range(len(header)):
            line_sec = f'''<{header2[j]}>{data[i][j]}</{header2[j]}>'''
            line_secs.append(line_sec)
        data_line = "".join(line_secs)
        data_lines.append(data_line)
    record_lines = ['    <record>\n'+'      '+i+'\n'+'    </record>\n' for i in data_lines]
    header_ht = '  <headers>'+",".join(header)+'</headers>\n'
    basics = ['<?xml version=\"1.0\"?>\n','<file>\n', header_ht, '  <data>\n', '  </data>\n','</file>\n']
    for i in range(len(record_lines)):
        basics.insert(-2,record_lines[i])
    output = "".join(basics)
    print(output)
header,data = mycsv.readcsv(mycsv.getdata())
csv2xml(header,data)
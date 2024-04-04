import untangle
import mycsv

data = mycsv.getdata()

def xml2csv(xmltxt):
    xml = untangle.parse(xmltxt)
    xml_records = xml.file.data.record
    header_str = xml.file.headers.cdata
    data_rows = [header_str]
    for i in range(len(xml_records)):
        data_row = []
        for j in range(len(xml_records[0].children)):
            data_row.append(xml.file.data.record[i].children[j].cdata)
        row_str = ",".join(data_row)
        data_rows.append(row_str)
    output = "\n".join(data_rows)
    print(output)

xml2csv(data)
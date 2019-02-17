import csv

def processDate(date):
    data = []
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    data.append(year)
    data.append(month)
    data.append(day)
    return data

def setHeaders(list):
    list.append("PICKUP_YEAR")
    list.append("PICKUP_MONTH")
    list.append("PICKUP_DAY")
    list.append("DELIVERY_YEAR")
    list.append("DELIVERY_MONTH")
    list.append("DELIVERY_DAY")
    return list

if __name__ == "__main__":
    file = csv.writer(open("processedData.csv", "wb+"))
    header = False
    pickup = ""
    delivery = ""

    with open('RawData.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            
            if not header:
                row = setHeaders(row)
                header = True
            else:
                pickup = row[14]
                delivery = row[15]
                row.extend(processDate(pickup))
                row.extend(processDate(delivery))
            
            file.writerow(row)
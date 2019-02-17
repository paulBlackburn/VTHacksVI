import httplib, urllib, base64, json, csv

def getParams(params):
    params = urllib.urlencode({
    "account" : params["account"],
    "destinationZip" : params["destinationZip"],
    "destinationState" : params["destinationState"],
    "destinationCity" : params["destinationCity"],
    "originState" : params["originState"],
    "originCity" : params["originCity"],
    "pickupDate" : params["pickupDate"],
    "deliveryDate" : params["deliveryDate"],
    })
    return params

def getOrders(conn, params, headers):
    conn.request("GET", "/orders/orders?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    return data

if __name__ == "__main__":
    params = {
    "account" : "",
    "destinationZip" : "",
    "destinationState" : "",
    "destinationCity" : "",
    "originState" : "",
    "originCity" : "",
    "pickupDate" : "",
    "deliveryDate" : ""
    }
    
    headers = {
    "Ocp-Apim-Subscription-Key" : "b5ff836411024a20988e655b9e1008fc"
    }
    
    '''
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    '''

    date = ""
    day = 01
    month = 01
    year = 2015
    conn = httplib.HTTPSConnection("jbhhackathonlab.azure-api.net")
    file = csv.writer(open("output.csv", "wb+"))
    header = False
    row = 0
    
    while True:
        date = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + "T00:00:00.000Z"
        params["deliveryDate"] = date
        data = getOrders(conn, getParams(params), headers)
        
        if data:
            data = json.loads(data)
            
            if data:
                print("Delivery Date: " + str(date))
                if not header:
                    file.writerow(data[0].keys())
                    header = True
                for element in data:
                    if row % 10000 == 0:
                        print("Row: " + str(row))
                    file.writerow(element.values())
                    row += 1
        
        day += 1
        
        if day == 18 and month == 1 and year == 2015:
            day = 19
            month = 9
        if day == 27 and month == 9 and year == 2015:
            day = 25
            month = 12
        
        if day == 32:
            day = 1
            month += 1
            if month == 13:
                month = 1
                year += 1
                if year == 2017:
                    break

    conn.close()
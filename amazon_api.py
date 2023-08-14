import http.client
import json
import mysql.connector
import config

def insert(value):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=config.passwd,
        database="orders",
        port="6942"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO ordernums (ID) VALUES (%s);"
    val = (12345)
    mycursor.execute(sql,(value,))

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def Convert(string): #yeah i have split the string parsed from json into a list and apparently this works
    li = list(string.split(" "))
    return li

def json_find(d, key): #it's almost criminal how handsome and good at coding i am
    if isinstance(d, dict):
        if key in d.keys():    # base case
            return d.get(key)
        return " ".join([ json_find(d[k],key) for k in d.keys() ])
    elif isinstance(d, list):
        return " ".join([ json_find(x,key) for x in d ])
    else:
        return ""              # base case

def getToken():
    conn = http.client.HTTPSConnection("api.amazon.com")
    payload = 'grant_type=refresh_token&refresh_token=$$$$$$$&client_secret=$$$$$$$'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/auth/o2/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))

    y=json.loads(data)

    return(str((y["access_token"])))

def getOrders():
    token = getToken()
    conn = http.client.HTTPSConnection("sellingpartnerapi-na.amazon.com")
    payload = ''
    headers = {
    'x-amz-access-token': '',
    'X-Amz-Date': '20230808T164624Z',
    'Authorization': 'AWS4-HMAC-SHA256 Credential=$$$$$/20230808/us-east-1/execute-api/aws4_request, SignedHeaders=host;x-amz-access-token;x-amz-date, Signature=$$$$$$'
    }
    headers['x-amz-access-token']=token
    conn.request("GET", "/orders/v0/orders?CreatedAfter=2023-08-01&MarketplaceIds=ATVPDKIKX0DER&FulfillmentChannels=AFN", payload, headers)
    res = conn.getresponse()
    data2 = res.read()
    #print(data.decode("utf-8"))
    return(data2)

data2 = getOrders()
jdata1 = json.loads(data2)
jdata = jdata1["payload"]

s = json_find(jdata, "AmazonOrderId")

listey = Convert(s)
print(listey)

ele = listey.pop() #removes last value from list because i'm too lazy to figure out why an empty value is being added every time

for i in listey:
    #print(i)
    insert(i)
    




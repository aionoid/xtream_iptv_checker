import requests as rq
import datetime as dt
import json
import pprint
# import asyncio

# site = 'http://mohdtv.com:8880'
# username = 'smarttv585cde0010b6'
# password = '67346552'
# url = f'{site}/player_api.php?username={username}&password={password}'

def read_sites():
    sites = dict()
    with open('site.json','r') as sjson:
        sites= json.load(sjson)
    return sites

def getXtreamInfo(site,username,password):
    out = 0
    url = f'{site}/player_api.php?username={username}&password={password}'
    try:
        rs =rq.get(url,timeout=1)
        data = rs.json()
        for key in data:
            if isinstance(data[key],dict):
                for k in data[key]:
                    #if (k in ['exp_date','created_at']):
                    if (k in 'exp_date'):
                        #dt.datetime(second=data[key][k])
                        exp_date = dt.datetime.fromtimestamp(int(data[key][k]))
                        exp_string =exp_date.strftime("%d/%m/%Y")
                        out = f'::{exp_string}::=>::{username}::{password} \n'
                        return out
                    # else:
                    #     print(f'{username}=>{key}::{k}::{data[key][k]}')
        
    except :
        print("error")
    return out

def main():
    with open('working.txt','w') as working:
        xtreams = read_sites()
        for data in xtreams:
            for url in data:
                print(url)
                working.write(f'{url} \n') 
                for username in data[url]:
                    password = data[url][username]
                    out  = getXtreamInfo(url,username,password)
                    if out != 0:
                        print(out)
                        working.write(out) 
        # pprint.pprint(all);

if __name__ == '__main__':
    main()

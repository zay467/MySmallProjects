from covid import Covid
import requests
# c = Covid()
# try : 
#     x = c.get_status_by_country_name("india")
#     print(x)
#     [print(i,":",x[i]) for i in x]
# except ValueError:
#     print("Country does not exist")
# except : 
#     print("Server Error")
try : 
    city = input()
    addr = "https://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=76cea6e6473d0a10b43946f70c8bd502"%(city)
    w = requests.get(url = addr)
    data = w.json()
    temp = data["main"]["temp"]
    weat = data["weather"][0]["description"]
    humi = data["main"]["humidity"]
    name = data["name"]
    print(temp)
except KeyError: 
    print("value")
# except :
#     print("hello")
# x = c.get_status_by_country_name("india")
# print(x)
# [print(i,":",x[i]) for i in x]
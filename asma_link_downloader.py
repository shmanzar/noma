import requests
import urllib.request
import os, shutil
import pandas
import concurrent.futures as futures

month = str(input("Please enter the Month (MM): \n"))
print("\n"+month)
year = str(input("Please enter the Year (YYYY): \n"))
print("\n"+year)

####credentials 

login_url = "http://www.monitoring.punjab.gov.pk/users/login_confirm"
continue_link = "http://www.monitoring.punjab.gov.pk/evaccs/setting/list_measles_datapack"

user, password = 'evaccs_visitors@pitb.gov.pk', 'evaccs_visitors'

download_path = os.path.expanduser('~/Desktop/Measles_Datapacks/')

####set download folder on desktop

if os.path.exists(download_path) and os.path.isdir(download_path):
    shutil.rmtree(download_path)
    os.mkdir(download_path)

payload = {
    'username': user, 
    'password': password
     #'submit' : "Sign In"
}


####Login with credentials 

####with requests.Session() as session:

s = requests.Session()
s.get(login_url)
post = s.post(login_url, data = payload)
r = s.get(continue_link)

#print(r.text)

districts = list(range(1,37))

url =[]

for district in districts:
    link = f'http://www.monitoring.punjab.gov.pk/evaccs/setting/list_vaccinators_children_in_dp?month={year}-{month}&district_id={district}'
    url.append(link)
    filename = f'{download_path}{district}_{year}{month}_VaccinatorsChildrenDataPack'
    s.get(link)
    urllib.request.urlretrieve(link, filename)
    print(f'http://www.monitoring.punjab.gov.pk/evaccs/setting/list_vaccinators_children_in_dp?month={year}-{month}&district_id={district}')

# print(url)

def fetch_url(entry):
    uri = entry
    if not os.path.exists(download_path):
        r = requests.get(uri, stream=True)
        if r.status_code == 200:
            with open(uri, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
    return uri

with futures.ThreadPoolExecutor(max_workers=5) as executor:
    pages = executor.map(fetch_url, url)
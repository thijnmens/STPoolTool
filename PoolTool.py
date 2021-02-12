import os, io, pickle, json, time, subprocess, zipfile
import dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('.env'))
ID = '12-KGea4sRUoLX-tiIwYT6i-FTjQEz0Zy'
Name = 'Links.json'

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

config = os.getenv('pog')
service = Create_Service(config, 'drive', 'v3', ['https://www.googleapis.com/auth/drive'])

def getFile(ID, Name):
    request = service.files().get_media(fileId=ID)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download finished')

    fh.seek(0)

    with open(os.path.join('./data', Name), 'wb') as f:
        f.write(fh.read())
        f.close()

print('Downloading ID list')
getFile(ID, Name)

Quest = input('Are you on quest or pc? [Q/P]: ').lower()
Download = input('Which map pools would you like to download? [4~7]: ')

links = str(json.loads(open('data\Links.json', encoding='utf8').read()))
links = links.split("~")
Lvl4 = 'Skip'
lvl4z = 'Skip'
Lvl5 = 'Skip'
lvl5z = 'Skip'
Lvl6 = 'Skip'
lvl6z = 'Skip'
Lvl7 = 'Skip'
lvl7z = 'Skip'
if Download == '4':
    Lvl4 = links[1]
    lvl4z = links[3]
elif Download == '5':
    Lvl5 = links[5]
    lvl5z = links[7]
elif Download == '6':
    Lvl6 = links[9]
    lvl6z = links[11]
elif Download == '7':
    Lvl7 = links[13]
    lvl7z = links[15]
else:
    print('Invalid input, please use a number between 4 and 7, this number should also be the lvl you are in.\nPlease close the program and try again.')
    time.sleep(60)

IDList = [Lvl4,  lvl4z, Lvl5,  lvl5z, Lvl6,  lvl6z, Lvl7,  lvl7z, ]
NameList = ['Lvl_4_map_pool.json', 'Lvl4.zip', 'Lvl_5_map_pool.json', 'Lvl5.zip', 'Lvl_6_map_pool.json', 'Lvl6.zip', 'Lvl_7_map_pool.json', 'Lvl7.zip']

a = 0
b = len(IDList)-1
while a <= b:
    if IDList[a] != 'Skip':
        print(f'Downloading {NameList[a]}')
        getFile(ID=IDList[a], Name=NameList[a])
        if Quest == 'q':
            try:
                with zipfile.ZipFile(f'.\data\{NameList[a]}', 'r') as zip_ref:
                    print('unzipping...')
                    zip_ref.extractall(f'.\data\{NameList[a]}')
            except zipfile.BadZipFile:
                None
            except FileNotFoundError:
                print('Something went wrong while unzipping the file, please unzip it yourself, the program will continue in 3 seconds')
                time.sleep(3)
        elif Quest == 'p':
            print('PC is not supported yet, but it will be in the near future!')
        elif Quest != 'p' and Quest != 'q':
            print('Something went wrong, make sure you only fill in values that are giving to you between the brackets like this: [values]')
    a = a + 1



cwd = os.getcwd()
os.remove("data\Links.json")
subprocess.Popen(f'explorer "{cwd}\data"')  
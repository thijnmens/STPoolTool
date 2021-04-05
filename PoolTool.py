import colorama, os, io, pickle, json, time, subprocess, zipfile, requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from distutils.dir_util import copy_tree
from shutil import copyfile
from pathlib import Path

colorama.init()
cwd = os.getcwd()
config = os.getenv("CONFIG")

ID = '12-KGea4sRUoLX-tiIwYT6i-FTjQEz0Zy'
Name = 'Links.json'
version = 'V2.0.0'
response = requests.get("https://api.github.com/repos/thijnmens/STpooltool/releases/latest")
if response.json()["name"] != version:
    print(f'----------\nA NEW VERSION IS AVAILABLE, download it here:\nhttps://github.com/thijnmens/STPoolTool/releases/latest\nCurrent version: {version}\nLatest version: {response.json()["name"]}\n----------')

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

def ERRORCODE(Code, Arg1=None):
    if Code == 1:
        print(colorama.Style.RESET_ALL)
        input(colorama.Fore.RED + '[ERRORCODE: 1] You didnt specify a value correctly, make sure you only fill in values that are giving to you between the brackets like this: [values]\nPress enter to Exit...')
        exit()
    elif Code == 2:
        print(colorama.Style.RESET_ALL)
        input(colorama.Fore.RED + '[ERRORCODE: 2] The zip got corrupted and the program is unable to unzip it, please re-run the program and if this doesnt fix it contact a dev\nPress enter to continue...')
        print(colorama.Style.RESET_ALL)
    elif Code == 3:
        print(colorama.Style.RESET_ALL)
        input(colorama.Fore.RED + '[ERRORCODE: 3] The downloaded file wasnt found, did you delete it?\nPress enter to continue...')
        print(colorama.Style.RESET_ALL)
    elif Code == 4:
        print(colorama.Style.RESET_ALL)
        input(colorama.Fore.RED + '[ERRORCODE: 4] The program is missing permission to complete a certain action, try running it as an administrator\nPress enter to continue...')
        print(colorama.Style.RESET_ALL)
    elif Code == 5:
        print(colorama.Style.RESET_ALL)
        input(colorama.Fore.RED + f'[ERRORCODE: 5] The program is tryign to create a file that already exists ({Arg1}), The program will attempt to delete the file, this action can NOT be undone\nPress enter to continue...')
        print(colorama.Style.RESET_ALL)
    

print('Downloading ID list')
getFile(ID, Name)

Platform = input('Are you on quest or pc? [Q/P]: ').lower()
if Platform != 'p' and Platform != 'q':
    ERRORCODE(1)
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
    ERRORCODE(1)

IDList = [Lvl4,  lvl4z, Lvl5,  lvl5z, Lvl6,  lvl6z, Lvl7,  lvl7z, ]
NameList = ['Lvl_4_map_pool.json', 'Lvl4.zip', 'Lvl_5_map_pool.json', 'Lvl5.zip', 'Lvl_6_map_pool.json', 'Lvl6.zip', 'Lvl_7_map_pool.json', 'Lvl7.zip']

if Platform == 'p':
    print('Searching for beat saber install...')
    if os.path.isdir('C:\Program Files (x86)\Steam\steamapps\common\Beat Saber'):
        BSPathRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Beat Saber'
        print(f'BS Install found at {BSPathRoot}\nCopying Songs...')
    elif os.path.isdir(''):
        BSPathRoot = 'C:\Program Files\Oculus\Software\Software\hyperbolic-magnetism-beat-saber'
        print(f'BS Install found at {BSPathRoot}\nCopying Songs...')
    else: 
        BSPathRoot = input('We couldn\'t find your Beat Saber installation, please provide it\nExample: C:\Program Files (x86)\Steam\steamapps\common\Beat Saber')
        

a = 0
b = len(IDList)-1
while a <= b:
    if IDList[a] != 'Skip':
        print(f'Downloading {NameList[a]}')
        getFile(ID=IDList[a], Name=NameList[a])
        filepath = Path(f'{cwd}\data\{NameList[a]}')
        if str(NameList[a]).split('.')[1] == 'zip':
            try:
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    print('unzipping...')
                    zippath = f'{cwd}\data\{str(NameList[a]).split(".")[0]}'
                    zip_ref.extractall(zippath)
            except zipfile.BadZipFile:
                ERRORCODE(2)
            except FileNotFoundError:
                ERRORCODE(3)
            if Platform == 'p':
                BSPath = BSPathRoot + '\Beat Saber_Data\CustomLevels'
                try:
                    copy_tree(f'{cwd}\data\{str(NameList[a]).split(".")[0]}', BSPath)
                except FileExistsError:
                    ERRORCODE(5, BSPath)
                input('Sucessfully installed all songs!\nPress enter to Exit...')
        if str(NameList[a]).split('.')[1] == 'json' and Platform == 'p':
            BSPath = BSPathRoot + f'\Playlists\{NameList[a]}'
            try:
                copyfile(f'{cwd}\data\{NameList[a]}', BSPath)
            except PermissionError:
                ERRORCODE(4)
            except FileExistsError:
                ERRORCODE(5, BSPath)
                os.remove(BSPath)
                copyfile(f'{cwd}\data\{NameList[a]}', BSPath)
    a = a + 1

os.remove("data\Links.json")
if Platform == 'q':
    maps = os.listdir(zippath)
    for song in maps:
        songPath = zippath + f'\{song}'
        with zipfile.ZipFile(f'{zippath}\{song}.zip', 'w') as zipObj:
            for file in os.listdir(songPath):
                filePath = songPath + f'\{file}'
                zipObj.write(filePath, os.path.basename(filePath))
    input('Sucessfully installed all songs!\nPress enter to Exit...')
    subprocess.Popen(f'explorer "{zippath}"')
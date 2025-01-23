import os
import sys
import json
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def set_path():
    file_path = hou.pwd().parm('file').evalAsString()
    base_path = '/'.join(file_path.split('/')[:-1])
    # print(base_path)
    # print(os.listdir(base_path))

    try:
        file_version = len([file for file in os.listdir(base_path) if file.endswith('bgeo.sc')])
    except:
        os.mkdir(base_path)
    message = 'Setting version: ' + str(file_version)
    hou.ui.displayMessage(message)

    if hou.pwd().parm('trange').eval() == 0:
        new_file_path = base_path + '/$HIPNAME.$USER_ID.' + r'asset_v{0}.bgeo.sc'.format(file_version)
    else:
        new_file_path = base_path + '/$HIPNAME.$USER_ID.' + r'asset_v{0}.$F.bgeo.sc'.format(file_version)

    # print(new_file_path)
    hou.pwd().parm('file').set(new_file_path)


def drivePublish():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    # get token
    flow = InstalledAppFlow.from_client_secrets_file(
        r'Your path to json credentials file',  # json credentials
        SCOPES
    )
    creds = flow.run_local_server(port=0)

    # save token
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())

    json_token_file = os.path.abspath('token.json')
    print(f"json token file path: {json_token_file}")

    # load token
    creds = Credentials.from_authorized_user_file('token.json')

    # auth token
    headers = {
        "Authorization": f"Bearer {creds.token}"
    }

    file_path = hou.pwd().parm('file').evalAsString()
    file_name = file_path.split('/')[-1]
    # file parms
    para = {
        "name": file_name,
    }

    # open file
    files = {
        "data": ("metadata", json.dumps(para), "application/json; charset=UTF-8"),
        "file": open(file_path, "rb"),
    }

    # request for publish
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files,
    )

    print(r.status_code)
    print(r.text)


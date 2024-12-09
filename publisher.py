import os
import sys
import json
import requests


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
    token = "ya29.a0AeDClZAZPlj69J9mnRnSIveBpNkqBOrxmR7DC4V1LCrdagpezb_WfxE7bJTxzo7Orvh8uY_Fzqk141wTZ-aBy3RtO6CNC0pFDMOTloLUa-iIviDBhEBc8Ng4RYB99La1LOmCv0y4FLc18aDSpRT8YDCukoZcZGRn8wyoccKeaCgYKAVUSARASFQHGX2MiKTkGfNWs-7dE-8J_V19cVw0175"
    # auth token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    file_path = hou.pwd().parm('file').evalAsString()
    file_name = file_path.split('/')[-1]
    # file parms
    para = {
        "name": file_name,  # Имя файла на Google Drive
    }

    # Открываем файл
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


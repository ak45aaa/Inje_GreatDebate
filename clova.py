<<<<<<< HEAD
import requests
import sys

def return_text(file):
    client_id = '보안문제로 인해 문의 바람'
    client_secret = '보안문제로 인해 문의 바람'

    headers = {
        "X-NCP-APIGW-API-KEY-ID" : client_id,
        "X-NCP-APIGW-API-KEY" : client_secret,
        "Content-Type" : "application/octet-stream"
    }

    language = "Kor"
    csr_rest_api_url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt"

    url = csr_rest_api_url + "?lang=" + language

    with open(file, 'rb') as data:  # 여기에 실제 음성 파일 데이터를 넣어야 합니다.
        response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code  # 서버로부터 받은 상태 코드를 rescode 변수에 저장

    return rescode, response.json() if rescode == 200 else None
    # 녹음 파일 형식 mp3, aac, ac3, ogg, flac, wav파일 형식 가능
=======
import http.client
import json
import sys
import urllib.parse

def return_text(file):
    client_id = ''
    client_secret = ''

    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }

    language = "Kor"
    host = "naveropenapi.apigw.ntruss.com"
    path = f"/recog/v1/stt?lang={language}"

    conn = http.client.HTTPSConnection(host)

    with open(file, 'rb') as data:
        conn.request("POST", path, body=data, headers=headers)
        
    response = conn.getresponse()
    rescode = response.status

    if rescode == 200:
        response_body = response.read()
        return rescode, json.loads(response_body.decode('utf-8'))
    else:
        return rescode, None

    # 녹음 파일 형식 mp3, aac, ac3, ogg, flac, wav파일 형식 가능
>>>>>>> b22f28c (bug fix)

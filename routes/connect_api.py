from fastapi import APIRouter, Depends, status, Response, HTTPException
import requests
import json

def get_bearer_token():
    url = 'https://tubeststvincent.azurewebsites.net/login'
    data = {"username": "widi", "password": "widi"}
    response = requests.post(url, data=data)
    jsonresponse = response.json()
    bearertoken = str(jsonresponse['access_token'])
    return bearertoken

def get_from_api(url: str):
    headers = {"Authorization": f'Bearer {get_bearer_token()}'}
    response = requests.get(url, headers=headers)
    jsonresponse = response.json()
    return jsonresponse
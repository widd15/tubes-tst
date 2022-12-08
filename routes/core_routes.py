from models.jwttoken import get_current_user
from fastapi import APIRouter, Body, HTTPException, Depends, Request, status, Path
from models.model import (User, cpu, gpu)
from database.database import *
from fastapi.encoders import jsonable_encoder
from routes.connect_api import get_from_api
import sys
import random

core_router = APIRouter()
sys.setrecursionlimit(100000)

@core_router.get('/best_recommendation/budget/{budget}')
async def recommend_from_budget(budget: int, current_user:User = Depends(get_current_user)):
    # Ngelist cpu dibawah budget 
    cpus = []
    for cpu in cpu_db.find():
        if (budget > parser_harga(cpu)):
            cpus.append(cpu_parser(cpu))
    # Ngelist gpu dibawah budget
    gpus = []
    for gpu in gpu_db.find():
        if (budget > parser_harga(gpu)):
            gpus.append(gpu_parser(gpu))

    max_score = 0
    recommendation = []

    for i in cpus:
        for j in gpus:
            if (combine_score(i,j) > max_score) and (harga_total(i,j) <= budget):
                max_score = combine_score(i,j)
                data = {
                    "Message": "Ini rekomendasi CPU dan GPU terbaik untuk anda",
                    "CPU": i['cpu'],
                    "GPU": j['gpu'],
                    "Total score": combine_score(i,j),
                    "Harga": harga_total(i,j)
                }
                recommendation.append(data)

    if recommendation:
        return recommendation[len(recommendation)-1]
    else:
        return {"Error": "Rekomendasi tidak bisa diberikan"}

@core_router.get('/best_recommendation/budget/cpu/{budget}/{brand}')
async def recommend_from_budgetandcpu(budget: int, brand: str, current_user:User = Depends(get_current_user)):
    # Ngelist cpu dengan model tertentu dibawah budget 
    cpus = []
    search = brand.upper().split()
    for cpu in cpu_db.find():
        if all(x in cpu['CPU'] for x in search) and (budget > parser_harga(cpu)):
            cpus.append(cpu_parser(cpu))
    # Ngelist gpu dibawah budget
    gpus = []
    for gpu in gpu_db.find():
        if (budget > parser_harga(gpu)):
            gpus.append(gpu_parser(gpu))
    
    max_score = 0

    recommendation = []

    for i in cpus:
        for j in gpus:
            if (combine_score(i,j) > max_score) and (harga_total(i,j) <= budget):
                max_score = combine_score(i,j)
                data = {
                    "Message": "Ini rekomendasi CPU dan GPU terbaik untuk anda",
                    "CPU": i['cpu'],
                    "GPU": j['gpu'],
                    "Total score": combine_score(i,j),
                    "Harga": harga_total(i,j)
                }
                recommendation.append(data)

    if recommendation:
        return recommendation[len(recommendation)-1]
    else:
        return {"Error": "Rekomendasi tidak bisa diberikan"}

@core_router.get('/best_recommendation/budget/gpu/{budget}/{brand}')
async def recommend_from_budgetandgpu(budget: int , brand: str, current_user:User = Depends(get_current_user)):
    # Ngelist cpu dibawah budget 
    cpus = []
    for cpu in cpu_db.find():
        if (budget > parser_harga(cpu)):
            cpus.append(cpu_parser(cpu))
    # Ngelist gpu dibawah budget
    gpus = []
    search = brand.upper().split()
    for gpu in gpu_db.find():
        if all(x in gpu['GPU'] for x in search) and (budget > parser_harga(gpu)):
            gpus.append(gpu_parser(gpu))

    max_score = 0
    recommendation = []

    for i in cpus:
        for j in gpus:
            if (combine_score(i,j) > max_score) and (harga_total(i,j) <= budget):
                max_score = combine_score(i,j)
                data = {
                    "Message": "Ini rekomendasi CPU dan GPU terbaik untuk anda",
                    "CPU": i['cpu'],
                    "GPU": j['gpu'],
                    "Total score": combine_score(i,j),
                    "Harga": harga_total(i,j)
                }
                recommendation.append(data)

    if recommendation:
        return recommendation[len(recommendation)-1]
    else:
        return {"Error": "Rekomendasi tidak bisa diberikan"}

@core_router.get('/list_recommendation/{budget}')
async def list_recommend_from_budget(budget: int, current_user:User = Depends(get_current_user)):
    # Ngelist cpu dibawah budget 
    cpus = []
    for cpu in cpu_db.find():
        if (budget > parser_harga(cpu)):
            cpus.append(cpu_parser(cpu))
    # Ngelist gpu dibawah budget
    gpus = []
    for gpu in gpu_db.find():
        if (budget > parser_harga(gpu)):
            gpus.append(gpu_parser(gpu))

    recommendation = []

    for i in cpus:
        for j in gpus:
            if (harga_total(i,j) > 0.9*budget) and (harga_total(i,j) <= budget):
                data = {
                    "CPU": i['cpu'],
                    "GPU": j['gpu'],
                    "Total score": combine_score(i,j),
                    "Harga": harga_total(i,j)
                }
                recommendation.append(data)

    show_recommendation = []
    loop = 3
    if len(recommendation) > 5:
        loop = round(len(recommendation)/2)
    elif len(recommendation) > 15:
        loop = round(len(recommendation)/3)
    else:
        loop = round(len(recommendation)/4)
    
    for i in range(loop):
        show_recommendation.append(recommendation[random.randrange(len(recommendation))])

    if recommendation:
        return show_recommendation
    else:
        return {"Error": "Rekomendasi tidak bisa diberikan"}

@core_router.get('/list_recommendation/game/{spec}')
async def recommendation_from_gamespec(spec: str, current_user:User = Depends(get_current_user)):
    if spec == "Very Low":
        return await list_recommend_from_budget(6000000)
    elif spec == "Low":
        return await list_recommend_from_budget(10000000)
    elif spec == "Average": 
        return await list_recommend_from_budget(15000000)
    elif spec == "High":
        return await list_recommend_from_budget(30000000) 
    else:
        return {"Error": "Spec dari game tidak valid"}   

@core_router.get('/can_run_thisgame/{budget}/{game_name}')
async def can_run_game(budget:int, game_name: str, current_user:User = Depends(get_current_user)):
    game_name = game_name.replace(" ","%20")
    url = f'https://tubeststvincent.azurewebsites.net/game-specs/get-specs/{game_name}'
    spec = get_from_api(url)
    if budget < 6000000:
        if spec == "Very Low":
            recommend_pc = await recommend_from_budget(random.randrange(1000000,6000000))
            data = [{"Message": "You cannot play this game",
            "Recomended spec": spec}, recommend_pc]
            return data
        elif spec == "Low":
            recommend_pc = await recommend_from_budget(random.randrange(6000000,10000000))
            data = [{"Message": "You cannot play this game",
            "Recomended spec": spec}, recommend_pc]
            return data
        elif spec == "Average":
            recommend_pc = await recommend_from_budget(random.randrange(10000000,15000000))
            data = [{"Message": "You cannot play this game",
            "Recomended spec": spec}, recommend_pc]
            return data
        elif spec == "High":
            recommend_pc = await recommend_from_budget(random.randrange(15000000,30000000))
            data = [{"Message": "You cannot play this game",
            "Recomended spec": spec}, recommend_pc]
            return data
    elif budget >= 6000000 and budget < 10000000 and spec == "Very Low":
        return {"Message": "Yes you can play this game"}
    elif budget >= 10000000 and budget < 15000000 and (spec == "Low" or spec == "Very Low"):
        return {"Message": "Yes you can play this game"}
    elif budget >= 15000000 and budget < 30000000 and (spec == "Low" or spec == "Very Low" or spec == "Average"):
        return {"Message": "Yes you can play this game"}
    elif budget >= 30000000 and (spec == "Average" or spec == "Very Low" or spec == "High"):
        return {"Message": "Yes you can play this game"}
    else:
        return {"Message": "You cannot play this game",
            "Recomended spec": spec}
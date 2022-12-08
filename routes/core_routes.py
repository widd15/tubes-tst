from models.jwttoken import get_current_user
from fastapi import APIRouter, Body, HTTPException, Depends, Request, status, Path
from models.model import (User, cpu, gpu)
from database.database import *
from fastapi.encoders import jsonable_encoder
import sys
import random

core_router = APIRouter()
sys.setrecursionlimit(100000)

@core_router.get('/best_recommendation/budget/{budget}')
def recomend_from_budget(budget: int):
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
def recomend_from_budget(budget: int,brand: str):
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
def recomend_from_budget(budget: int ,brand: str):
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

@core_router.get('/list_recommendation_from_budget')
def recomend_from_budget(budget: int):
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

    recomendation = []

    for i in cpus:
        for j in gpus:
            if (harga_total(i,j) > 0.9*budget) and (harga_total(i,j) <= budget):
                data = {
                    "CPU": i['cpu'],
                    "GPU": j['gpu'],
                    "Total score": combine_score(i,j),
                    "Harga": harga_total(i,j)
                }
                recomendation.append(data)

    return recomendation


from models.jwttoken import get_current_user
from fastapi import APIRouter, Body, HTTPException, Depends, Request, status
from models.model import (User, cpu, gpu)
from database.database import *
from fastapi.encoders import jsonable_encoder
import sys

parts_router = APIRouter()
sys.setrecursionlimit(100000)

# GET
@parts_router.get('/cpus')
def get_all_cpus(current_user:User = Depends(get_current_user)):
    cpus = get_all_cpu()
    if cpus:
        return cpus

@parts_router.get('/gpus')
def get_all_gpus(current_user:User = Depends(get_current_user)):
    gpus = get_all_gpu()
    if gpus:
        return gpus

@parts_router.get('/cpus/getbyid/{id}')
async def get_cpus_from_id(id: str, current_user:User = Depends(get_current_user)):
    cpu = await get_cpu_by_id(id)
    if cpu:
        return cpu

@parts_router.get('/gpus/getbyid{id}')
async def get_gpus_from_id(current_user:User = Depends(get_current_user)):
    gpu = await get_gpu_by_id(id)
    if gpu:
        return gpu

@parts_router.get('/cpus/getbyname/{nama_cpu}')
def get_cpu_from_name(cpu_name: str, current_user:User = Depends(get_current_user)):
    cpus = []
    search = cpu_name.upper().split()
    for cpu in cputest_db.find():
        if all(x in cpu['CPU'] for x in search):
            cpus.append(cpu_parser(cpu))
    return cpus

@parts_router.get('/gpus/getbyname/{nama_gpu}')
def get_gpu_from_name(gpu_name: str, current_user:User = Depends(get_current_user)):
    gpus = []
    search = gpu_name.upper().split()
    for gpu in gpu_db.find():
        if all(x in gpu['GPU'] for x in search):
            gpus.append(gpu_parser(gpu))
    return gpus
    
@parts_router.get('/cpus/under/{harga}')
def get_cpu_under_price(harga: int):
    cpus = []
    for cpu in cpu_db.find():
        if (parser_harga(cpu) < harga):
            print(parser_harga(cpu))
            cpus.append(cpu_parser(cpu))
    return cpus

@parts_router.get('/gpus/under/{harga}')
def get_gpu_under_price(harga: int):
    gpus = []
    for gpu in gpu_db.find():
        if (parser_harga(gpu) < harga):
            gpus.append(gpu_parser(gpu))
    return gpus

# POST
@parts_router.post('/cpus/add')
async def add_cpu_data(cpu: cpu = Body(...), current_user:User = Depends(get_current_user)):
    cpu = jsonable_encoder(cpu)
    new_cpu = await add_cpu(cpu)
    return {"CPU":"Added"}

@parts_router.post('/gpus/add')
async def add_gpu_data(gpu: gpu = Body(...), current_user:User = Depends(get_current_user)):
    gpu = jsonable_encoder(gpu)
    new_gpu = await add_gpu(gpu)
    return {"GPU":"Added"}

# PUT
@parts_router.put('/cpus/update/{id}')
async def update_cpu_data(id: str, cpu: cpu = Body(...), current_user:User = Depends(get_current_user)):
    cpu = {k: v for k, v in cpu.dict().items() if v is not None}
    updated_cpu = await update_cpu(id, cpu)
    if updated_cpu :
        return {"Message": "Data CPU berhasil diubah"} 
    return {"Error":"Data CPU gagal diubah"}

@parts_router.put('/gpus/update/{id}')
async def update_gpu_data(id: str, gpu: gpu = Body(...), current_user:User = Depends(get_current_user)):
    gpu = {k: v for k, v in gpu.dict().items() if v is not None}
    updated_gpu = await update_gpu(id, gpu)
    if updated_gpu :
        return {"Message": "Data GPU berhasil diubah"} 
    return {"Error":"Data GPU gagal diubah"}

# DELETE
@parts_router.delete('/cpus/delete/{id}')
async def delete_cpu_data(id: str, current_user:User = Depends(get_current_user)):
    await delete_cpu(id)
    return {"CPU":"Deleted"}

@parts_router.delete('/gpus/delete/{id}')
async def delete_gpu_data(id: str, current_user:User = Depends(get_current_user)):
    await delete_gpu(id)
    return {"GPU":"Deleted"}


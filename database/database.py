from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from models.model import *

mongodb_uri = 'mongodb+srv://widhys15:l1pW8mRA13f1xHei@apitst.jxllzys.mongodb.net/?retryWrites=true&w=majority'
port = 8000
client = MongoClient(mongodb_uri, port)

user_db = client["User"]

parts_db = client["parts"]
cpu_db = parts_db["cpu"]
gpu_db = parts_db["gpu"]
cputest_db = parts_db["cpu_test"]


# CPU
# Convert data cpu dari database ke python
def cpu_parser(cpu) -> dict:
    return {
        "id": str(cpu["_id"]),
        "cpu": cpu["CPU"],
        "harga": cpu["Harga"],
        "score": cpu["Score"]
    }

def cpu_serializer(cpus) -> list:
    return [cpu_parser(cpu) for cpu in cpus]

# Mengambil semua list cpu
def get_all_cpu():
    cpus = []
    for cpu in cpu_db.find():
        cpus.append(cpu_parser(cpu))
    return cpus

# Mengambil nama cpu berdasarkan idnya
async def get_cpu_by_id(id: str) -> dict:
    cpu = cpu_db.find_one({"_id": ObjectId(id)})
    if cpu:
        return cpu_parser(cpu)

# Menambah cpu ke database
async def add_cpu(cpu: dict) -> dict:
    cpu = cpu_db.insert_one(cpu)
    new_cpu = cpu_db.find_one({"_id": cpu.inserted_id})
    return cpu_parser(new_cpu)

# Update informasi cpu yang sudah ada
async def update_cpu(id: str, data: dict):
    if len(data) < 1:
        return False

    cpu = cpu_db.find_one({"_id": ObjectId(id)})

    if cpu:
        updated_cpu = cpu_db.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_cpu:
            return True
        return False

# Menghapus data cpu dari database
async def delete_cpu(id: str):
    cpu = cpu_db.find_one({"_id": ObjectId(id)})
    if cpu:
        cpu_db.delete_one({"_id": ObjectId(id)})
        return True

# GPU
# Convert data gpu dari database ke python
def gpu_parser(gpu) -> dict:
    return {
        "id": str(gpu["_id"]),
        "gpu": gpu["GPU"],
        "harga": gpu["Harga"],
        "score": gpu["Score"]
    }

def gpu_serializer(gpus) -> list:
    return [gpu_parser(gpu) for gpu in gpus]

# Mengambil semua list gpu
def get_all_gpu():
    gpus = []
    for gpu in gpu_db.find():
        gpus.append(gpu_parser(gpu))
    return gpus

# Mengambil nama gpu berdasarkan idnya
async def get_gpu_by_id(id: str) -> dict:
    gpu = gpu_db.find_one({"_id": ObjectId(id)})
    if gpu:
        return gpu_parser(gpu)

# Menambah gpu ke database
async def add_gpu(gpu: dict) -> dict:
    gpu = gpu_db.insert_one(gpu)
    new_gpu = gpu_db.find_one({"_id": gpu.inserted_id})
    return gpu_parser(new_gpu)

# Update informasi gpu yang sudah ada
async def update_gpu(id: str, data:dict):
    if len(data) < 1:
        return False

    gpu = gpu_db.find_one({"_id": ObjectId(id)})

    if gpu:
        updated_gpu = gpu_db.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_gpu:
            return True
        return False

# Menghapus data gpu dari database
async def delete_gpu(id: str):
    gpu = gpu_db.find_one({"_id": ObjectId(id)})
    if gpu:
        gpu_db.delete_one({"_id": ObjectId(id)})
        return True

# # CPU Test
# # Convert data cpu dari database ke python
# def cpu_parser(cpu) -> dict:
#     return {
#         "id": str(cpu["_id"]),
#         "cpu": cpu["CPU"],
#         "harga": cpu["Harga"],
#         "score": cpu["Score"]
#     }

# def cpu_serializer(cpus) -> list:
#     return [cpu_parser(cpu) for cpu in cpus]

# # Mengambil semua list cpu
# def get_all_cpu():
#     cpus = []
#     for cpu in cputest_db.find():
#         cpus.append(cpu_parser(cpu))
#     return cpus

# # Mengambil nama cpu berdasarkan idnya
# async def get_cpu_by_id(id: str) -> dict:
#     cpu = cputest_db.find_one({"_id": ObjectId(id)})
#     if cpu:
#         return cpu_parser(cpu)

# # Menambah cpu ke database
# async def add_cpu(cpu: dict) -> dict:
#     cpu = cputest_db.insert_one(cpu)
#     new_cpu = cputest_db.find_one({"_id": cpu.inserted_id})
#     cpu_parser(new_cpu)
#     return {"Message": "Data CPU berhasil ditambahkan ke database"}

# # Update informasi cpu yang sudah ada
# async def update_cpu(id: str, data: dict):
#     if len(data) < 1:
#         return False

#     cpu = cputest_db.find_one({"_id": ObjectId(id)})

#     if cpu:
#         updated_cpu = cputest_db.update_one(
#             {"_id": ObjectId(id)}, {"$set": data}
#         )
#         if updated_cpu:
#             return True
#         return False

# # Menghapus data cpu dari database
# async def delete_cpu(id: str):
#     cpu = cputest_db.find_one({"_id": ObjectId(id)})
#     if cpu:
#         cputest_db.delete_one({"_id": ObjectId(id)})
#         return {"Message": "Data CPU berhasil dihapus"} 
#     return {"Error": "Data CPU tidak ditemukan di database"}
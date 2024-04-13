import resource
import pickle
import time
import os

def folderExists(folderName):
    os.makedirs(folderName, exist_ok=True)

def fileExists(filePath):
    return os.path.exists(filePath)

def timer():
    return time.time()

def getExecutionTime(start_time, end_time):
    return end_time - start_time

def writeExecutionTime(filePath, executionTime, params):
    with open(filePath, 'w') as file:
        str = f"Время выполнения кода: {executionTime} секунд c параметрами {params}"
        file.write(str)
    print(str)

def mem():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

def getMemUsage(mem_before, mem_after):
    mem = mem_after - mem_before
    if mem < 1024:
        return str(mem) + ' Кб'
    else:
        return str(mem/1024) + ' Мб'

def writeMemUsage(filePath, mem_usage, params):
    with open(filePath, 'w') as file:
      file.write(f"Время выполнения кода: {mem_usage} секунд c параметрами {params}")
    print(f"Потребление памяти: {mem_usage}")

def pickle_dump(filePath, data):
    with open(filePath, 'wb') as f:
        pickle.dump(data, f)

def pikcle_load(filePath):
    with open(filePath, 'rb') as file:
        return pickle.load(file)
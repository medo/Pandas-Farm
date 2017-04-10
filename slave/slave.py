from common.serializer import serialize, deserialize
import multiprocessing
import time, xmlrpc.client
import numpy as np

serverProxy = xmlrpc.client.ServerProxy('http://127.0.0.1:5555', use_builtin_types=True)
n_process = multiprocessing.cpu_count()

def parallelize_dataframe(tasks, num_partitions, func):
    pool = multiprocessing.Pool(num_partitions)
    result = pool.map(func, tasks)
    pool.close()
    pool.join()
    return result

def execute_function(task):
    return {    "partition_id": task["partition_id"],
                "result": deserialize(task["func"])(task["df"])
            }

def start():
    serverProxy.hand_shake(n_process)
    while True:
        time.sleep(1)
        res = serverProxy.offer_resources(n_process)
        tasks = deserialize(res)
        print(tasks)
        for task in tasks:
            task['func'] = serialize(task['func'])
        if tasks:
            results = parallelize_dataframe(tasks, n_process, execute_function)
            for result in results:
                print(type(result["result"]))
                serverProxy.submit_result(result["partition_id"], serialize(result["result"]))


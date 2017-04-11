from common.serializer import serialize, deserialize
import multiprocessing, os, concurrent.futures
import time, xmlrpc.client
import numpy as np

HOST = os.getenv('CL_MASTER_HOST', 'http://127.0.0.1')
PORT = os.getenv('CL_MASTER_PORT', "5555")
serverProxy = xmlrpc.client.ServerProxy("http://%s:%s" % (HOST, PORT), use_builtin_types=True)
n_process = multiprocessing.cpu_count()

def parallelize_dataframe(tasks, num_partitions, func):
    with concurrent.futures.ThreadPoolExecutor(n_process) as executor:
        result = executor.map(func, tasks)
        return result

def execute_function(task):
    return {    "partition_id": task["partition_id"],
                "result": deserialize(task["func"])(task["df"])
            }

def start():
    print("Connected to: %s:%s" % (HOST, PORT))
    serverProxy.hand_shake(n_process)
    while True:
        time.sleep(1)
        res = serverProxy.offer_resources(n_process)
        tasks = deserialize(res)
        for task in tasks:
            task['func'] = serialize(task['func'])
        if tasks:
            print("Executing Partitions: %s" % str(list(map(lambda t: t["partition_id"], tasks))))
            results = parallelize_dataframe(tasks, n_process, execute_function)
            for result in results:
                serverProxy.submit_result(result["partition_id"], serialize(result["result"]))


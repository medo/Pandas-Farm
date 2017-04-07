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
	return {	"partition_id": task["partition_id"],
				"result": task["func"](task["df"])
			}

def start():
	serverProxy.hand_shake(n_process)
	while True:
		time.sleep(1)
		tasks = deserialize(serverProxy.offer_resources(n_process))
		if tasks: print(tasks)
		if tasks:
			results = parallelize_dataframe(tasks, n_process, execute_function)
			print(results)
			for result in results:
				print(result)
				serverProxy.submit_result(result["partition_id"], serialize(int(result["result"])))


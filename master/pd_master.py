from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.client import Binary
import numpy as np
import dill


PORT = 5555
HOST = "127.0.0.1"
ENDPOINT = "RPC2"

class RequestHandler(SimpleXMLRPCRequestHandler):
    # rpc_paths = ('RPC2',)
    def log_message(self, format, *args):
    	pass
    	

class ServerHandler:
	
	def __init__(self):
		self.task_queue = []
		self.total_partitions = 0
		self.TASK_ID = 0
		self.PARTITION_ID = 0
		self.result = {}

	def hand_shake(self, paritions):
		self.total_partitions += paritions
		print("Current Paritions " + str(self.total_partitions))

	def schedule_task(self, df, func):
		self.TASK_ID += 1
		df = dill.loads(df)
		func = self.__deserialize_function(func)
		task = {"df": df, "func": func, "priority": 0, "task_id": self.TASK_ID}
		splitted_task = self.__split_task(task)
		self.task_queue += splitted_task
		return self.TASK_ID

	def submit_result(self, partition_id, res):
		matched = list(filter(lambda t: t["partition_id"] == partition_id, self.task_queue))
		matched = matched[0] if matched else None
		if matched:
			self.task_queue.remove(matched)
			self.result.setdefault(matched["task_id"], [])
			self.result[matched["task_id"]].append(dill.loads(res))
		print(self.result)

	def offer_resources(self, partitions):
		assigned_tasks = []
		for task in sorted(self.task_queue, key=lambda t: t["priority"])[:partitions]:
			task["priority"] += 1
			assigned_tasks.append(task)
		return dill.dumps(assigned_tasks)

	def __resplit():
		pass

	# TODO limit the scope passed to function
	def __deserialize_function(self, func_code):
		return dill.loads(func_code)

	def __split_task(self, task):
		df_split = np.array_split(task["df"], self.total_partitions)
		tasks = []
		for df in df_split:
			self.PARTITION_ID += 1
			tasks.append({	"df": df,
		 					"func": task["func"],
		  					"priority": task["priority"],
		  					"task_id": task["task_id"],
		  					"partition_id": self.PARTITION_ID})
		return tasks



# Create server
server = SimpleXMLRPCServer((HOST, PORT),
 							requestHandler=RequestHandler,
							allow_none=True, use_builtin_types=True)
server.register_instance(ServerHandler())
print("Server is listening on " + HOST + ":" + str(PORT) + "/" + ENDPOINT)
server.serve_forever()


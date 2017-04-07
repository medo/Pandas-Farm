import pandas as pd
from common.serializer import serialize, deserialize
import xmlrpc.client

class ClusterPandas:

    def __init__(self, master_url='http://127.0.0.1:5555'):
        self.master_url = master_url
        self.master = xmlrpc.client.ServerProxy(self.master_url, use_builtin_types=True)

    def paralleize(self, data, func, partitions=8):
        return self.master.schedule_task(serialize(data), serialize(func), partitions)

    def collect(self, task_id):
        return deserialize(self.master.collect(task_id))

    def ready(self, task_id):
        return self.master.ready(task_id)



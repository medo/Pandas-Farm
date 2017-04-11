import pandas as pd
from common.serializer import serialize, deserialize
import xmlrpc.client

# In case no merger function is passed assume dataframe concatenation
def default_merger(x, y):
	import pandas as pd
	return pd.concat([x, y])

class ClusterPandas:

    def __init__(self, master_url='http://127.0.0.1:5555'):
        self.master_url = master_url
        self.master = xmlrpc.client.ServerProxy(self.master_url, use_builtin_types=True, allow_none=True)

    def paralleize(self, data, apply, partitions=0, merge=default_merger):
        return self.master.schedule_task(serialize(data), serialize(apply), partitions, serialize(merge))

    def collect(self, task_id):
        return deserialize(self.master.collect(task_id))

    def ready(self, task_id):
        return self.master.ready(task_id)

    def progress(self, task_id):
    	return self.master.progress(task_id)

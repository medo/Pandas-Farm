import dill

def serialize(obj):
	return dill.dumps(obj)

def deserialize(data):
	return dill.loads(data)

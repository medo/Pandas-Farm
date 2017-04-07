class Scheduler:

	def __init__(self):
		# User Redis instead
		self.task_queue = []

	def schedule_task(self, task):
		self.task_queue.append(task)

	def schedule_tasks(self, tasks):
		for task in tasks:
			self.schedule_task(task)

	def select_tasks(self, n_tasks, resource_params=None):
		assigned_tasks = []
		for task in sorted(self.task_queue, key=lambda t: t["priority"])[:n_tasks]:
			task["priority"] += 1
			assigned_tasks.append(task)
		return assigned_tasks

	def finish_task(self, partition_id):
		matched = list(filter(lambda t: t["partition_id"] == partition_id, self.task_queue))
		matched = matched[0] if matched else None
		if matched:
			self.task_queue.remove(matched)
			return matched['task_id']
		return None

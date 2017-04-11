import numpy as np
import copy

PARTITION_ID = 0

def split_task(task, partitions):
    global PARTITION_ID
    df_split = np.array_split(task["df"], partitions)
    tasks = []
    for df in df_split:
        PARTITION_ID += 1
        subtask = copy.deepcopy(task)
        subtask["df"] = df
        subtask["partition_id"] = PARTITION_ID
        tasks.append(subtask)
    return tasks
import numpy as np

PARTITION_ID = 0


def split_task(task, partitions):
    global PARTITION_ID
    print(task)
    df_split = np.array_split(task["df"], partitions)
    tasks = []
    for df in df_split:
        PARTITION_ID += 1
        tasks.append({  "df": df,
                    "func": task["func"],
                    "priority": task["priority"],
                    "task_id": task["task_id"],
                    "partition_id": PARTITION_ID})
    return tasks
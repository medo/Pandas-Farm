# Panda Farm

An easy tool to parallelize and distribute your pandas dataframe operation across your cluster or your personal machines.

## Getting Started

### Master

In order to use Panda Farm you need a netwrok accessible master running. If you have docker installed in the master machine, just run

`docker run -p 5555:5555 medo/farm-master`

### Slave

Now the master is running, and you can schedule operations. In order to process operations you need at least one slave running. In your slave machine run

`docker run -e "CL_MASTER_HOST=<MASTER_IP>" -e "CL_MASTER_PORT=5555"  medo/farm-slave`

### Driver

Now you ready to play with Panda Farm. All you need to do is create a function that takes a dataframe and returns a dataframe.

```python
import pandas.rpy.common as rcom
iris = rcom.load_data('iris')

def area(df):
  df['Sepal.Area'] = df['Sepal.Width'] * df['Sepal.Length']
  return df

```

And now run your function on the iris dataframe

```python
from clpandas.driver import PandaFarm

pf = PandaFarm('<MASTER_HOST>')

job = pf.parallelize(iris, area, 10)

```

You can check the progress of the operatiosn

```python
print("Progress = %d / 100" % pf.progress(job))
```

To get the result of the operation

```python
result = pf.collect(job)
```

The result we get here is a single dataframe, However, Panda Farm runs a merge function on partiions to reduce the paritions into a single result, by default the function is `pd.concat`. You can get the raw result of the paritions or pass a different merge function

```python
pf.parallelize(iris, apply = area, merge = None)

```

## Manage Dependenices

### Run inside your own Containe

## Provision slaves with AWS Spot Instances


## Architecture

## Why I built this

## Future Work

- Automatically pass a docker container as a dependency of a function instead of restarting the slaves

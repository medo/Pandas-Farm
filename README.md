# Panda Farm

An easy tool to parallelize and distribute your python pandas dataframe operation across your cluster or your personal machines. Although, in theory, you can distribute arbitrary python functions with Panda-Farm but it was built and tested to work with Pandas Dataframes

## Getting Started

To quickly get started with Panda Farm you need 3 instacens running
- Master: to mange, schedule and relay the data
- Slave(s): to compute the functions
- Driver: from which you can submit code to Panda Farm cluster 

### Master

In order to use Panda Farm you need a netwrok accessible master running. If you have docker installed in the master machine, just run

```bash
docker run -p 5555:5555 medo/farm-master
```

### Slave

Now the master is running, and you can schedule operations. In order to process operations you need at least one slave running. In your slave machine run

```bash 
docker run -e "CL_MASTER_HOST=<MASTER_IP>" -e "CL_MASTER_PORT=5555"  medo/farm-slave
```

### Driver

Now you ready to play with Panda Farm. All you need to do is create a function that takes a dataframe and returns a dataframe.

```python
import pandas.rpy.common as rcom
iris = rcom.load_data('iris')

def area(df):
  df['Sepal.Area'] = df['Sepal.Width'] * df['Sepal.Length']
  return df

```

Let's try our function on iris dataset.

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

In order to be able to install libraries in the slaves. You will need to create your own docker image, push it to the registery and then you can use your image to install the dependecies.

### Run inside your own Container

Create a Dockerfile

```bash
FROM medo/farm-slave

MAINTAINER <example@mail.com>

RUN pip3 install nltk
```

Now build the image

```bash
docker build -t <image_name> . 
```

Push it to the registery

```bash
docker push <image_name>
```

### Run the image on the slaves

Now you need to run your image on the slaves

```bash
docker run -e "CL_MASTER_HOST=<MASTER_IP>" -e "CL_MASTER_PORT=5555"  medo/farm-slave
```

### Run watchtower

Watch tower is a docker image that enables you to automatically update your containers. check this post http://www.ecliptik.com/Automating-Container-Updates-With-Watchtower/

All you need to do is to run watchtower container on the slaves

```bash
docker run -d  --name watchtower  -v /var/run/docker.sock:/var/run/docker.sock centurylink/watchtower --interval 10 <image_name>
```

if you don't specify `<image_name>` then all the container on the slave machine will be included in the update script

### Update your Image

Now you have everything set up. All you need to do to install new dependencies for your script is to install the dependency on the docker container and push it with the same name  `<image_name>` 

## Provision slaves with AWS Spot Instances

TODO...

## Architecture

![alt tag](https://github.com/medo/Pandas-Farm/blob/master/architecture-diagram.jpeg)

## Why I built this

## Future Work

- Support different Python versions
- Automatically pass a docker container as a dependency of a function instead of restarting the slaves
- Shadow Master failure recovery
- Effiecient Distribute Merging

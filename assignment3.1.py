#!/usr/bin/env python
# coding: utf-8

# # Assignment 3
# 
# Welcome to Assignment 3. This will be even more fun. Now we will calculate statistical measures on the test data you have created.
# 
# YOU ARE NOT ALLOWED TO USE ANY OTHER 3RD PARTY LIBRARIES LIKE PANDAS. PLEASE ONLY MODIFY CONTENT INSIDE THE FUNCTION SKELETONS
# Please read why: https://www.coursera.org/learn/exploring-visualizing-iot-data/discussions/weeks/3/threads/skjCbNgeEeapeQ5W6suLkA
# . Just make sure you hit the play button on each cell from top to down. There are seven functions you have to implement. Please also make sure than on each change on a function you hit the play button again on the corresponding cell to make it available to the rest of this notebook.
# Please also make sure to only implement the function bodies and DON'T add any additional code outside functions since this might confuse the autograder.
# 
# So the function below is used to make it easy for you to create a data frame from a cloudant data frame using the so called "DataSource" which is some sort of a plugin which allows ApacheSpark to use different data sources.
# 

# All functions can be implemented using DataFrames, ApacheSparkSQL or RDDs. We are only interested in the result. You are given the reference to the data frame in the "df" parameter and in case you want to use SQL just use the "spark" parameter which is a reference to the global SparkSession object. Finally if you want to use RDDs just use "df.rdd" for obtaining a reference to the underlying RDD object. 
# 
# Let's start with the first function. Please calculate the minimal temperature for the test data set you have created. We've provided a little skeleton for you in case you want to use SQL. You can use this skeleton for all subsequent functions. Everything can be implemented using SQL only if you like.

# In[40]:


def minTemperature(df,spark):
    #TODO Please enter your code here, you are not required to use the template code below
    #some reference: https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame
#     return df.agg({"temperature": "min"}).collect()[0]["min(temperature)"]
    return spark.sql("SELECT min(temperature) as mintemp from washing").first().mintemp


# Please now do the same for the mean of the temperature

# In[41]:


def meanTemperature(df,spark):
    #TODO Please enter your code here, you are not required to use the template code below
    #some reference: https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame
#     return df.agg({"temperature": "avg"}).collect()[0]["avg(temperature)"]
    return spark.sql("SELECT avg(temperature) as meantemp from washing").first().meantemp


# Please now do the same for the maximum of the temperature

# In[42]:


def maxTemperature(df,spark):
    #TODO Please enter your code here, you are not required to use the template code below
    #some reference: https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame
#     return df.agg({"temperature": "max"}).collect()[0]["max(temperature)"]
    return spark.sql("SELECT max(temperature) as maxtemp from washing").first().maxtemp


# Please now do the same for the standard deviation of the temperature

# In[43]:


def sdTemperature(df,spark):
    #TODO Please enter your code here, you are not required to use the template code below
    #some reference: https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame
    #https://spark.apache.org/docs/2.3.0/api/sql/
#     from math import sqrt
#     rows = df.select('temperature').rdd 
#     teptRows = rows.map(lambda x : x["temperature"])
#     temp = teptRows.filter(lambda x: x is not None).filter(lambda x: x != "")
#     n = float(temp.count())
#     sum=temp.sum()
#     mean =sum/n
#     sd=sqrt(temp.map(lambda x : pow(x-mean,2)).sum()/n)
#     return sd
    return spark.sql("SELECT stddev(temperature) as stdTemp from washing").first().stdTemp


# Please now do the same for the skew of the temperature. Since the SQL statement for this is a bit more complicated we've provided a skeleton for you. You have to insert custom code at four position in order to make the function work. Alternatively you can also remove everything and implement if on your own. Note that we are making use of two previously defined functions, so please make sure they are correct. Also note that we are making use of python's string formatting capabilitis where the results of the two function calls to "meanTemperature" and "sdTemperature" are inserted at the "%s" symbols in the SQL string.

# In[61]:


def skewTemperature(df,spark):
#     from math import sqrt
#     rows = df.select('temperature').rdd 
#     teptRows = rows.map(lambda x : x["temperature"])
#     temp = teptRows.filter(lambda x: x is not None).filter(lambda x: x != "")
#     n = float(temp.count())
#     sum=temp.sum()
#     mean =sum/n
#     sd=sqrt(temp.map(lambda x : pow(x-mean,2)).sum()/n)
#     return n*(temp.map(lambda x:pow(x-mean,3)/pow(sd,3)).sum())/(float(n-1)*float(n-2))
    return spark.sql("""
                        SELECT 
                            (
                                1/count(temperature)
                            ) *
                            SUM (
                                POWER(temperature-%s,3)/POWER(%s,3)
                            )

                            as skewTemp from washing
                                            """ %(meanTemperature(df,spark),sdTemperature(df,spark))).first().skewTemp


# Kurtosis is the 4th statistical moment, so if you are smart you can make use of the code for skew which is the 3rd statistical moment. Actually only two things are different.

# In[62]:


def kurtosisTemperature(df,spark):
#     from math import sqrt
#     rows = df.select('temperature').rdd 
#     teptRows = rows.map(lambda x : x["temperature"])
#     temp = teptRows.filter(lambda x: x is not None).filter(lambda x: x != "")
#     n = float(temp.count())
#     sum=temp.sum()
#     mean =sum/n
#     sd=sqrt(temp.map(lambda x : pow(x-mean,2)).sum()/n)
#     return temp.map(lambda x:pow(x-mean,4)).sum()/(pow(sd,4)*(n))
    return spark.sql("""
            SELECT 
                (
                    1/count(temperature)
                ) *
                SUM (
                    POWER(temperature-%s,4)/POWER(%s,4)
                )

            as kurtTemp from washing
                    """ %(meanTemperature(df,spark),sdTemperature(df,spark))).first().kurtTemp


# Just a hint. This can be solved easily using SQL as well, but as shown in the lecture also using RDDs.

# In[46]:


def correlationTemperatureHardness(df,spark):
    #TODO Please enter your code here, you are not required to use the template code below
    #some reference: https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame
    #https://spark.apache.org/docs/2.3.0/api/sql/
#     from math import sqrt
#     rowsT = df.select('temperature').rdd 
#     teptRows = rowsT.map(lambda x : x["temperature"])
#     temp = teptRows.filter(lambda x: x is not None).filter(lambda x: x != "")
#     rowsH = df.select('hardness').rdd
#     hardRows = rowsH.map(lambda x : x["hardness"])
#     hard = rowsH.filter(lambda x: x is not None).filter(lambda x: x != "")
#     n = float(temp.count())
#     totalT=temp.sum()
#     totalH=hard.sum()
#     meanT =totalT/n
#     meanH = totalH/n
#     cov = temp.zip(hard).map(lambda x,y : (x-meant)*(y-meanh)).sum()/n  
#     sd1 = sqrt(temp.map(lambda x : pow(x-meant,2)).sum()/n)
#     sd2 = sqrt(hard.map(lambda x : pow(x-meanh,2)).sum()/n)
#     corr = cov12 / (sd1 * sd2)
    #corr12
    return df.stat.corr("temperature", "hardness")


# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED
# #axx
# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED

# Now it is time to grab a PARQUET file and create a dataframe out of it. Using SparkSQL you can handle it like a database. 

# In[47]:


get_ipython().system('wget https://github.com/IBM/coursera/blob/master/coursera_ds/washing.parquet?raw=true')
get_ipython().system('mv washing.parquet?raw=true washing.parquet')


# In[48]:


df = spark.read.parquet('washing.parquet')
df.createOrReplaceTempView('washing')
df.show()


# Now it is time to connect to the object store and read a PARQUET file and create a dataframe out of it. We've created that data for you already. Using SparkSQL you can handle it like a database.

# In[49]:


import ibmos2spark

# @hidden_cell
credentials = {
    'endpoint': 'https://s3-api.us-geo.objectstorage.service.networklayer.com',
    'api_key': 'PUJMZf9PLqN4y-6NUtVlEuq6zFoWhfuecFVMYLBrkxrT',
    'service_id': 'iam-ServiceId-9cd8e66e-3bb4-495a-807a-588692cca4d0',
    'iam_service_endpoint': 'https://iam.bluemix.net/oidc/token'}

configuration_name = 'os_b0f1407510994fd1b793b85137baafb8_configs'
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name, 'bluemix_cos')

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
# Since JSON data can be semi-structured and contain additional metadata, it is possible that you might face issues with the DataFrame layout.
# Please read the documentation of 'SparkSession.read()' to learn more about the possibilities to adjust the data loading.
# PySpark documentation: http://spark.apache.org/docs/2.0.2/api/python/pyspark.sql.html#pyspark.sql.DataFrameReader.json

df = spark.read.parquet(cos.url('washing.parquet', 'courseradsnew-donotdelete-pr-1hffrnl2pprwut'))
df.createOrReplaceTempView('washing')
df.show()


# In[50]:


minTemperature(df,spark)


# In[51]:


meanTemperature(df,spark)


# In[52]:


maxTemperature(df,spark)


# In[53]:


sdTemperature(df,spark)


# In[60]:


skewTemperature(df,spark)


# In[63]:


kurtosisTemperature(df,spark)


# In[56]:


correlationTemperatureHardness(df,spark)


# Congratulations, you are done, please download this notebook as python file using the export function and submit is to the gader using the filename "assignment3.1.py"

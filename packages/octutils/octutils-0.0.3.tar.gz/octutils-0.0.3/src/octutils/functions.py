#!/usr/bin/env python
# coding: utf-8

# ## functions
# 
# New notebook

# In[1]:


import sempy.fabric as fabric 
from datetime import datetime
from notebookutils import mssparkutils
import json
import pytz


# In[2]:


def get_executer_alias():
    try:
        executing_user = mssparkutils.env.getUserName()
        at_pos = executing_user.find('@')
        executing_user = executing_user[:at_pos]
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        executing_user = msg = msg.replace("'",'"')
    return executing_user


# In[3]:


def get_modifiedtimestamp():
    try:
        pst_timezone = pytz.timezone('US/Pacific')
        current_time_utc = datetime.now(pytz.utc)
        current_time_pst = current_time_utc.astimezone(pst_timezone)
    except Exception as e: 
        current_time_pst = datetime(1900, 1, 1, 0, 0, 0)
    return current_time_pst


# In[4]:


def get_workspace_name(WorkspaceID):
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        response = client.get(f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/')
        metadata = response.json()
        WorkspaceName = metadata.get('displayName','')
        msg = "{} workspace name is retrieved".format(WorkspaceName)
    except Exception as e:
        WorkspaceName = "Unknown"
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return (WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime)


# In[5]:


def get_dataset_name(WorkspaceID,DatasetID):
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        response = client.get(f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{DatasetID}')
        metadata = response.json()
        DatasetName = metadata.get('displayName','')
        msg = "{} dataset name is retrieved".format(DatasetName)
    except Exception as e:
        DatasetName = "Unknown"
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return (WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)


# In[6]:


def get_lakehouse_name(WorkspaceID,LakehouseID):
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        response = client.get(f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{LakehouseID}')
        metadata = response.json()
        LakehouseName = metadata.get('displayName','')
        msg = "{} dataset name is retrieved".format(LakehouseName)
    except Exception as e:
        LakehouseName = "Unknown"
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return (WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime)


# In[7]:


def get_tmsl(workspace,dataset):
    tmsl_script = fabric.get_tmsl(dataset,workspace)
    tmsl_dict = json.loads(tmsl_script)
    return tmsl_dict


# In[8]:


def get_default_lakehouse():
    defaultLakehouseWorkspaceId = mssparkutils.notebook.notebook.nb.context.get('defaultLakehouseWorkspaceId')
    defaultLakehouseWorkspaceName = mssparkutils.notebook.notebook.nb.context.get('defaultLakehouseWorkspaceName')
    defaultLakehouseId = mssparkutils.notebook.notebook.nb.context.get('defaultLakehouseId')
    defaultLakehouseName = mssparkutils.notebook.notebook.nb.context.get('defaultLakehouseName')  
    return (defaultLakehouseWorkspaceId,defaultLakehouseWorkspaceName,defaultLakehouseId,defaultLakehouseName)


# In[9]:


def create_tables():
    try:
        spark.sql("""CREATE TABLE WorkspaceList (ID STRING, Name STRING, Info String, Alias STRING, ModifiedTime timestamp) USING DELTA""")
        spark.sql("""CREATE TABLE DatasetList (WorkspaceID String, ID STRING, Name STRING, Alias STRING, Info String, ModifiedTime timestamp) USING DELTA""")
        spark.sql("""CREATE TABLE LakehouseList (WorkspaceID String,ID STRING, Name STRING, Alias STRING,Info String, ModifiedTime timestamp) USING DELTA""")
        msg = "Required Tables are successfully created"
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return msg


# In[10]:


def truncate_table():
    try:
        spark.sql("""DELETE FROM WorkspaceList""")
        spark.sql("""DELETE FROM DatasetList""")
        spark.sql("""DELETE FROM LakehouseList""")
        msg = "data deleted from all required tables"
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return msg


# In[11]:


def insert_update_workspace_detail(WorkspaceID):
    try:
        defaultLakehouseWorkspaceId,defaultLakehouseWorkspaceName,defaultLakehouseId,defaultLakehouseName = get_default_lakehouse()
        if defaultLakehouseId is not None:
            WorkspaceID = WorkspaceID.lower()
            query = "SELECT count(1) as output FROM delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/workspacelist` WHERE lcase(trim(ID)) = '{2}'".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID)
            df = spark.sql(query)
            flag = df.select("output").first()[0]
            if flag == 0:
                WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime = get_workspace_name(WorkspaceID)
                insertquery = "INSERT INTO delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/workspacelist` VALUES ('{2}', '{3}', '{4}' , '{5}', '{6}');".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime)
                spark.sql(insertquery)
                msg = "{0} Workspace Metadata is Inserted".format(WorkspaceName)
            else:
                WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime = get_workspace_name(WorkspaceID)
                if WorkspaceName != "Unknown":
                    updatequery = "UPDATE delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/workspacelist` SET Name = '{3}',Info = '{4}',Alias = '{5}' , ModifiedTime = '{6}' WHERE lcase(ID) = '{2}'".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime)
                    spark.sql(updatequery)
                    msg = "{0} Workspace Metadata is Updated".format(WorkspaceName)
                else: 
                    msg = "You don't have access {0} workspaceid but we already workspace details".format(WorkspaceID)
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return msg


# In[12]:


def insert_update_dataset_detail(WorkspaceID,DatasetID):
    try:
        defaultLakehouseWorkspaceId,defaultLakehouseWorkspaceName,defaultLakehouseId,defaultLakehouseName = get_default_lakehouse()
        if defaultLakehouseId is not None:
            WorkspaceID = WorkspaceID.lower()
            query = "SELECT count(1) as output FROM delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/datasetlist` WHERE lcase(trim(ID)) = '{2}'".format(defaultLakehouseWorkspaceId,defaultLakehouseId,DatasetID)
            df = spark.sql(query)
            flag = df.select("output").first()[0]
            if flag == 0:
                WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime = get_dataset_name(WorkspaceID,DatasetID)
                insertquery = "INSERT INTO delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/datasetlist` VALUES ('{2}', '{3}', '{4}' , '{5}', '{6}','{7}');".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)
                spark.sql(insertquery)
                msg = "{0} Dataset Metadata is Inserted".format(DatasetName)
            else:
                WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime = get_dataset_name(WorkspaceID,DatasetID)
                if DatasetName != "Unknown":
                    updatequery = "UPDATE delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/datasetlist` SET WorkspaceID = '{2}',Name = '{4}',Info = '{5}',Alias = '{6}' , ModifiedTime = '{7}' WHERE lcase(ID) = '{3}'".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)
                    spark.sql(updatequery)
                    msg = "{0} Workspace Metadata is Updated".format(DatasetName)
                else: 
                    msg = "You don't have access {0} dataset but we already dataset details".format(DatasetID)
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return msg


# In[13]:


def insert_update_lakehouse_detail(WorkspaceID,LakehouseID):
    try:
        defaultLakehouseWorkspaceId,defaultLakehouseWorkspaceName,defaultLakehouseId,defaultLakehouseName = get_default_lakehouse()
        if defaultLakehouseId is not None:
            WorkspaceID = WorkspaceID.lower()
            query = "SELECT count(1) as output FROM delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/lakehouselist` WHERE lcase(trim(ID)) = '{2}'".format(defaultLakehouseWorkspaceId,defaultLakehouseId,LakehouseID)
            df = spark.sql(query)
            flag = df.select("output").first()[0]
            if flag == 0:
                WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime = get_lakehouse_name(WorkspaceID,LakehouseID)
                insertquery = "INSERT INTO delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/lakehouselist` VALUES ('{2}', '{3}', '{4}' , '{5}', '{6}','{7}');".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime)
                spark.sql(insertquery)
                msg = "{0} Dataset Metadata is Inserted".format(LakehouseName)
            else:
                WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime = get_lakehouse_name(WorkspaceID,LakehouseID)
                if LakehouseName != "Unknown":
                    updatequery = "UPDATE delta.`abfss://{0}@msit-onelake.dfs.fabric.microsoft.com/{1}/Tables/lakehouselist` SET WorkspaceID = '{2}',Name = '{4}',Info = '{5}',Alias = '{6}' , ModifiedTime = '{7}' WHERE lcase(ID) = '{3}'".format(defaultLakehouseWorkspaceId,defaultLakehouseId,WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime)
                    spark.sql(updatequery)
                    msg = "{0} Workspace Metadata is Updated".format(LakehouseName)
                else: 
                    msg = "You don't have access {0} lakehouse but we already lakehouse details".format(LakehouseID)
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    return msg


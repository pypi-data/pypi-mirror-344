#!/usr/bin/env python
# coding: utf-8

# ## Functions
# 
# New notebook

# In[1]:


import sempy.fabric as fabric 
from datetime import datetime
from notebookutils import mssparkutils
import pytz


# In[2]:


def get_executer_alias():
    try:
        executing_user = mssparkutils.env.getUserName()
        at_pos = executing_user.find('@')
        executing_user = executing_user[:at_pos]
    except Exception as e:
        executing_user = e
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
        msg = e
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
        msg = e
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
        DatasetName = "Unknown"
        msg = e
    return (WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime)


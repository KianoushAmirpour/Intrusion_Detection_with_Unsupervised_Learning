import os
import re
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs

def read_data(filename):
    """
    This function reads the log file and then parse them into a pre-defined columns
    """
    pattern = r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])'
    
    df = pd.read_csv(os.path.join("../input", filename),
                     sep= pattern,
                     engine="python",
                     header=None,
                     na_values="-",
                     names = ['ip', 'time', 'request', 'status_code', 'response_length', 'user_agent', 'response_time'],
                     error_bad_lines=False)
    
    return df

def session_indentifier(df):
    """
    This function finds sessions for each unique pair of ip and user agent with a 30 min interval between two 
        consecutive sessions. so each pair might have several sessions.   
    Args:
        df : the base dataframe which must includes ip, time, user agent
    Returns:
        df['session']: this new column identifies sessions (int)
    """
    
    if df.time.dtype ==  "O":
        df.time = pd.to_datetime(df.time)
    
    df = df.sort_values('time')
    grp_ip_agent = df.groupby(['ip',"user_agent"])
    
    
    df['session'] = grp_ip_agent['time'].apply(
                    lambda s: (s - s.shift(1) > pd.to_timedelta(1800, unit='s')).fillna(0).cumsum(skipna=False))
    
    return df['session']


    
    



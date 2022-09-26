import os
import re
import sys
sys.path.append('../')
import numpy as np
import pandas as pd
from datetime import datetime
from user_agents import parse


def build_features(df):
    
    """ This function builds features for each user session. 
        A user session is a sequence of requests a Web client makes during the single visit to the Website.

    Args:
        df : the base dataframe which includes ip, time, user agent, session, methods, path, status_code, 
            response_length, response_time as its columns
        

    Returns:
        user_session: a dataframe with (ip, user agent and session) as its indices and created features
    """

    # num_requests: (the number of HTTP requests sent by a user in a single session) 
    # higher num_requests can only be achieved by an automated script and is usually very low for a human visitor of the web site.
    
    df["path"] = df["path"].fillna("-")
    user_session = pd.DataFrame(df.groupby(["ip", "user_agent", "session"]).size(), columns=["num_requests"])
    
    # Image_to_request ratio:  
    # the number of image file (JPEG and PNG) requests over the number of requests sent in a single session.
    # this ratio would be lower for web crawlers than for human users. 
    # usual formats for images: ".tif", ".tiff", ".bmp", ".jpg", ".gif", ".png", ".jpeg", ".eps", ".ico"
    
    condition_1 = df["path"].str.contains("images")
    condition_2 = df["path"].str.endswith(".png") 
    condition_3 = df["path"].str.endswith(".jpg") 
    condition_4 = df["path"].str.endswith(".gif") 
    condition_5 = df["path"].str.endswith(".ico")
    request_imgs = df[condition_1 | condition_2 | condition_3 | condition_4 | condition_5]
    user_session["req_imgs"] = request_imgs.groupby(["ip", "user_agent", "session"])["path"].agg("size")
    user_session["req_imgs"] = user_session["req_imgs"].fillna(0) 
    user_session["img_to_req(%)"] = (user_session["req_imgs"] / user_session["num_requests"]) * 100
    
    # Percentage of 4xx error responses:
    # the percentage of erroneous HTTP requests sent in a single session.
    # usually higher rate of erroneous requests for crawlers since they have higher chance of requesting outdated or deleted pages. 
    
    status_4xx = df[(df["status_code"] >= 400)]
    user_session["4xx_status_codes"] = status_4xx.groupby(["ip", "user_agent","session"])["status_code"].agg("size")
    user_session["4xx_status_codes"] = user_session["4xx_status_codes"].fillna(0)
    user_session["4xx(%)"] = (user_session["4xx_status_codes"] / user_session["num_requests"]) * 100
    
    # Percentage of HTTP requests of type HEAD:
    # percentage of requests of HTTP type HEAD sent in a single session.
    # Most web crawlers, in order to reduce the amount of data requested from a site, employ the 
    # HEAD method when requesting a web page. A human user browsing web site would exclusively request web pages using a GET method
    
    head_requested = df[df["method"] == "Head"]
    user_session["requested_head"] = head_requested.groupby(["ip", "user_agent","session"])["method"].agg("size")
    user_session["requested_head"] = user_session["requested_head"].fillna(0)
    user_session["Head(%)"] = (user_session["requested_head"] / user_session["num_requests"]) * 100
     
    # Standard deviation of requested page’s depth: 
    # the standard deviation of page depth across all requests sent in a single session. Deeper requests usually indicates a human user.
    
    df["path_length"] = df["path"].apply(lambda x : len(x.split("/")))
    user_session["std_path_length"] = df.groupby(["ip", "user_agent","session"])["path_length"].agg("std")
    user_session["std_path_length"] = user_session["std_path_length"].fillna(0)
    
    # Percentage of consecutive repeated HTTP requests:
    # the number of repeated requests sent in sequence belonging to the same web directory sent by a user during a session.
    
    user_session['merged_paths']= df.groupby(['ip', 'user_agent', "session"])['path'].apply(' '.join)
    
    def consq_rep_reqs(merged_path):
        splited_paths = merged_path.split(" ")
        for idx in range(len(splited_paths)):
            splited_parts = splited_paths[idx].split("/")
            if len(splited_parts) > 1:
                splited_paths[idx] = "/".join(splited_parts[:-1])
        return len(np.unique(np.array(splited_paths)))
    
    user_session['consq_rep_path_count'] = user_session['merged_paths'].apply(consq_rep_reqs)
    user_session['consq_rep_path_count'] = user_session['num_requests'] - user_session['consq_rep_path_count']
    user_session['consq_rep_path(%)'] = (user_session['consq_rep_path_count'] / user_session['num_requests'])*100
    
    # average and sum of response length and response time for each session
    # how to interpret this ??????????????????????????
    user_session["ave_response_len"] = df.groupby(['ip', 'user_agent', "session"])['response_length'].agg("mean")
    user_session["sum_response_len"] = df.groupby(['ip', 'user_agent', "session"])['response_length'].agg("sum")
    user_session["ave_response_time"] = df.groupby(['ip', 'user_agent', "session"])['response_time'].agg("mean")
    user_session["sum_response_time"] = df.groupby(['ip', 'user_agent', "session"])['response_time'].agg("sum")
    
    # Also, since we are investigating the behaviour as evident from the click-stream of a user-agent,
    # it is fair to assume that any session with less than 5 requests in total, is too short to enable labelling. 
    # Even by manual inspection, a session with such a few numbers of requests is almost impossible to classify. We are therefore 
    # ignoring sessions that are too small (i.e. with less than 5 requests). 
    requests_thre = 5
    user_session = user_session[user_session["num_requests"] > 5]
    
    # session duration :
    # time interval (in seconds) between the times of the last and the first requests in session
    
    temp = df.sort_values(by="time")
    user_session['session_duration']= ((temp.groupby(['ip', 'user_agent', "session"])['time'].nth(-1) - 
                                 temp.groupby(['ip', 'user_agent', "session"])['time'].nth(0)).dt.total_seconds()) /60
    
    
    # average time per page: the average time (in seconds) the user browsed a single page in session
    
    user_session["ave_time_per_page"] = user_session['session_duration'] / (user_session["num_requests"] - 1)
    
    # Robot.txt file request:
    # nominal attribute with values of either 1 or 0, indicating whether ‘robot.txt’ file was requested or not.
    
    requested_robots_txt = df[df["path"].str.contains("robots.txt")]
    user_session["robot.txt_count"] = requested_robots_txt.groupby(["ip", "user_agent","session"])["path"].agg("size")
    user_session["robot.txt_count"] = user_session["robot.txt_count"].fillna(0)
    user_session["robot_txt"] = user_session["robot.txt_count"].apply(lambda x : 1 if x > 0 else 0)
    
    # using the scraped data from udger resourcees in order to find crawlers and bots in user agent
    
    known_bots = []
    with open("../input/known_crawlers_2022-08-02.txt", "r") as bots:
        for bot in bots:
            known_bots.append(bot.lower().replace(" ", "").replace("-", "").strip())
    
    if "browser" not in df.columns:
        df["browser"] = df['user_agent'].apply(lambda x: parse(x).browser.family)
        
    df["suspected_bot_1"] = df["browser"].apply(lambda x: 1 if x.lower().strip().replace("-", "").replace(" ", "") in known_bots else 0)
            
    user_session["is_bot_1"] = df.groupby(['ip', 'user_agent', "session"])['suspected_bot_1'].apply(
                lambda grp: 1 if grp.sum() > 1 else 0)
    
    # looking for these words in user agents
    # ["bot", "spider", "crawler", "worm", "search", "track", "harvest", "dig", "hack", "trap", "archive", "scrap"]
    
    def decting_bot(x):
        patterns = ["bot", "spider", "crawler", "worm", "search", "track", "harvest", "dig", "hack", "trap", "archive", "scrap"]
        for pattern in patterns:
            if pattern in x.lower().strip():
                return 1
            return 0

            
    df["suspected_bot_2"] = df["user_agent"].apply(decting_bot)
    
    user_session["is_bot_2"] = df.groupby(['ip', 'user_agent', "session"])['suspected_bot_2'].apply(
                lambda grp: 1 if grp.sum() > 1 else 0)  
    
    user_session['is_bot'] = user_session.apply(lambda row : 1 if row["is_bot_1"] == 1 or row["is_bot_2"] == 1 else 0, axis = 1)
    
    user_session.drop(columns=["req_imgs", "4xx_status_codes", "requested_head", "robot.txt_count", "merged_paths",
                               "consq_rep_path_count","is_bot_1","is_bot_2" ], inplace=True)
    
    return user_session

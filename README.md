# Intrusion detection with unsupervised learning

This is the final project for advanced machine learning course represented by [Rahnema College](https://rahnemacollege.com/). In this project, we were tasked with identifying intrusions in a system, relying on the analysis of logs. Since the ground truth labels for anomalous behaviors weren't provided, we had to employ unsupervised anomaly detection methods.

## Dataset.
Because the dataset cannot be shared publicly, we've included a few samples below to give you an idea of its content.

* 207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get /cdn/profiles/1026106239] 304 0 [[Googlebot-Image/1.0]] 32
* 207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get images/badge.png] 304 0 [[Googlebot-Image/1.0]] 4

## Project structure
- EDA
  - Data_Cleaning_and_Basic_EDA.ipynb
  - Distributions.ipynb
  - Feature_Generation_and_EDA_based_on_them.ipynb

- modes
  - AutoEncoder.ipynb
  - Gaussian_Mixture_Models.ipynb
  - IsolationForest.ipynb

- utils
  - Gaussian_mixture_from_scratch.py
  - build_features.py
  - scraping_crawlers.py
  - utils.py

## Workflow
- Data Cleaning and EDA:
    - We performed data cleaning by removing unnecessary characters, modifying data types, and identifying missing values. We handled these issues using suitable approaches, along with visualizations.
- Finding Sessions:
  - We identified sessions for each unique pair of IP addresses and user agents, incorporating a 30-minute interval between two consecutive sessions.
- Feature Engineering:
  - num_requests
  - Image_to_request ratio
  - Percentage of `4xx` error responses
  - Percentage of `HTTP` requests of type `HEAD`
  - Standard deviation of the requested page’s depth
  - Percentage of consecutively repeated `HTTP` requests
  - Average and sum of response length and response time for each session
  - Session duration
  - Average time per page
  - Robot.txt file request
- Scraped Well-Known Crawlers.
- Data Transformation Experimentation:
  - We experimented with various data transformation techniques, including Power, Quantile, Logarithmic, Reciprocal, Square Root, Exponential, and Box-Cox transformations.
- Anomaly Detection:
  - Isolation Forest
  - Gaussian mixture models
  - Autoencoders




   



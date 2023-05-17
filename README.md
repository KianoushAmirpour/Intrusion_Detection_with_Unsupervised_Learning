## Intrusion_Detection_with_unsupervised_Learning

This is the final project for advanced machine learning course represented by [Rahnema College](https://rahnemacollege.com/). In this project, we were asked to identify intrusion in a system, which relies on the analysis of logs. Since the ground truth labels of anomalous behaviors were not given to us, we had to use unsupervised anomaly detection methods.

## Dataset
Since the dataset cannot be publicly published, in order to get the sense of it, a few samples are shown below.

* 207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get /cdn/profiles/1026106239] 304 0 [[Googlebot-Image/1.0]] 32
* 207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get images/badge.png] 304 0 [[Googlebot-Image/1.0]] 4

## Project Structure
In the [Data cleaning and basic EDA](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/EDA/Data_Cleaning%20_and_Basic_EDA.ipynb), the focus was mostly on reading the data using regex and storing them in a pandas data frame, cleaning the texts by removing unnecessary characters, modifying data types and finding missing values and handling them with suitable approaches. This notebook also contains some basic visualization.

For next step, sessions for each unique pair of Ip and user agent with a 30 min interval between two consecutive sessions were found. The code can be find [here](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/utils/utils.py)

Some useful features which could be useful for this project were extracted from literature. These features are num_requests, Image_to_request ratio, Percentage of 4xx error responses, Percentage of HTTP requests of type HEAD, Standard deviation of requested page’s depth, Percentage of consecutive repeated HTTP requests, average and sum of response length and response time for each session, session duration, average time per page, Robot.txt file request. [build_features.py](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/utils/build_features.py) builds the required features.

I also scraped some useful resources to get the most up to date list of known crawlers which have been used in building the features. for more information about the websites that I used and how I extracted their data you can look at [scraping_crawlers.py](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/utils/scraping_crawlers.py)

In [Feature_Generation_and_EDA_based_on_them](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/EDA/Feature_Generation_and_EDA_based_on_them.ipynb) notebook, at first Features were built and then Exploratory Data Analysis were done based on them, which you can find it [here](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/EDA/Feature_Generation_and_EDA_based_on_them.ipynb).

I also tried some data transformation techniques including Power, Quantile, Logarithmic, Reciprocal, Square Root, Exponential and coxbox Transformations to see which one works better for this project. The effects on the distribution of features under each of mentioned transformations can be seen [here](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/blob/main/EDA/Distributions.ipynb).

For finding the anomalous behaviors, Isolation Forest and Gaussian mixture models were used. you can find more details [here](https://github.com/KianoushAmirpour/Intrusion_Detection_with_Unsupervised_Learning/tree/main/models)















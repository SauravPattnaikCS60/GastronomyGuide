import pandas as pd
import numpy as np
import ast
from math import radians, cos, sin, asin, sqrt, isnan
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
from functools import lru_cache

tfidf_df = None

@lru_cache(maxsize=None)
def get_latitude_longitude(positioning_data):
    positioning_data = ast.literal_eval(positioning_data)
    latitude = positioning_data['data'][0]['latitude']
    longitude = positioning_data['data'][0]['longitude']
    return longitude, latitude


def compute_score_bracket(distance):
    if distance < 5:
        return 100
    elif distance < 10:
        return 90
    elif distance < 15:
        return 70
    elif distance < 25:
        return 50
    else:
        return 25


def haversine(res1_positioning_info, res2_positioning_info):
    if res1_positioning_info is np.nan or res2_positioning_info is np.nan:
        return 0

    lon1, lat1 = get_latitude_longitude(res1_positioning_info)
    lon2, lat2 = get_latitude_longitude(res2_positioning_info)

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return compute_score_bracket(c * r)

# Function 2
# Used to check boolean indicators for restaurants(like booking table is available or not, online order is available or not)

def same_feature_check(res1_value, res2_value):
    if res1_value == res2_value:
        return 100
    else:
        return 0


# Function 3
# Used to give higher weightage to similar value ranges(like for votes and approx cost for two, ratings)

def compute_closeness_score(value1, value2):
    if value1 == -1 or value2 == -1:
        return 0

    try:
        ratio = value1 / value2 if value1 < value2 else value2 / value1
        return ratio * 100

    except:
        return 0


# Function 4
# Computes Jaccquard Similarity between list of items like cuisines, food items, restaurant types

def compute_jaccard_similarity(list1, list2):
    if isinstance(list1, str):
        list1 = list1.split(' ')
    if isinstance(list2, str):
        list2 = list2.split(' ')

    intersection = np.intersect1d(list1, list2)
    union = np.union1d(list1, list2)
    try:
        score = len(intersection) / len(union)
        return score * 100
    except:
        return 0


# Function 5
# Aggregate all the text of each restaurants and find the most common words found.
# Then use cosine similarty/jaccquard similarity to assign a score

def return_preprocessed_text(text):
    text = text.lower()
    text = re.sub("[^a-z0-9]", " ", text)
    text = re.sub("(\s)+", " ", text)
    text = text.strip()

    return text


def agg_user_reviews(review_list):
    try:
        review_list = ast.literal_eval(review_list)
        agg_reviews = ''
        for tup in review_list:
            _, review = tup
            review = review.split('\n')[1]
            clean_review = return_preprocessed_text(review)
            agg_reviews = agg_reviews + clean_review + ' '
            return agg_reviews
    except:
        return ''

def create_feature_vector_tfidf(df, agg_text_col):
    tfidf = TfidfVectorizer(max_features=150, stop_words='english',max_df=0.95)
    tfidf_df = pd.DataFrame(tfidf.fit_transform(df[agg_text_col]).toarray(),columns=tfidf.get_feature_names_out())
    tfidf_df['url'] = df['url']
    return tfidf_df


# Function 6
# This fuction takes the tfidf weights of two restaurants and computes cosine similarity


@lru_cache(maxsize=None)
def get_tfidf_values(url1, url2):
    tfidf_values_1 = np.array(tfidf_df[tfidf_df['url'] == url1].drop('url',axis=1))[0]
    tfidf_values_2 = np.array(tfidf_df[tfidf_df['url'] == url2].drop('url',axis=1))[0]
    return tfidf_values_1, tfidf_values_2

def get_reviews_score(url1, url2, tfidf):
    global tfidf_df
    if tfidf_df is None:
        tfidf_df = tfidf

    tfidf_values_1, tfidf_values_2 = get_tfidf_values(url1,url2)
    cosine_score = (1-cosine(tfidf_values_1,tfidf_values_2))*100
    if isnan(cosine_score):
        return 0
    return cosine_score


def get_rating(rating):
    try:
        return float(rating.split('/')[0])
    except:
        return -1


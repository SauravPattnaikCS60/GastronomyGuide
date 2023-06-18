from feature_engineering import *
from tqdm import tqdm

restaurants_to_restaurants_score_mapper = {}
recommendatation_model = {}

def initialize_dictionary(restaurant1, restaurant2, distance_score, online_order_score, booking_table_score,
                          rating_score,
                          votes_score, type_of_restaurant_score, dishes_score, cuisines_score, approx_cost_score,
                          reviews_score,
                          final_score):
    if restaurant1 not in restaurants_to_restaurants_score_mapper.keys():
        restaurants_to_restaurants_score_mapper[restaurant1] = {}

    if restaurant2 not in restaurants_to_restaurants_score_mapper[restaurant1].keys():
        restaurants_to_restaurants_score_mapper[restaurant1][restaurant2] = {}

    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['distance_score'] = distance_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['online_order_score'] = online_order_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['booking_table_score'] = booking_table_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['rating_score'] = rating_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['votes_score'] = votes_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2][
        'type_of_restaurant_score'] = type_of_restaurant_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['dishes_score'] = dishes_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['cuisines_score'] = cuisines_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['approx_cost_score'] = approx_cost_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['reviews_score'] = reviews_score
    restaurants_to_restaurants_score_mapper[restaurant1][restaurant2]['final_score'] = final_score


def train_recommendation_model(df):
    df['agg_user_reviews'] = df['reviews_list'].apply(agg_user_reviews)
    df['agg_user_reviews'].fillna('', inplace=True)

    tfidf = create_feature_vector_tfidf(df, 'agg_user_reviews')
    df['rate'] = df['rate'].apply(get_rating)

    for index1, row1 in tqdm(df.iterrows()):
        temporary_dictionary = {}
        restaurant1 = row1['name'] + ',' + row1['location']
        for index2, row2 in df.iloc[index1 + 1:].iterrows():
            if row1['name'] == row2['name']:
                continue  # passing same restaurants in different locations

            distance_score = haversine(row1['positioning_data'], row2['positioning_data'])
            online_order_score = same_feature_check(row1['online_order'], row2['online_order'])
            booking_table_score = same_feature_check(row1['book_table'], row2['book_table'])
            rating_score = compute_closeness_score(row1['rate'], row2['rate'])
            votes_score = compute_closeness_score(row1['votes'], row2['votes'])
            type_of_restaurant_score = compute_jaccard_similarity(row1['rest_type'], row2['rest_type'])

            dishes_score = compute_jaccard_similarity(row1['dishes'], row2['dishes'])
            cuisines_score = compute_jaccard_similarity(row1['cuisines'], row2['cuisines'])
            approx_cost_score = compute_closeness_score(row1['approx_cost(for two people)'],
                                                        row2['approx_cost(for two people)'])

            reviews_score = get_reviews_score(row1['url'], row2['url'], tfidf)

            restaurant2 = row2['name'] + ',' + row2['location']

            final_score = distance_score*0.05 + 0.05*online_order_score + 0.05*booking_table_score + 0.05*rating_score +\
                          0.05*votes_score + 0.2*type_of_restaurant_score + 0.15*dishes_score + 0.2*cuisines_score +\
                          0.15*approx_cost_score + 0.05*reviews_score

            temporary_dictionary[restaurant2] = final_score

            initialize_dictionary(restaurant1, restaurant2, distance_score, online_order_score, booking_table_score,
                                  rating_score,
                                  votes_score, type_of_restaurant_score, dishes_score, cuisines_score,
                                  approx_cost_score, reviews_score,
                                  final_score)

            initialize_dictionary(restaurant2, restaurant1, distance_score, online_order_score, booking_table_score,
                                  rating_score,
                                  votes_score, type_of_restaurant_score, dishes_score, cuisines_score,
                                  approx_cost_score, reviews_score,
                                  final_score)

        temporary_dictionary = sorted(temporary_dictionary.items(), key=lambda x: x[1], reverse=True)[:3]
        recommendatation_model[restaurant1] = temporary_dictionary

    return recommendatation_model, restaurants_to_restaurants_score_mapper

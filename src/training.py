import pandas as pd
import joblib
from data_cleaning import clean_data
from build_recommendation_model import *

def perform_training():
    # reading of data
    df = pd.read_excel('../data/zomato_data_final_with_positioning_data.xlsx')

    # basic cleaning of data
    df_clean = clean_data(df)

    # build recommendation model
    recommendation_model, feature_matrix = train_recommendation_model(df_clean)
    joblib.dump(recommendation_model, open("../model/BLR_restaurant_model.pkl","wb"))
    joblib.dump(feature_matrix,open("../model/feature_matrix.pkl","wb"))
    print('Training Pipeline Done')

perform_training()

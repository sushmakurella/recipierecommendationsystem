import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
# import config
# load in parsed recipe dataset
df_recipes = pd.read_csv('Cleaned_Indian_Food_Dataset.csv')
df_recipes=df_recipes.iloc[0:3500]
# Tfidf needs unicode or string types
df_recipes['Cleaned_Ingredients'] =df_recipes.Cleaned_Ingredients.values.astype('U')
# TF-IDF feature extractor
tfidf = TfidfVectorizer()
tfidf.fit(df_recipes['Cleaned_Ingredients'])
tfidf_recipe = tfidf.transform(df_recipes['Cleaned_Ingredients'])
#save the tfidf model and encodings
with open("tfidf.pkl", "wb") as f:
     pickle.dump(tfidf, f)
with open("tfidf_encodings.pkl", "wb") as f:
     pickle.dump(tfidf_recipe, f)
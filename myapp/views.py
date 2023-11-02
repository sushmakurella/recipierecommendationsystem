from django.shortcuts import render
#*****************************
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
#from ingredient_parser import ingredient_parser
import pickle
#import config 
import unidecode, ast


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
#******************************
# Create your views here.

# /Users/Jack/Documents/Projects/Whatscooking-/src

# Top-N recomendations order by score
def get_recommendations(N, scores):
    # load in recipe dataset 
    df_recipes = pd.read_csv('Cleaned_Indian_Food_Dataset.csv')
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # create dataframe to load in recommendations 
    recommendation = pd.DataFrame(columns = ['recipe', 'ingredients', 'score', 'url'])
    # recommendation = pd.DataFrame(columns = ['recipe', 'score', 'url'])
    count = 0
    for i in top:
        recommendation.at[count, 'recipe'] = title_parser(df_recipes['TranslatedRecipeName'][i])
        recommendation.at[count, 'ingredients'] = df_recipes['TranslatedIngredients'][i]
        recommendation.at[count, 'url'] = df_recipes['URL'][i]
        recommendation.at[count, 'image_url'] = df_recipes['image_url'][i]
        recommendation.at[count, 'TranslatedInstructions'] = df_recipes['TranslatedInstructions'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        #image_url
        #TranslatedInstructions


        count += 1
    return recommendation

# neaten the ingredients being outputted 
def ingredient_parser_final(ingredient):
    if isinstance(ingredient, list):
        ingredients = ingredient
    else:
        ingredients = ast.literal_eval(ingredient)
    
    ingredients = ','.join(ingredients)
    ingredients = unidecode.unidecode(ingredients)
    return ingredients

def title_parser(title):
    title = unidecode.unidecode(title)
    return title 

def RecSys(ingredients, N=10):
    """
    The reccomendation system takes in a list of ingredients and returns a list of top 5 
    recipes based of of cosine similarity. 
    :param ingredients: a list of ingredients
    :param N: the number of reccomendations returned 
    :return: top 5 reccomendations for cooking recipes
    """

    # load in tdidf model and encodings 
    with open("tfidf_encodings.pkl", 'rb') as f:
        tfidf_encodings = pickle.load(f)

    with open("tfidf.pkl", "rb") as f:
        tfidf = pickle.load(f)
    #*******************************************
    # df_recipes = pd.read_csv('Cleaned_Indian_Food_Dataset.csv')
    # # Tfidf needs unicode or string types
    # df_recipes['Cleaned_Ingredients'] =df_recipes.Cleaned_Ingredients.values.astype('U')
    # # TF-IDF feature extractor
    # tfidf = TfidfVectorizer()
    # tfidf.fit(df_recipes['Cleaned_Ingredients'])
    # tfidf_encodings = tfidf.transform(df_recipes['Cleaned_Ingredients'])
    #**********************************************************
    ingredients_parsed=ingredients
    # use our pretrained tfidf model to encode our input ingredients
    ingredients_tfidf = tfidf.transform([ingredients_parsed])

    # calculate cosine similarity between actual recipe ingreds and test ingreds
    cos_sim = map(lambda x: cosine_similarity(ingredients_tfidf, x), tfidf_encodings)
    scores = list(cos_sim)

    # Filter top N recommendations 
    recommendations = get_recommendations(N, scores)
    return recommendations

# if __name__ == "__main__":
#     # test ingredients
#     test_ingredients = "pasta tomato onion"
#     recs = RecSys(test_ingredients)
#     # print(recs.score)
#     # print(recs)
#     print(recs.ingredients)



def index(request):
    return render(request,'index.html')
def collect(request):
    if request.method=='POST':
        '''n=int(request.POST['dummy'])
        print(n)
        lst=[]
        l=['i'+str(i) for i in range(n+1)]
        s=''
        print('*******************',l)
        for i in range(n+1):
            ele=request.POST[l[i]]
            lst.append(ele)
            s=s+ele+' '
        print(lst)'''
        s=request.POST['inp']
        s.replace(',',' ')
        recs = RecSys(s)
        res=[]
        for index, row in recs.iterrows():
            temp=[]
            temp.append(row['recipe'])
            t=row['ingredients'].split(',')
            temp.append(t)
            temp.append(row['url'])
            temp.append(row['image_url'])
            temp.append(row['TranslatedInstructions'])
            res.append(temp)
            

    return render(request,'show.html',{'res':res})
# def test(request):
#     j=0
#     for i in range(10000000000000000000000000000000):
#         j+=1
#     return render(request,'test.html')

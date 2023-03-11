import pandas as pd
import numpy as np

from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity

from django.contrib.auth.models import User
from main.models import Story, UserProfile, LikedStory


class UserBasedRecommender:
    def __init__(self) -> None:
        self.cache_key = 'ub_recommender_similarities'
    
    
    def train(self):
        # Get stories
        stories = Story.objects.all().values('id', 'title1')
        stories = pd.DataFrame(list(stories))

        stories.rename(columns={'id': 'story_id'}, inplace=True)
        #print(f'Head stories:\n{stories.head()}')


        # Get ratings
        ratings = LikedStory.objects.all().values('user_profile', 'story')
        ratings = pd.DataFrame(list(ratings))
        ratings.rename(columns={'user_profile': 'user_profile_id','story': 'story_id'}, inplace=True)
        ratings['rating'] = 1
        #print(f'Head ratings:\n{ratings.head()}')


        # Merge tables
        df = pd.merge(ratings, stories, on='story_id', how='inner')
        #print(f'Head table:\n{df.head()}')


        # Count ratings
        #agg_ratings = df.groupby('title1').agg(number_of_ratings = ('rating', 'count')).reset_index()
        #x = agg_ratings.sort_values(by='number_of_ratings', ascending=False).head()
        #print(f'agg ratings\n{x}')


        # Create matrix
        matrix = df.pivot_table(index='user_profile_id', columns='title1', values='rating').fillna(0)
        #print(f'Matrix\n{matrix.head()}')


        # Get cosine similarities
        cosine_similarities = cosine_similarity(matrix)
        #print(f'Cosine similarities\n{cosine_similarities}')


        # Map cosine similatiries
        similarities = {}
        for i, cs in enumerate(cosine_similarities):
            similar_indices = cs.argsort()[:-50:-1]
            similarities[matrix.index[i]] = [(matrix.index[x], cs[x]) for x in similar_indices][1:]
        #print(f'Similarities\n{similarities}')


        # Save recommendations in cache
        cache.set(self.cache_key, similarities, timeout=None)
        return True


    def recommend(self, user_id, max_recommendations=10):
        # Get the similarities from cache
        matrix_similarities = cache.get(self.cache_key)
        if not matrix_similarities:
            print(f'\n\nThe recommender is not trained yet, training...\n\n')
            trainning = self.train()
            if trainning:
                return self.recommend(user_id=user_id, max_recommendations=max_recommendations)
            return []
        #print(f'\nMatrix similarities\n{matrix_similarities}')

        # Similar users is an array with the users id and similarity predicted
        similar_users = matrix_similarities.get(user_id)
        if similar_users:
            similar_users = similar_users[:max_recommendations]

        print(f'{similar_users}')

import pandas as pd
import numpy as np

from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity

from django.contrib.auth.models import User
from main.models import Story, UserProfile, LikedStory


class UserBasedRecommender:
    def __init__(self) -> None:
        self.cache_users_key = 'ubr_users'
        self.cache_stories_key = 'ubr_stories'
        self.cache_cosines_key = 'ubr_cosines'
        self.timeout = None
    
    
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
        matrix = df.pivot_table(index='user_profile_id', columns='story_id', values='rating').fillna(0)
        cache.set(self.cache_stories_key, matrix, timeout=self.timeout)
        #print(f'Matrix\n{matrix.head()}')


        # Get cosine similarities
        cosine_similarities = cosine_similarity(matrix)
        #print(f'Cosine similarities\n{cosine_similarities}')

        # Cosine similarities as dataframe
        cosine_similarities_df = pd.DataFrame(cosine_similarities, index=matrix.index, columns=matrix.index)
        cache.set(self.cache_cosines_key, cosine_similarities_df, timeout=self.timeout)

        # Cosine similatiries as dict
        similarities = {}
        for i, cs in enumerate(cosine_similarities):
            similar_indices = cs.argsort()[:-50:-1]
            similarities[matrix.index[i]] = [(matrix.index[x], cs[x]) for x in similar_indices][1:]
        #print(f'Similarities\n{similarities}')


        # Save recommendations in cache
        cache.set(self.cache_users_key, similarities, timeout=self.timeout)
        return True

    # Return stories
    def recommend(self, user_id, max_recommendations=10):
        users_similarities = cache.get(self.cache_users_key)
        stories_matrix = cache.get(self.cache_stories_key)
        cosines = cache.get(self.cache_cosines_key)
        #print(stories_matrix)


        if not users_similarities:
            print(f'\n\nThe recommender is not trained yet, training...\n\n')
            trainning = self.train()
            if trainning:
                return self.recommend(user_id=user_id, max_recommendations=max_recommendations)
            return []


        # Remove current user from matrix
        cosines.drop(index=user_id, inplace=True)
        similar_users = cosines[cosines[user_id]>0][user_id].sort_values(ascending=False)[:10]
        #print(f'similar users\n{similar_users}')

        # Get only ids
        #similar_ids = [x[0] for x in similar_users]
        
        # Remove picked user ID from the candidate list
        #cosine_similarities_df.drop(index=picked_userid, inplace=True)

        # Take a look at the data
        #cosine_similarities_df.head()


        # Stories matrix only with user's row
        user_row = stories_matrix[stories_matrix.index == user_id].dropna(axis=1, how='all')
        #print(f'picked row\n{user_row}')

        # Stories matrix only without user's row
        similar_user_stories = stories_matrix[stories_matrix.index.isin(similar_users.index)].dropna(axis=1, how='all')
        #print(f'similar user stories\n{similar_user_stories}')


        item_score = {}
        excluded_ids = []
        # Iterate by columns
        for i, j in zip(similar_user_stories.columns, user_row.columns):
            # if user selected has rated story jumps to another column
            if user_row[j][user_id] > 0:
                excluded_ids.append(j)
                continue
            
            story_rating = similar_user_stories[i]
            
            total = 0
            # Similar users id
            
            for u in similar_users.index:
                score = similar_users[u] * story_rating[u]
                total += score
            
            item_score[i] = total

        # Convert dictionary to pandas dataframe
        item_score = pd.DataFrame(item_score.items(), columns=['story', 'score'])
        # Sort by score
        sorted_stories_ids = item_score.sort_values(by='score', ascending=False)

        
        # Recommend highest stories similarities
        strong_recommended = round(max_recommendations / 2)
        # Cut only required stories
        sorted_stories_ids = sorted_stories_ids[:strong_recommended]
        sorted_stories_ids = sorted_stories_ids['story'].tolist()

        # Recommend random stories
        random_recommended = max_recommendations - len(sorted_stories_ids)

        # search ids
        excluded_ids = excluded_ids + sorted_stories_ids
        stories_random_ids = Story.objects.all().values('id').exclude(pk__in=excluded_ids).order_by('?')
        stories_random_ids = [x['id'] for x in stories_random_ids]

        # Crop stories
        stories_random_ids = stories_random_ids[:random_recommended]

        # Get stories queryset
        stories_to_search = sorted_stories_ids + stories_random_ids
        stories_recommended = Story.objects.filter(pk__in=stories_to_search).order_by('?')

        return stories_recommended
        
        
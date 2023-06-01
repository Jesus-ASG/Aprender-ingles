import json
import pandas as pd

from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity

from main.models import Story, LikedStory, AppSettings


class UserBasedRecommender:
    def __init__(self) -> None:
        self.cache_most_rated_stories_key = 'ubr_most_rated_stories'
        self.cache_stories_key = 'ubr_stories'
        self.cache_cosines_key = 'ubr_cosines'
        self.timeout = self.get_db_timeout(1800)

    
    @staticmethod
    def get_db_timeout(default):
        settings = AppSettings.objects.filter(key='ubr').first()
        if not settings:
            return default
        try:
            settings_dict = json.loads(settings.value)
            timeout = int(settings_dict.get('timeout', default))
            if timeout < 30:
                timeout = None
            return timeout
        except:
            return default
        
    
    def update_timeout(self):
        most_rated_stories = cache.get(self.cache_most_rated_stories_key)
        stories_matrix = cache.get(self.cache_stories_key)
        cosines = cache.get(self.cache_cosines_key)

        if most_rated_stories is None or stories_matrix is None or cosines is None:
            return

        cache.set(self.cache_most_rated_stories_key, most_rated_stories, timeout=self.timeout)
        cache.set(self.cache_stories_key, stories_matrix, timeout=self.timeout)
        cache.set(self.cache_cosines_key, cosines, timeout=self.timeout)

    
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


        # Count likes
        agg_ratings = df.groupby('story_id').agg(number_of_ratings = ('rating', 'count')).reset_index()
        agg_ratings_sorted = agg_ratings.sort_values(by='number_of_ratings', ascending=False)
        cache.set(self.cache_most_rated_stories_key, agg_ratings_sorted, timeout=self.timeout)
        #print(f'agg ratings\n{agg_ratings_sorted}')


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

        return True

    # Return stories
    def recommend(self, user_id, max_recommendations=10):
        most_rated_stories = cache.get(self.cache_most_rated_stories_key)
        stories_matrix = cache.get(self.cache_stories_key)
        cosines = cache.get(self.cache_cosines_key)

        # Check if recommender is trained
        if most_rated_stories is None or stories_matrix is None or cosines is None:
            #print(f'\n\nThe recommender is not trained yet, training...\n\n')
            trainning = self.train()
            if trainning:
                return self.recommend(user_id=user_id, max_recommendations=max_recommendations)
            else:
                return Story.objects.none()
        
        # Integer to know how many similar user stories recommend
        strong_recommended = round(max_recommendations / 2)


        # Stories matrix only with user's row
        user_row = stories_matrix[stories_matrix.index == user_id]
        #print(f'picked row\n{user_row}')
        
        # If user has no likes return popular stories
        if user_row.empty:
            # Limit of stories to process
            most_rated_stories = most_rated_stories[:1000]
            #print(f'most_rated_stories \n{most_rated_stories}')

            # Get ids of most rated stories
            mr_ids = most_rated_stories['story_id'].tolist()
            # Crop most rated ids
            mr_ids = mr_ids[:strong_recommended]


            # Get random stories to fill the maximum
            random_recommended = max_recommendations - len(mr_ids)
            stories_random_ids = Story.objects.all().values('id').exclude(pk__in=mr_ids).order_by('?')
            stories_random_ids = [x['id'] for x in stories_random_ids]
            # Crop random ids
            stories_random_ids = stories_random_ids[:random_recommended]


            # Prepare ids to search
            stories_to_search = stories_random_ids + mr_ids

            # Get querysets
            stories = Story.objects.filter(pk__in=stories_to_search).order_by('?')
            return stories


        # Remove current user from matrix
        cosines.drop(index=user_id, inplace=True)
        similar_users = cosines[cosines[user_id]>0][user_id].sort_values(ascending=False)[:10]


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
        
        
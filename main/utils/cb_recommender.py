import json
import pandas as pd

from django.core.cache import cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from main.models import Story, AppSettings


class ContentBasedRecommender:
    def __init__(self) -> None:
        self.cache_key = 'cb_recommender_similarities'
        self.timeout = self.get_db_timeout(None)


    @staticmethod
    def get_db_timeout(default):
        settings = AppSettings.objects.filter(key='cbr').first()
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
        similarities = cache.get(self.cache_key)
        if similarities:
            cache.set(self.cache_key, similarities, timeout=self.timeout)
    

    def train(self, max_data=5000):
        stories = Story.objects.all()
        if not stories:
            return False
        data = []
        for story in stories:
            tag_names = [tag.name1 for tag in story.tags.all()]
            tag_names_str = ' '.join(tag_names)
            data.append({
                'id': story.id,
                'title': story.title1,
                'tags': tag_names_str,
                'description': story.description1
            })
        
        stories = pd.DataFrame(data).fillna("")
        #print(f'Training... dataframe\n{stories.head()}\n...{stories.tail()}')
        if len(stories) > max_data:
            stories = stories.sample(n=max_data)
        
        stories['data'] = stories['title'] \
                        + ' ' + stories['tags'] \
                        + ' ' + stories['description'].str.replace(r'\n', ' ', regex=True)
        
        
        tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
        stories_matrix = tfidf.fit_transform(stories['data'])
        cosine_similarities = cosine_similarity(stories_matrix) 
        similarities = {}
        for i in range(len(cosine_similarities)):
            similar_indices = cosine_similarities[i].argsort()[:-50:-1] 
            similarities[stories['id'].iloc[i]] = [(stories['id'][x], cosine_similarities[i][x]) for x in similar_indices][1:]
        
        # Set the similarities into cache
        cache.set(self.cache_key, similarities, timeout=self.timeout)
        return True

    def recommend(self, story_id, max_recommendations=10):
        # Get the similarities from cache
        matrix_similarities = cache.get(self.cache_key)
        if not matrix_similarities:
            #print(f'\n\nThe recommender is not trained yet, training...\n\n')
            trainning = self.train()
            if trainning:
                return self.recommend(story_id=story_id, max_recommendations=max_recommendations)
            return []
        #print(f'\nMatrix similarities\n{matrix_similarities}')

        # Recommendations is an array with the story id and similarity predicted
        recommendations = matrix_similarities.get(story_id)
        #print(f'\n\n{recommendations}\n\n')

        recommendations_story = []
        if (recommendations):
            recommendations = recommendations[:max_recommendations]
            for r in recommendations:
                try:
                    recommendations_story.append(Story.objects.get(id=r[0]))
                except:
                    pass
        return recommendations_story
                    

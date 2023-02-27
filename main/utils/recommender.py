# content based recommender system
import pandas as pd

from django.core.cache import cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from main.models import Story

class Recommender:
    def __init__(self) -> None:
        pass
    
    def train(self, max_data=5000):
        stories = Story.objects.all()
        if not stories:
            return False
        data = []
        for story in stories:
            related_names = [related.name1 for related in story.tag.all()]
            related_names_str = ' | '.join(related_names)
            data.append({
                'id': story.id,
                'title': story.title1,
                'tags': related_names_str,
                'description': story.description1
            })
        
        stories = pd.DataFrame(data).fillna("")
        #print(f'Training... dataframe\n{stories.head()}\n...{stories.tail()}')
        if len(stories) > max_data:
            stories = stories.sample(n=max_data)
        
        stories['data'] = stories['title'] \
                        + ' ' + stories['tags'].str.replace(r'|', ' ', regex=True) \
                        + ' ' + stories['description'].str.replace(r'|', ' ', regex=True)
        
        
        tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
        stories_matrix = tfidf.fit_transform(stories['data'])
        cosine_similarities = cosine_similarity(stories_matrix) 
        similarities = {}
        for i in range(len(cosine_similarities)):
            similar_indices = cosine_similarities[i].argsort()[:-50:-1] 
            similarities[stories['id'].iloc[i]] = [(cosine_similarities[i][x], stories['id'][x], stories['title'][x], stories['tags'][x]) for x in similar_indices][1:]
        
        # Set the similarities into cache
        cache.set('data_similarities', similarities, None)
        return True

    def recommend(self, story_id, max_recommendations=10):
        # Get the similarities from cache
        matrix_similarities = cache.get('data_similarities')
        if not matrix_similarities:
            #print('The recommender is not trained yet')
            trainning = self.train()
            if trainning:
                self.recommend()
            return
        #print(f'\nMatrix similarities\n{matrix_similarities}')
        return matrix_similarities[story_id][:max_recommendations]
        
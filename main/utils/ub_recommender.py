import pandas as pd
import numpy as np
import scipy.stats

from sklearn.metrics.pairwise import cosine_similarity

from main.models import Story


class UserBasedRecommender:
    def __init__(self) -> None:
        pass
    
    def train(self, max_data=5000):
        # Get stories data
        stories = Story.objects.all().values('id', 'title1')

        print(f'\n\nStories:\n{stories}\n\n')
        
        return True


import json

from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict

from main.models import Story, Scores, RepeatPhrase

# expiration time for cache in seconds
expiration_time = 86400

def get_or_None(object, **kwargs):
    try:
        return object.get(**kwargs)
    except:
        return None


def rateSkills(max_percentage):
    score = 'C+'
    match max_percentage:
        case num if 295 < num <= 300:
            score = 'S+'
            
        case num if 280 < num <= 295:
            score = 'S'

        case num if 270 < num <= 280:
            score = 'S-'

        case num if 265 < num <= 270:
            score = 'A+'

        case num if 257 < num <= 265:
            score = 'A'

        case num if 250 < num <= 257:
            score = 'A-'
        
        case num if 240 < num <= 250:
            score = 'B+'

        case num if 225 < num <= 240:
            score = 'B'

        case num if 210 < num <= 225:
            score = 'B-'

        case _:
            score = 'C+'
    return score


@login_required(login_url='/login/')
def storyInfo(request, route):
    try:
        user_profile = request.user.profile
        
        story = Story.objects.get(route=route)
        cache.delete(f'story_answers_{story.id}')

        # getting all fields 
        #all_stories_completed = CompletedStory.objects.filter(user=user_profile)
        #print(f'\nAll stories that {user_profile} has completed \n {all_stories_completed}\n')

        #users_who_completed = CompletedStory.objects.filter(story=story)
        #users_who_completed = story.completed_by.all()
        #print(f'\nAll users who completed {story}\n {users_who_completed}\n')

        scores = Scores.objects.filter(user_profile=user_profile, story=story).order_by('-score').values()
        high_score = None
        
        if scores:
            high_score = scores[0]
            letter_grade = ''
            
            writing_percentage = float(high_score.get('writing_percentage')) 
            comprehension_percentage = float(high_score.get('comprehension_percentage')) 
            speaking_percentage = float(high_score.get('speaking_percentage'))

            max_percentage = writing_percentage + comprehension_percentage + speaking_percentage
            letter_grade = rateSkills(max_percentage)
            
            high_score['letter_grade'] = letter_grade


        pages = story.pages.all().order_by('date_created', 'time_created').values()
        total_pages = len(pages)

        page_number = 1
        
        context = {
            'story': story, 
            'page_number': page_number,
            'total_pages': total_pages, 
            'scores': scores,
            'high_score': high_score,
            }
    except:
        return HttpResponseNotFound()
    return render(request, 'user/story_info.html', context)


@login_required(login_url='/login/')
def storyContent(request, route, page_number):
    if request.method == "GET":
        try:
            page_index = page_number - 1

            story = Story.objects.get(route=route)
            pages = story.pages.all().order_by('date_created', 'time_created')
            total_pages = len(pages)

            prev_page = None
            next_page = None
            current_page = pages[page_index]

            if page_index >= 1:
                prev_page = page_number - 1 
            if page_index < len(pages) - 1:
                next_page = page_number + 1
            
            images = current_page.images.all()
            dialogues = current_page.dialogues.all()
            repeat_phrases = current_page.repeat_phrases.all()

            dialogues = json.dumps(list(dialogues.values()))
            repeat_phrases = json.dumps(list(repeat_phrases.values()))

            images_json = []
            for image in images:
                x = model_to_dict(image)
                x['image'] = x['image'].url
                images_json.append(x)
            images_json = json.dumps(images_json)
            
            context = {
                'story': story,
                'page_number': page_number,
                'total_pages': total_pages,
                'prev_page': prev_page,
                'next_page': next_page,
                'current_page': current_page,
                'images': images,
                'images_json': images_json,
                'dialogues': dialogues,
                'repeat_phrases': repeat_phrases
                }
        except:
            return HttpResponseNotFound()
        return render(request, 'user/story_render_'+str(current_page.page_type)+'.html', context)

    if request.method == 'POST':
        story = Story.objects.get(route=route)

        # Get data from client
        evaluate = request.POST["evaluate"]
        feedback_page_id = int(request.POST["feedback_page_id"])
        user_story_answers = request.POST["story_answers"]
        user_story_answers = json.loads(user_story_answers)
        

        feedback_page = None
        cache_story_answers = cache.get(f'story_answers_{story.id}')
        if cache_story_answers is None:
            cache.set(f'story_answers_{story.id}', user_story_answers, expiration_time)
            cache_story_answers = cache.get(f'story_answers_{story.id}')

        cache_requested_page = list(filter(lambda x: x["id"] == feedback_page_id, cache_story_answers["pages"]))
        
        if cache_requested_page:
            feedback_page = cache_requested_page[0]
        else:
            user_feedback_page = list(filter(lambda x: x["id"] == feedback_page_id, user_story_answers["pages"]))
            
            cache_story_answers["pages"].append(user_feedback_page[0])
            cache.set(f'story_answers_{story.id}', cache_story_answers, expiration_time)
            cache_story_answers = cache.get(f'story_answers_{story.id}')

            cache_requested_page = list(filter(lambda x: x["id"] == feedback_page_id, cache_story_answers["pages"]))

            feedback_page = cache_requested_page[0]

        for exercise in feedback_page["exercises"]:
            match exercise["type"]:
                case "repeat_phrase":
                    rp_answ = RepeatPhrase.objects.get(id=int(exercise["id"]))
                    exercise["feedback"] = rp_answ.content1
        
        cache.set(f'story_answers_{story.id}', cache_story_answers, expiration_time)
        cache_story_answers = cache.get(f'story_answers_{story.id}')
        return JsonResponse(cache_story_answers)

def answerPage(request, route, id):
    pass
        
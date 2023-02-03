import json
import re

from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict

from main.models import Story, Score, RepeatPhrase
from main.forms import ScoreForm

# expiration time for cache in seconds
expiration_time = 86400
points_per_correct_answer = 100
tolerance_error = 3


def rateSkills(max_percentage):
    grades = ['S+', 'S', 'S-', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
    iterations = 0
    delta = 4
    aux = 100

    ranges = []
    for _ in range(len(grades)):
        ranges.append(round(aux, 2))
        aux -= delta

    iterations = 0
    for i in range(len(ranges)-1):
        if ranges[i] >= max_percentage > ranges[i+1]:
            break
        else:
            iterations += 1
    return grades[iterations]


@login_required(login_url='/login/')
def storyInfo(request, route):
    try:
        user_profile = request.user.profile
        
        story = Story.objects.get(route=route)
        cache.delete(f'story_answers_{story.id}')
        cache.delete(f'evaluated_story_{story.id}')

        # getting all fields 
        #all_stories_completed = CompletedStory.objects.filter(user=user_profile)
        #print(f'\nAll stories that {user_profile} has completed \n {all_stories_completed}\n')

        #users_who_completed = CompletedStory.objects.filter(story=story)
        #users_who_completed = story.completed_by.all()
        #print(f'\nAll users who completed {story}\n {users_who_completed}\n')

        scores = Score.objects.filter(user_profile=user_profile, story=story).order_by('-score').values()
        high_score = None
        
        if scores:
            high_score = scores[0]
            letter_grade = ''

            max_percentage = float(high_score.get('score')) / float(high_score.get('score_limit'))
            max_percentage = max_percentage * 100
            max_percentage = round(max_percentage, 2)

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
        user_profile = request.user.profile

        # Get data from client
        evaluate = request.POST["evaluate"]
        feedback_page_id = int(request.POST["feedback_page_id"])
        user_story_answers = request.POST["story_answers"]

        evaluate = json.loads(evaluate)
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


        cache_evaluated_story = cache.get(f'evaluated_story_{story.id}')
        if cache_evaluated_story is None:
            cache_evaluated_story = False
        
        results = ""
        if evaluate and not cache_evaluated_story:
            # evaluate means give all califications
            results = evaluateAnswers(story, cache_story_answers)
            cache.set(f'evaluated_story_{story.id}', True, expiration_time)

            score_form = ScoreForm(request.POST or None)
            if not score_form.is_valid():
                pass

            score_form_obj = score_form.save(commit=False)

            score_form_obj.user_profile = user_profile
            score_form_obj.story = story

            score_form_obj.score = results["score"]
            score_form_obj.score_limit = results["score_limit"]
            score_form_obj.writing_percentage = results["writing_percentage"]
            score_form_obj.comprehension_percentage = results["comprehension_percentage"]
            score_form_obj.speaking_percentage = results["speaking_percentage"]
            
            max_percentage = float(results.get('score')) / float(results.get('score_limit'))
            max_percentage = max_percentage * 100
            max_percentage = round(max_percentage, 2)
            letter_grade = rateSkills(max_percentage)

            score_form_obj.save()

            cache_story_answers["score"] = results
            cache_story_answers["score"]["letter_grade"] = letter_grade

            cache.set(f'story_answers_{story.id}', cache_story_answers, expiration_time)
        

        return JsonResponse(cache_story_answers)


def evaluateAnswers(story, story_answers):
    # count all elements
    exercises_number = 0
    pages = story.pages.all()
    for p in pages:
        repeat_phrases = p.repeat_phrases.all()
        exercises_number  += len(repeat_phrases)

    results = {
        "score": 0, 
        "writing_percentage": 0, 
        "comprehension_percentage": 0, 
        "speaking_percentage": 0
    }
    
    for page in story_answers["pages"]:
        for exercise in page["exercises"]:
            match exercise["type"]:
                case "repeat_phrase":
                    rp = RepeatPhrase.objects.get(id=int(exercise["id"]))
                    answ_r = cleanStr(rp.content1)
                    answ_u = cleanStr(exercise["answer"])
                    rp_results = evaluateRepeatPhrase(answ_r, answ_u)

                    results["score"] += rp_results["score"]
                    results["writing_percentage"] += rp_results["writing_percentage"]
                    results["comprehension_percentage"] += rp_results["comprehension_percentage"]
                    results["speaking_percentage"] += rp_results["speaking_percentage"]
                    
    
    wp_t = (results["writing_percentage"] / exercises_number) * 100
    cp_t = (results["comprehension_percentage"] / exercises_number) * 100
    sp_t = (results["speaking_percentage"] / exercises_number) * 100

    results["score"] = int(results["score"])
    results["score_limit"] = exercises_number * points_per_correct_answer

    results["writing_percentage"] = round(wp_t, 2)
    results["comprehension_percentage"] = round(cp_t, 2)
    results["speaking_percentage"] = round(sp_t, 2)
    
    return results


def cleanStr(string):
    only_alpha_numerics = re.sub(r'[^A-Za-z0-9 ]+', ' ', string)
    only_one_space = re.sub(' +', ' ', only_alpha_numerics)
    lower_strip = only_one_space.lower().strip()
    return lower_strip


def searchPage(page_id, page_list):
    return list(filter(lambda x: x["id"] == page_id, page_list))


def evaluateRepeatPhrase(answer_right, answer_user):
    if answer_user == "":
        results = {
            "score": 0, 
            "writing_percentage": 1, 
            "comprehension_percentage": 0, 
            "speaking_percentage": 0
        }
        return results

    answer_right = answer_right.split(' ')
    answer_user = answer_user.split(' ')

    index = 0
    total_words = len(answer_right)
    total_user_words = len(answer_user)
    correct_words = 0
    incorrect_words = 0

    len_diff = abs(total_words - total_user_words)

    for i in range(total_words):
        for j in range(index, total_user_words):
            if answer_right[i] == answer_user[j]:
                correct_words = correct_words + 1
                index = j + 1
                break

    
    incorrect_words = incorrect_words + len_diff

    score = 0
    writing_percentage = 1
    comprehension_percentage = 0
    speaking_percentage = 0
    
    quit_points = (incorrect_words / (total_words * tolerance_error ))

    comprehension_percentage = (correct_words / total_words) - quit_points

    speaking_percentage = (correct_words / total_words) - quit_points
    score = points_per_correct_answer - quit_points * points_per_correct_answer
    
    comprehension_percentage = 0 if (comprehension_percentage < 0) else comprehension_percentage
    speaking_percentage = 0 if (speaking_percentage < 0) else speaking_percentage
    score = 0 if (score < 0) else score

    results = {
        "score": score, 
        "writing_percentage": writing_percentage, 
        "comprehension_percentage": comprehension_percentage, 
        "speaking_percentage": speaking_percentage
    }
    return results


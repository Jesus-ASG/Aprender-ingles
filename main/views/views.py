import json

from rest_framework.renderers import JSONRenderer

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Subquery, OuterRef, Max
from django.http import HttpResponseNotFound, JsonResponse

from main.models import Story, Tag, UserProfile, Score
from main.models import RepeatPhrase, Spellcheck, MultipleChoiceQuestion
from main.forms import SelectDefaultImageForm, ScoreForm, UserAnswer

from main.utils.ub_recommender import UserBasedRecommender
from main.utils.cb_recommender import ContentBasedRecommender
from main.utils.level_manager import LevelManager
from main.utils.evaluate_story import rateSkills, evaluateAnswers, map_answers

from main.utils.paginate_and_filter import paginate_stories

from main.serializers import MultipleChoiceQuestionSerializer


def not_found_page(request, exception):
    return render(request, 'utils/404_page.html', {})

def test_not_found(request):
    return render(request, 'utils/404_page.html', {})

def index(request):
    
    if not request.user.is_authenticated:
        return render(request, 'no-logged/home.html')
    if request.method == 'GET':
        page_title = 'Recommended'
        message_if_empty = ''
        ubr = UserBasedRecommender()
        user_profile = request.user.profile
        stories = ubr.recommend(user_profile.id, max_recommendations=6)
        #print(user_profile.id)
        #stories = Story.objects.all()
        context = {
            'page_title': page_title,
            'message_if_empty': message_if_empty,
            'stories': stories,
        }
        
        return render(request, 'user/index_user.html', context=context)


@login_required(login_url='/login/')
def profile(request):

    profile = request.user.profile
    default_image_form = SelectDefaultImageForm(instance=profile)

    lvl_obj = LevelManager()
    level_statistics = lvl_obj.get_level_statistics(profile.xp)

    statistics = {
        'level': level_statistics
    }

    context = {
        'profile': profile,
        'statistics': statistics,
        'default_image_form': default_image_form
    }

    if request.method == 'GET':
        max_scores = Score.objects.filter(user_profile=profile).values('story').annotate(max_score_percentage=Max('score_percentage'))
        
        subquery = max_scores.filter(story=OuterRef('story')).values('max_score_percentage')
        user_scores = Score.objects.filter(user_profile=profile, score_percentage__in=Subquery(subquery))

        # Uniques high scores
        u_high_scores = []
        user_scores = user_scores.order_by('-score_percentage', 'date')
        for i in user_scores:
            if not i.story in [x['score'].story for x in u_high_scores]:
                grade = rateSkills(i.score_percentage)
                u_high_scores.append({'score': i, 'grade': grade})

        wa = 0
        ca = 0
        sa = 0
        for i in u_high_scores:
            wa += i['score'].writing_percentage
            ca += i['score'].comprehension_percentage
            sa += i['score'].speaking_percentage
        num_elements = 1 if len(u_high_scores) <= 0 else len(u_high_scores)
        wa = wa / num_elements
        ca = ca / num_elements
        sa = sa / num_elements

        wg = rateSkills(wa)
        cg = rateSkills(ca)
        sg = rateSkills(sa)
        
        context['statistics']['writing'] = { 'average': wa, 'grade':wg }
        context['statistics']['comprehension'] = { 'average': ca, 'grade':cg }
        context['statistics']['speaking'] = { 'average': sa, 'grade':sg }
        
        context['u_high_scores'] = u_high_scores

        return render(request, 'user/profile.html', context)
    
    if request.method == 'POST':
        default_image_form = SelectDefaultImageForm(request.POST or None)
        if not default_image_form.is_valid():
            return render(request, 'user/profile.html', context)
        
        profile_obj = UserProfile.objects.get(user=request.user)
        profile_obj.default_profile_image = default_image_form.cleaned_data['default_profile_image']
        profile_obj.save()
        
        #context['success'] = True
        # Update
        return redirect('profile')
        #return render(request, 'user/profile.html', context)


@login_required(login_url='/login/')
def storiesGallery(request):
    if request.method == 'GET':

        context = paginate_stories(request, items_per_page=8)
        
        return render(request, 'user/stories_gallery.html', context)


@login_required(login_url='/login/')
def storyInfo(request, route):
    user_profile = request.user.profile
    
    story = Story.objects.get(route=route)

    # Get recommendations
    recommender = ContentBasedRecommender()
    recommendations_list = recommender.recommend(story_id=story.id, max_recommendations=4)

    # check if user likes the story
    story_liked = False
    if story in user_profile.liked_stories.all():
        story_liked = True
    story_liked = json.dumps(story_liked)
    
    # check if user has saved the story
    story_saved = False
    if story in user_profile.saved_stories.all():
        story_saved = True
    story_saved = json.dumps(story_saved)
    
    scores = Score.objects.filter(user_profile=user_profile, story=story).order_by('-score_percentage', 'date').values()
    high_score = None
    
    if scores:
        high_score = scores[0]
        letter_grade = rateSkills(high_score.get('score_percentage'))
        high_score['letter_grade'] = letter_grade


    pages = story.pages.all().order_by('date_created', 'time_created').values()
    total_pages = len(pages)

    page_number = 1
    
    context = {
        'story': story,
        'recommendations_list': recommendations_list,
        'story_liked': story_liked,
        'story_saved': story_saved,
        'page_number': page_number,
        'total_pages': total_pages,
        'scores': scores,
        'high_score': high_score,
        }
    return render(request, 'user/story_info.html', context)


@login_required(login_url='/login/')
def pageDisplayer(request, route, page_number):
    
    story = Story.objects.get(route=route)
    user_profile = request.user.profile
    
    page_index = page_number - 1
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
    videos = current_page.videos.all()
    texts = current_page.texts.all()
    dialogues = current_page.dialogues.all()
    repeat_phrases = current_page.repeat_phrases.all()
    spellchecks = current_page.spellchecks.all()
    mc_questions = current_page.questions.all()

    mc_questions_s = MultipleChoiceQuestionSerializer(mc_questions, many=True)
    
    
    db_answers = user_profile.answers.filter(page=current_page)

    rp_content_type = ContentType.objects.get_for_model(RepeatPhrase)
    spc_content_type = ContentType.objects.get_for_model(Spellcheck)
    mcq_content_type = ContentType.objects.get_for_model(MultipleChoiceQuestion)


    if request.method == "GET":
        answers = []

        if db_answers:
            answers = map_answers(db_answers)
        
        score = None
        story_answered = UserAnswer.objects.filter(user_profile=user_profile, story=story).first()
        if story_answered:
            if story_answered.evaluated:
                score = Score.objects.filter(user_profile=user_profile, story=story).order_by('-date').values().first()
                
                letter_grade = rateSkills(score['score_percentage'])
                score['letter_grade'] = letter_grade
                score = json.dumps(score, indent=4, sort_keys=True, default=str)

        answers = json.dumps(answers)

        images = json.dumps(list(images.values()))
        videos = json.dumps(list(videos.values()))
        texts = json.dumps(list(texts.values()))
        dialogues = json.dumps(list(dialogues.values()))
        repeat_phrases = json.dumps(list(repeat_phrases.values()))
        spellchecks = json.dumps(list(spellchecks.values()))

        mc_questions = JSONRenderer().render(mc_questions_s.data).decode('utf-8')
        
        context = {
            'story': story,
            'page_number': page_number,
            'total_pages': total_pages,
            'prev_page': prev_page,
            'next_page': next_page,
            'current_page': current_page,
            'media_url': settings.MEDIA_URL,
            'images': images,
            'videos': videos,
            'texts': texts,
            'dialogues': dialogues,
            'repeat_phrases': repeat_phrases,
            'spellchecks': spellchecks,
            'mc_questions': mc_questions,
            'answers': answers,
            'score': score
            }
        return render(request, 'page_display/page_display.html', context)


    if request.method == 'POST':        
        update = False
        if db_answers:
            if db_answers[0].submited:
                return JsonResponse({'message': 'This page is already submited'})
            else: # update answers
                update = True

        # Get data from client
        evaluate = request.POST['evaluate']
        submit = request.POST['submit']
        answers = request.POST['answers']
        
        evaluate = json.loads(evaluate)
        answers = json.loads(answers)
        submit = json.loads(submit)
        
        # Filter exercises
        rp_answered = db_answers.filter(exercise_type=rp_content_type)
        spc_answered = db_answers.filter(exercise_type=spc_content_type)
        mcq_answered = db_answers.filter(exercise_type=mcq_content_type)
        
        # Save answers
        for exercise in answers:
            match exercise['type']:
                case 'repeat_phrase':
                    rp = repeat_phrases.get(pk=int(exercise['id']))
                    
                    if update:
                        answer_update_obj = rp_answered.filter(exercise_id=rp.pk)
                        if exercise['answer'] == '':
                            answer_update_obj.update(submited=submit)
                        else:
                            answer_update_obj.update(
                                answer=exercise['answer'],
                                submited=submit,
                            )
                    else:
                        answer_obj = UserAnswer.objects.create(
                            user_profile=user_profile,
                            story=story,
                            page=current_page,
                            exercise_type=ContentType.objects.get_for_model(rp),
                            exercise_id=rp.pk,
                            answer=exercise['answer'],
                            submited=submit,
                        )
                case 'spellcheck':
                    spc = spellchecks.get(pk=int(exercise['id']))
                    
                    if update:
                        answer_update_obj = spc_answered.filter(exercise_id=spc.pk)
                        if exercise['answer'] == '':
                            answer_update_obj.update(submited=submit)
                        else:
                            answer_update_obj.update(
                                answer=exercise['answer'],
                                submited=submit,
                            )
                    else:
                        answer_obj = UserAnswer.objects.create(
                            user_profile=user_profile,
                            story=story,
                            page=current_page,
                            exercise_type=ContentType.objects.get_for_model(spc),
                            exercise_id=spc.pk,
                            answer=exercise['answer'],
                            submited=submit,
                        )
                case 'mc_question':
                    q = mc_questions.get(pk=int(exercise['id']))
                    
                    if update:
                        answer_update_obj = mcq_answered.filter(exercise_id=q.pk)
                        if exercise['answer'] == '':
                            answer_update_obj.update(submited=submit)
                        else:
                            answer_update_obj.update(
                                answer=exercise['answer'],
                                submited=submit,
                            )
                    else:
                        answer_obj = UserAnswer.objects.create(
                            user_profile=user_profile,
                            story=story,
                            page=current_page,
                            exercise_type=ContentType.objects.get_for_model(q),
                            exercise_id=q.pk,
                            answer=exercise['answer'],
                            submited=submit,
                        )


        # Get updated objects
        story_answers = UserAnswer.objects.filter(user_profile=user_profile, story=story)
        db_answers = story_answers.filter(page=current_page)
        feedback_answers = map_answers(db_answers)

        response = {}
        response['answers'] = feedback_answers
        
        results = ""
        if evaluate:
            # Give form to answers
            answers = []
            if story_answers:
                evaluated = story_answers[0].evaluated
                if evaluated:
                    return JsonResponse({'message': 'This story is already answered'})
                
                # Map all the story answers
                answers = map_answers(story_answers)
            
            results = evaluateAnswers(story, answers)
            
            score_form = ScoreForm(request.POST or None)
            if not score_form.is_valid():
                pass

            score_form_obj = score_form.save(commit=False)

            #score_form_obj = Score()

            score_form_obj.user_profile = user_profile
            score_form_obj.story = story

            score_form_obj.score = results["score"]
            score_form_obj.score_limit = results["score_limit"]
            score_form_obj.writing_percentage = results["writing_percentage"]
            score_form_obj.comprehension_percentage = results["comprehension_percentage"]
            score_form_obj.speaking_percentage = results["speaking_percentage"]
            
            score_form_obj.score_percentage = results['score_percentage']

            letter_grade = rateSkills(results['score_percentage'])
            results['letter_grade'] = letter_grade

            score_form_obj.save()

            user_profile.xp += results.get('score', 0)
            # update level
            lvl_obj = LevelManager()
            level_statistics = lvl_obj.get_level_statistics(user_profile.xp)
            user_profile.level = level_statistics['level']
            user_profile.save()
            
            # Update story answers to evaluated
            story_answers.update(evaluated=True)
            story_answers.update(submited=True)
            response['results'] = results
            
        return JsonResponse(response)

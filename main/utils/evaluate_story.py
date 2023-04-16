import re
from main.models import RepeatPhrase, Spellcheck
from django.contrib.contenttypes.models import ContentType


points_per_correct_answer = 100
tolerance_error = 4


def map_answers(db_answers):
    mapped_list = []
    if db_answers:
        # Repeat phrases
        rp_content_type = ContentType.objects.get_for_model(RepeatPhrase)
        rp_answered = db_answers.filter(exercise_type=rp_content_type)
        for i in rp_answered:
            obj = {
                'exercise_id': i.exercise_id,
                'answer': i.answer,
                'feedback': i.exercise.content1,
                'submited': i.submited,
                'type': 'repeat_phrase'
            }
            mapped_list.append(obj)

        # spellchecks
        spc_content_type = ContentType.objects.get_for_model(Spellcheck)
        spc_answered = db_answers.filter(exercise_type=spc_content_type)
        for i in spc_answered:
            obj = {
                'exercise_id': i.exercise_id,
                'answer': i.answer,
                'feedback': i.exercise.right_text,
                'submited': i.submited,
                'type': 'spellcheck'
            }
            mapped_list.append(obj)

    return mapped_list


def cleanStr(string):
    only_alpha_numerics = re.sub(r'[^A-Za-z0-9 ]+', ' ', string)
    only_one_space = re.sub(' +', ' ', only_alpha_numerics)
    lower_strip = only_one_space.lower().strip()
    return lower_strip

def searchPage(page_id, page_list):
    return list(filter(lambda x: x["id"] == page_id, page_list))


def rateSkills(max_percentage):
    if not max_percentage:
        return '?'
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


def evaluateRepeatPhrase(user_answer, correct_answer):
    if user_answer == "":
        results = {
            "score": 0,
            "comprehension_percentage": 0, 
            "speaking_percentage": 0
        }
        return results

    user_answer = user_answer.split(' ')
    correct_answer = correct_answer.split(' ')

    total_user_words = len(user_answer)
    total_correct_words = len(correct_answer)
    
    correct_words = 0
    penalty_words = total_user_words - total_correct_words if total_user_words > total_correct_words else 0

    index_user = 0
    index_correct = 0
    
    for i in range(index_user, total_user_words):
        for j in range(index_correct, total_correct_words):
            if user_answer[i] == correct_answer[j]:
                correct_words = correct_words + 1
                index_correct = j + 1
                index_user += 1
                break

    score = 0
    
    speaking_percentage = 0
    quit_points = 0
    if tolerance_error != 0:
        quit_points = penalty_words / (total_correct_words * tolerance_error )

    speaking_percentage = (correct_words / total_correct_words) - abs(quit_points)
    speaking_percentage = 0 if speaking_percentage < 0 else speaking_percentage
    speaking_percentage = round(speaking_percentage, 2)

    score = points_per_correct_answer - quit_points * points_per_correct_answer
    score = 0 if (score < 0) else score

    results = {
        "score": round(score, 2),
        "comprehension_percentage": speaking_percentage, 
        "speaking_percentage": speaking_percentage
    }
    return results


def evaluateSpellcheck(user_answer, correct_answer):
    if user_answer == "":
        results = {
            "score": 0, 
            "writing_percentage": 0, 
            "comprehension_percentage": 0
        }
        return results
    
    user_answer = user_answer.split(' ')
    correct_answer = correct_answer.split(' ')

    total_user_words = len(user_answer)
    total_correct_words = len(correct_answer)
    
    correct_words = 0
    penalty_words = total_user_words - total_correct_words if total_user_words > total_correct_words else 0

    index_user = 0
    index_correct = 0
    
    for i in range(index_user, total_user_words):
        for j in range(index_correct, total_correct_words):
            if user_answer[i] == correct_answer[j]:
                correct_words = correct_words + 1
                index_correct = j + 1
                index_user += 1
                break

    score = 0
    
    writing_percentage = 0
    quit_points = 0
    if tolerance_error != 0:
        quit_points = penalty_words / (total_correct_words * tolerance_error )

    writing_percentage = (correct_words / total_correct_words) - abs(quit_points)
    writing_percentage = 0 if writing_percentage < 0 else writing_percentage
    writing_percentage = round(writing_percentage, 2)

    score = points_per_correct_answer - quit_points * points_per_correct_answer
    score = 0 if (score < 0) else score

    results = {
        "score": round(score, 2), 
        "writing_percentage": writing_percentage, 
        "comprehension_percentage": writing_percentage
    }
    return results


def evaluateAnswers(story, answers):
    # count all elements
    exercises_number = 0
    rp_count = 0
    spc_count = 0
    pages = story.pages.all()
    for p in pages:
        rp_count  += p.repeat_phrases.all().count()
        spc_count += p.spellchecks.all().count()
    
    exercises_number = rp_count + spc_count

    results = {
        "score": 0, 
        "writing_percentage": 0, 
        "comprehension_percentage": 0, 
        "speaking_percentage": 0,
        "score_percentage": 0
    }
    if exercises_number <= 0:
        return results


    for a in answers:
        match a['type']:
            case 'repeat_phrase':
                correct_answer = cleanStr(a['feedback'])
                user_answer = cleanStr(a['answer'])
                rp_results = evaluateRepeatPhrase(user_answer, correct_answer)

                results["score"] += rp_results["score"]
                results["comprehension_percentage"] += rp_results["comprehension_percentage"]
                results["speaking_percentage"] += rp_results["speaking_percentage"]

            case 'spellcheck':
                correct_answer = a['feedback']
                user_answer = a['answer']
                spc_results = evaluateSpellcheck(user_answer, correct_answer)

                results["score"] += spc_results["score"]
                results["writing_percentage"] += spc_results["writing_percentage"]
                results["comprehension_percentage"] += spc_results["comprehension_percentage"]
                

    # Execises count
    writing_count = spc_count
    speaking_count = rp_count

    wp_t = (results["writing_percentage"] / writing_count) * 100 if writing_count > 0 else 100
    sp_t = (results["speaking_percentage"] / speaking_count) * 100 if speaking_count > 0 else 100

    cp_t = (results["comprehension_percentage"] / exercises_number) * 100

    results["score"] = int(results["score"])
    results["score_limit"] = exercises_number * points_per_correct_answer

    results["writing_percentage"] = round(wp_t, 2)
    results["comprehension_percentage"] = round(cp_t, 2)
    results["speaking_percentage"] = round(sp_t, 2)

    #score_percentage = results["writing_percentage"] + results['comprehension_percentage'] + results['speaking_percentage']
    #score_percentage = score_percentage / 3
    score_percentage = results['comprehension_percentage']
    results['score_percentage'] = round(score_percentage, 2)
    
    return results
    

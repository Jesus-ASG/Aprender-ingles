import re
from main.models import RepeatPhrase


points_per_correct_answer = 100
tolerance_error = 3

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
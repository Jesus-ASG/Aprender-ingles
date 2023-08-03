import json
import uuid

from django.core.files import File

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse

from main.models import Story, Page, Audio, Video, Image, Text, Dialogue, RepeatPhrase, Spellcheck, MultipleChoiceQuestion, QuestionChoice
from main.forms import DialogueForm, PageForm, RepeatPhraseForm
from main.serializers import MultipleChoiceQuestionSerializer, PageSerializer
from rest_framework.renderers import JSONRenderer


MAX_PAGE_TYPES = 3


def is_staff(user):
    return user.is_staff


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def index(request, route):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all().order_by('date_created', 'time_created').values()
    except:
        return HttpResponseNotFound()
    return render(request, 'admin/view_pages.html', {'story':story, 'pages':pages})


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def create(request, route, page_type):
    if not 0 < page_type <= MAX_PAGE_TYPES:
        return HttpResponseNotFound()
    try:
        story = Story.objects.get(route=route)
    except:
        return HttpResponseNotFound()

    if request.method == "GET":
        context = {
            'story': story, 
            'page_type': page_type
        }
        return render(request, 'page_editor/page_editor.html', context)


    if request.method == "POST":
        if page_type == 0:
            return HttpResponseNotFound()
        
        # create all forms
        pgForm = PageForm(request.POST or None)
        #imgForm = ImageForm(request.POST or None, request.FILES or None)
        diaForm = DialogueForm(request.POST or None)
        repPForm = RepeatPhraseForm(request.POST or None)

        # validation
        if ((not pgForm.is_valid()) or (not diaForm.is_valid()) or 
                (not repPForm.is_valid())):
            return JsonResponse({'message': 'error validating'})

        # collecting data
        data = request.POST["data"]
        data = json.loads(data)
        
        # creating page
        pgObj = pgForm.save(commit=False)
        if data["page_id"] != 0:
            pgObj = Page.objects.get(id=int(data["page_id"]))
        
        pgObj.story = story
        pgObj.subtitle1 = data["sub1"]
        pgObj.subtitle2 = data["sub2"]
        pgObj.page_type = page_type
        
        
        # Images
        images_to_submit = []
        images = data["images"]
        
        for img in images:
            
            imgObj = Image()
            imgObj.page = pgObj

            if img["id"] != "":
                imgObj = Image.objects.get(id=int(img["id"]))
            
            imgObj.element_number = img["element_number"]

            file_key = img['file_key']
            if file_key == '': # if user didn't send an image file
                if not imgObj.image: # previous imgObj don't have an image
                    if pgObj.page_type == 1: # doesn't matter if imgObj don't have image because it can
                        continue
                    else: # Any other template with image input empty will be returned as an error
                        return JsonResponse({'message': 'Must select an image file'})
                
            else: # user has sent an image file
                img_file = request.FILES.get(file_key)

                extension = img_file.name.split('.')[-1]
                random_name = f'{uuid.uuid4()}.{extension}'

                imgObj.image.save(random_name, File(img_file), save=False)
            images_to_submit.append(imgObj)


        # Videos
        videos_to_submit = []
        videos = data.get("videos", [])
        for v in videos:
            if v['url'] == '':
                return JsonResponse({'message': 'url content cannot be empty'})
            video_obj = Video()
            video_obj.page = pgObj

            if v['id'] != '':
                video_obj = Video.objects.get(id=int(v['id']))
            
            video_obj.element_number = v.get('element_number', 0)
            video_obj.url = v['url']

            videos_to_submit.append(video_obj)


        # Audios
        audios_to_submit = []
        audios = data["audios"]
        
        for a in audios:
            # Validate fields
            if a['show_description']:
                if a['description'] == '' or a['t_description'] == '':
                    return JsonResponse({'message': 'Both description must have content'})
            
            audio_obj = Audio()
            audio_obj.page = pgObj

            if a["id"] != "":
                audio_obj = Audio.objects.get(id=int(a["id"]))
            
            audio_obj.element_number = a["element_number"]
            audio_obj.label_name = a["label_name"]
            audio_obj.show_description = a["show_description"]
            audio_obj.description = a["description"]
            audio_obj.t_description = a["t_description"]


            file_key = a['file_key']
            if file_key == '': # if user didn't send an audio file
                if not audio_obj.audio_file: # previous audio_obj don't have an audio file
                    return JsonResponse({'message': 'Must select an audio file'})
                
            else: # user has sent an audio file
                audio_file = request.FILES.get(file_key)

                extension = audio_file.name.split('.')[-1]
                random_name = f'{uuid.uuid4()}.{extension}'

                audio_obj.audio_file.save(random_name, File(audio_file), save=False)
            audios_to_submit.append(audio_obj)


        # Texts
        texts_to_submit = []
        texts = data["texts"]
        for t in texts:
            if t['language1'] == '' or t['language1'] == '':
                return JsonResponse({'message': 'texts contents cannot have empty values'})
            
            textObj = Text()
            textObj.page = pgObj

            if t['id'] != '':
                textObj = Text.objects.get(id=int(t['id']))
            
            textObj.element_number = t['element_number']
            textObj.language1 = t['language1']
            textObj.language2 = t['language2']

            texts_to_submit.append(textObj)

        # Dialogues
        dialogues_to_submit = []
        dialogues = data["dialogues"]
        for d in dialogues:
            if d["name"] == "" or d["language1"] == "" or d["language2"] == "":
                return JsonResponse({'message': 'dialogues contents cannot have empty values'})
            
            diaObj = diaForm.save(commit=False)
            if d["id"] != "":
                diaObj = Dialogue.objects.get(id=int(d["id"]))
            diaObj.page = pgObj
            diaObj.element_number = d["element_number"]

            diaObj.name = d["name"]
            diaObj.content1 = d["language1"]
            diaObj.content2 = d["language2"]
            diaObj.color = d["color"]
            dialogues_to_submit.append(diaObj)
            diaForm = DialogueForm(request.POST or None)
        
        # Repeat phrases
        repeatPhrases_to_submit = []
        repeatPhrases = data["repeatPhrases"]
        for rp in repeatPhrases:
            if rp["language1"] == "" or rp["language2"] == "":
                return JsonResponse({'message': 'repeat phrases empty fields'})
            
            rpPObj = repPForm.save(commit=False)
            if rp["id"] != "":
                rpPObj = RepeatPhrase.objects.get(id=int(rp["id"]))
            rpPObj.page = pgObj
            rpPObj.content1 = rp["language1"]
            rpPObj.content2 = rp["language2"]
            rpPObj.element_number = rp["element_number"]
            rpPObj.show_text = rp["show_text"]
            repeatPhrases_to_submit.append(rpPObj)
            repPForm = RepeatPhraseForm(request.POST or None)    
        
        # Spellchecks
        spellchecks_to_submit = []
        spellchecks = data['spellchecks']
        for s in spellchecks:
            if s['wrong_text'] == '' or s['right_text'] == '' or s['translated_right_text']=='':
                return JsonResponse({'message': 'spellchecks empty fields'})
            
            spcObj = Spellcheck()
            spcObj.page = pgObj
            if s['id'] != '':
                spcObj = Spellcheck.objects.get(id=int(s['id']))
            
            spcObj.element_number = s['element_number']
            spcObj.wrong_text = s['wrong_text']
            spcObj.right_text = s['right_text']
            spcObj.translated_right_text = s['translated_right_text']
            spellchecks_to_submit.append(spcObj)

        
        # Multiple Choice Questions
        mc_to_submit = []
        choices_to_submit = []
        mcq = data['mc_questions']
        for q in mcq:
            if q['text'] == '' or q['t_text'] == '':
                return JsonResponse({'message': 'The questions cannot be empty'})
            
            qObj = MultipleChoiceQuestion()
            qObj.page = pgObj
            if q['id'] != '':
                qObj = MultipleChoiceQuestion.objects.get(id=int(q['id']))

            qObj.element_number = q['element_number']
            qObj.text = q['text']
            qObj.t_text = q['t_text']
            qObj.randomize_choices = q['randomize_choices']


            choices = q['choices']
            corrects = 0
            for c in choices:
                if c['text'] == '' or c['t_text'] == '':
                    return JsonResponse({'message': 'The choices cannot be empty'})

                cObj = QuestionChoice()
                cObj.question = qObj
                if c['id'] != '':
                    cObj = QuestionChoice.objects.get(id=int(c['id']))

                cObj.choice_number = c['choice_number']
                cObj.text = c['text']
                cObj.t_text = c['t_text']
                
                correct = c['correct']
                cObj.correct = correct
                if correct:
                    corrects += 1

                choices_to_submit.append(cObj)
            if corrects == 0:
                return JsonResponse({'message': 'You need to mark one option as correct'})
            if corrects > 1:
                return JsonResponse({'message': 'You can\'t mark more than one option as correct'})

            mc_to_submit.append(qObj)

        
        # Delete objects that were deleted
        deleted = data["deleted"]
        for d in deleted['images']:
            safe_delete(Image, d)

        for d in deleted['videos']:
            safe_delete(Video, d)

        for d in deleted['audios']:
            safe_delete(Audio, d)

        for d in deleted['texts']:
            safe_delete(Text, d)

        for d in deleted['dialogues']:
            safe_delete(Dialogue, d)
        
        for d in deleted['repeatPhrases']:
            safe_delete(RepeatPhrase, d)

        for d in deleted['spellchecks']:
            safe_delete(Spellcheck, d)

        for d in deleted['mc_questions']:
            safe_delete(MultipleChoiceQuestion, d)

        for d in deleted['question_choices']:
            safe_delete(QuestionChoice, d)
        
        #"""
        # Save all
        pgObj.save()
        
        # Content
        # Videos
        for video in videos_to_submit:
            video.save()

        # Audios
        for audio in audios_to_submit:
            audio.save()

        # Images
        for image in images_to_submit:
            image.save()

        for text in texts_to_submit:
            text.save()
        
        # Dialogues
        for dialogue in dialogues_to_submit:
            dialogue.save()
        
        # Repeat phrases
        for repeatPhrase in repeatPhrases_to_submit:
            repeatPhrase.save()

        # Spellchecks
        for spc in spellchecks_to_submit:
            spc.save()

        # Multiple choice questions
        for q in mc_to_submit:
            q.save()

        # Question choices
        for c in choices_to_submit:
            c.save()
        #"""
        return JsonResponse({'message': 'success'})
        

@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def update(request, route, page_type, page_id):
    if not 0 < page_type <= MAX_PAGE_TYPES:
        return HttpResponseNotFound()
    
    # get content
    story = Story.objects.get(route=route)
    page = story.pages.get(id=page_id)

    json_page = PageSerializer(page)
    json_page = JSONRenderer().render(json_page.data).decode('utf-8')

    context = {
        'story': story, 
        'page_type': page_type,
        'json_page': json_page
    }
    
    if request.method == "GET":
        return render(request, 'page_editor/page_editor.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def delete(request, id):
    if request.method == "POST":
        try:
            page = Page.objects.get(id=id)
            page.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponseBadRequest('')


def safe_delete(model, id):
    try:
        model.objects.get(id=int(id)).delete()
    except:
        pass
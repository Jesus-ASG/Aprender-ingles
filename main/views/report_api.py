import json

from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

from main.models import Story, StoryReport


def is_staff(user):
    return user.is_staff


@login_required(login_url='/login/')
def send_report(request):
    if request.method == 'POST':
        key = f'user_request_reports_{request.user.id}'
        rate_limit = 1000 ##############################################
        rate_limit_time = 30

        num_requests = cache.get(key, 0)
        if num_requests >= rate_limit:
            response = {
                'success': True, 
                'message': 'Please, wait before send another report.',
                'message_t': 'Por favor, espere antes de enviar otro reporte.'
            }
            return JsonResponse(response)
        cache.set(key, num_requests + 1, rate_limit_time)


        story_id = request.POST.get('story_id')
        description = request.POST.get('description')

        story = Story.objects.get(pk=int(story_id))
        profile = request.user.profile

        report_obj = StoryReport()
        report_obj.story = story
        report_obj.user_profile = profile
        report_obj.description = description

        report_obj.save()

        response = {
            'success': True, 
            'message': 'Thank you for your comments.',
            'message_t': 'Gracias por sus comentarios.'
        }

        return JsonResponse(response)
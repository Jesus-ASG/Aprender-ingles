from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse
from django.template import loader

from main.models import Story, StoryReport
from main.serializers import StoryReportSerializer


def is_staff(user):
    return user.is_staff


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def get_reports(request):
    if request.method == 'GET':
        reports = StoryReport.objects.all()

        status = request.GET.get('status')

        if status:
            reports = reports.filter(status=status)
        
        # Sort reports
        reports = reports.order_by('-created_at')
        template = loader.get_template('parts/reports_table.html').render(
            context={'reports': reports}
        )

        return HttpResponse(template)
    

def update_report_status(request, report_id):
    
    pass


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

        story_id = request.POST.get('story_id')
        description = request.POST.get('description')
        if description == '':
            response = {
                'success': True, 
                'message': 'Please, describe the problem.',
                'message_t': 'Por favor, describa el problema.'
            }
            return JsonResponse(response)


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

        cache.set(key, num_requests + 1, rate_limit_time)
        return JsonResponse(response)
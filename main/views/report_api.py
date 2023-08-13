import json

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
    

@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def get_reports(request):
    if request.method == 'GET':
        reports = StoryReport.objects.all()

        status = request.GET.get('status')

        if status:
            reports = reports.filter(status=status)
        
        # Sort reports
        
        reports = reports.order_by('-updated_at')
        template = loader.get_template('parts/reports_table.html').render(
            context={'reports': reports}
        )

        return HttpResponse(template)


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def open_report(request, report_id):
    if request.method == 'GET':
        report = StoryReport.objects.get(pk=report_id)
        if report.status == 'unread':
            report.status = 'read'
            report.save()

        template = loader.get_template('parts/report_content.html').render(context={'report':report})
        return HttpResponse(template)


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def delete_reports(request):
    """ Delete many reports by their id
    :param: 'delete' - list of ids from reports to delete
    :return: A json response
    """
    if request.method == 'DELETE':
        to_delete = json.loads(request.body)
        to_delete = to_delete.get('delete')
        
        for d in to_delete:
            try:
                StoryReport.objects.get(pk=int(d)).delete()
            except:
                pass
        response = {
            'success': True,
            'message': 'Reports deleted correctly.',
            'message_t': 'Reportes eliminados correctamente.'
        }
        return JsonResponse(response)
    

@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def modify_reports_status(request):
    """ Change the report status
    :query param: status
    :body: 'reports_ids' - list of ids of reports to modify
    :return: A json response
    """

    if request.method == 'PUT':
        q_status = request.GET.get('status')
        if not q_status:
            return JsonResponse(
                {'success': False, 'message': 'Query param for \'status\' is required.', 'message_t': 'Se necesita el parámetro \'status\'.'}
            )
        q_status = q_status.lower()
        if not q_status in ['unread', 'read', 'in_progress', 'fixed']:
            return JsonResponse(
                {'success': False, 'message': 'Status not valid.', 'message_t': 'Estado no válido.'}
            )
        reports_ids = json.loads(request.body)
        reports_ids = reports_ids.get('reports_ids')

        for ri in reports_ids:
            try:
                r = StoryReport.objects.get(pk=int(ri))
                r.status = q_status
                r.save()
            except:
                pass
        response = {
            'success': True,
            'message': 'Reports status changed correctly.',
            'message_t': 'Estado de los reportes cambiados correctamente.'
        }
        return JsonResponse(response)

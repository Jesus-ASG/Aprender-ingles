from main.models import StoryReport

def get_reports_unread_number(request):
	if request.user.is_staff or request.user.is_superuser:
		return {'reports_unread_number': StoryReport.objects.filter(status='unread').count()}
	else:
		return {'reports_unread_number': 0}
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from main.models import UserProfile, StoryReport
from main.serializers import StoryReportSerializer

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user = instance)


@receiver(post_save, sender=StoryReport)
def send_notification_on_report_create(sender, instance, created, **kwargs):
	if created:
		json_report = StoryReportSerializer(instance)
		json_report = JSONRenderer().render(json_report.data).decode('utf-8')

		channel_layer = get_channel_layer()
		group_name = 'report-notifications'
		event = {
			'type': 'report_created',
			'content': json_report
		}

		async_to_sync(channel_layer.group_send)(group_name, event)

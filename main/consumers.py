import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ReportNotificationsConsumer(WebsocketConsumer):
	def connect(self):
		self.notifications_group_name = 'report-notifications'
		# Join room group
		async_to_sync(self.channel_layer.group_add)(
			self.notifications_group_name, self.channel_name
		)
		self.accept()


	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.notifications_group_name, self.channel_name
		)
	
	def report_created(self, event):
		username = self.scope["user"]

		if username.is_staff or username.is_superuser:
			self.send(text_data=event['content'])

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     self.send(text_data=json.dumps({"message": message}))
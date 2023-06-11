from rest_framework import serializers
from .models import User, MultipleChoiceQuestion, QuestionChoice

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
        )
        

class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = '__all__'

    


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True)
    class Meta:
        model = MultipleChoiceQuestion
        fields = '__all__'


    def get_choices(self, instance):
        sorted_choices = instance.choices.order_by('choice_number')  # Sort choices
        serializer = QuestionChoiceSerializer(sorted_choices, many=True)
        return serializer.data

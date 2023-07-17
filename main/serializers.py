from rest_framework import serializers
import main.models as model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.User
        fields = (
            'id',
            'username',
            'password',
        )

# --------------- Content Serializers --------------------- #
class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Audio
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Video
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Image
        fields = '__all__'

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Text
        fields = '__all__'

class DialogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Dialogue
        fields = '__all__'
# ---------------------------------------------------------- #


# --------------- Exercises Serializers --------------------- #
class RepeatPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.RepeatPhrase
        fields = '__all__'

class SpellCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Spellcheck
        fields = '__all__'

class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.QuestionChoice
        fields = '__all__'
    
class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True)
    class Meta:
        model = model.MultipleChoiceQuestion
        fields = '__all__'
    def get_choices(self, instance):
        sorted_choices = instance.choices.order_by('choice_number')  # Sort choices
        serializer = QuestionChoiceSerializer(sorted_choices, many=True)
        return serializer.data



class PageSerializer(serializers.ModelSerializer):
    # Content
    audios = AudioSerializer(many=True)
    videos = VideoSerializer(many=True)
    images = ImageSerializer(many=True)
    texts = TextSerializer(many=True)
    dialogues = DialogueSerializer(many=True)
    # Exercises
    spellchecks = SpellCheckSerializer(many=True)
    questions = MultipleChoiceQuestionSerializer(many=True)
    repeat_phrases = RepeatPhraseSerializer(many=True)
    class Meta:
        model = model.Page
        fields = '__all__'



# Report
class StoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.StoryReport
        fields = '__all__'


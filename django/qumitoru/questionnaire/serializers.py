from rest_framework import serializers

from .models import QuestionareScore

class QuestionareScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionareScore
        fields = '__all__'

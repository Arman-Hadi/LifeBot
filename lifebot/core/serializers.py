from rest_framework import serializers

from .models import QuestionType, Question, Answer, TelUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelUser
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(write_only=True, default="")
    type_id = serializers.IntegerField(write_only=True, default="")

    class Meta:
        model = Question
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        if 'type_name' in validated_data:
            qtype = QuestionType.objects.get(
                name=validated_data['type_name'])
            q = Question(qtype=qtype,
                message_id=validated_data['message_id'])
            q.save()
            return q
        elif 'type_id' in validated_data:
            qtype = QuestionType.objects.get(
                pk=validated_data['type_id'])
            q = Question(qtype=qtype,
                message_id=validated_data['message_id'])
            q.save()
            return q
    
    def validate(self, data):
        if data['type_name'] == "":
            data.pop('type_name')
        if data['type_id'] == "":
            data.pop('type_id')
        if not 'type_name' in data and not 'type_id' in data:
            raise serializers.ValidationError(
            {'error': "You must send either 'type_name' or "
                "'type_id' to distinguish Question Type."})
        return data


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    message_id = serializers.IntegerField(write_only=True)
    chat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        depth = 2
    
    def create(self, validated_data):
        user = TelUser.objects.get(chat_id=validated_data['chat_id'])
        question = Question.objects.get(
            message_id=validated_data['message_id'])
        answer = Answer(
            answer=validated_data['answer'],
            user=user,
            question=question)
        answer.save()
        return answer

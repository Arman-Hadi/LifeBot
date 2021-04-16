from django.db import IntegrityError
from django.contrib.auth import authenticate

from rest_framework.exceptions import status
from rest_framework import serializers

from .models import AnswerManager, QuestionType, Question, Answer, TelUser, DetailedQuestion


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
        try:
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
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'already exists'}, status.HTTP_409_CONFLICT)
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
        try:
            answer = Answer(
                answer=validated_data['answer'],
                user=user,
                question=question)
            answer.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'already exists'}, status.HTTP_409_CONFLICT)
        return answer


class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for the user authentication object'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class DetailedQuestionSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(write_only=True)
    qtype = serializers.CharField(write_only=True)

    class Meta:
        model = DetailedQuestion
        fields = '__all__'
        depth = 1

    def create(self, data):
        user = TelUser.objects.get(chat_id=data['chat_id'])
        question = QuestionType.objects.get(
            name=data['qtype'])

        data.pop('qtype')
        data.pop('chat_id')
        params = {
            'user': user,
            'question': question,
            **data
        }

        try:
            q = DetailedQuestion(
                **params)
            q.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'already exists'}, status.HTTP_409_CONFLICT)

        return q

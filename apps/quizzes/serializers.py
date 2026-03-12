import uuid
from rest_framework import serializers
from .models import Quiz, Question, QuizSubmission


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'question_text',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer',
        ]
        read_only_fields = ['id']


class QuestionDisplaySerializer(serializers.ModelSerializer):
    """Serializer that hides the correct answer (for students)."""
    class Meta:
        model = Question
        fields = [
            'id', 'question_text',
            'option_a', 'option_b', 'option_c', 'option_d',
        ]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'title', 'total_questions', 'created_at', 'questions']
        read_only_fields = ['id', 'created_at', 'total_questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        quiz = Quiz.objects.create(**validated_data)
        for q_data in questions_data:
            Question.objects.create(quiz=quiz, **q_data)
        quiz.total_questions = len(questions_data)
        quiz.save(update_fields=['total_questions'])
        return quiz


class QuizDisplaySerializer(serializers.ModelSerializer):
    """Quiz serializer for students — hides correct answers."""
    questions = QuestionDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'title', 'total_questions', 'created_at', 'questions']


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.DictField(
        child=serializers.CharField(),
        help_text='Map of question_id -> selected answer (a/b/c/d)',
    )
    submission_uid = serializers.CharField(
        required=False,
        help_text='Unique ID for offline deduplication',
    )

    def validate_submission_uid(self, value):
        if value and QuizSubmission.objects.filter(submission_uid=value).exists():
            raise serializers.ValidationError(
                'This submission has already been recorded.'
            )
        return value


class QuizResultSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = QuizSubmission
        fields = [
            'id', 'quiz', 'quiz_title', 'score', 'total',
            'percentage', 'submitted_at',
        ]

    def get_percentage(self, obj):
        if obj.total == 0:
            return 0
        return round((obj.score / obj.total) * 100, 1)

import uuid
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.accounts.permissions import IsFacilitator
from .models import Quiz, Question, QuizSubmission
from .serializers import (
    QuizSerializer,
    QuizDisplaySerializer,
    QuizSubmitSerializer,
    QuizResultSerializer,
)


class CreateQuizView(generics.CreateAPIView):
    """POST /lessons/{lesson_id}/quiz — Create a quiz for a lesson."""
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsFacilitator]

    def perform_create(self, serializer):
        serializer.save(lesson_id=self.kwargs['lesson_id'])


class RetrieveQuizView(generics.ListAPIView):
    """GET /lessons/{lesson_id}/quiz — Retrieve quizzes for a lesson."""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.role in ('facilitator', 'admin', 'system_admin'):
            return QuizSerializer
        return QuizDisplaySerializer

    def get_queryset(self):
        return Quiz.objects.filter(
            lesson_id=self.kwargs['lesson_id']
        ).prefetch_related('questions')


class SubmitQuizView(generics.GenericAPIView):
    """POST /quiz/{quiz_id}/submit — Submit quiz answers."""
    serializer_class = QuizSubmitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.prefetch_related('questions').get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response(
                {'detail': 'Quiz not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data['answers']
        submission_uid = serializer.validated_data.get(
            'submission_uid', str(uuid.uuid4())
        )

        # Grade the quiz
        score = 0
        total = quiz.questions.count()
        for question in quiz.questions.all():
            given_answer = answers.get(str(question.id), '').lower()
            if given_answer == question.correct_answer.lower():
                score += 1

        submission = QuizSubmission.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total,
            answers=answers,
            submission_uid=submission_uid,
        )

        return Response(
            QuizResultSerializer(submission).data,
            status=status.HTTP_201_CREATED,
        )


class QuizResultView(generics.RetrieveAPIView):
    """GET /quiz/{quiz_id}/result — Retrieve latest quiz result for current user."""
    serializer_class = QuizResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return QuizSubmission.objects.filter(
            quiz_id=self.kwargs['quiz_id'],
            user=self.request.user,
        ).latest('submitted_at')

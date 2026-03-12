import uuid
from django.conf import settings
from django.db import models


class Quiz(models.Model):
    """Quiz attached to a lesson."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(
        'courses.Lesson', on_delete=models.CASCADE, related_name='quizzes'
    )
    title = models.CharField(max_length=255)
    total_questions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'quizzes'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    """Multiple-choice question within a quiz."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions'
    )
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
    )

    def __str__(self):
        return self.question_text[:80]


class QuizSubmission(models.Model):
    """Student's quiz submission with score."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_submissions',
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='submissions'
    )
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    answers = models.JSONField(
        default=dict, help_text='Map of question_id -> selected answer'
    )
    submission_uid = models.CharField(
        max_length=100, unique=True,
        help_text='Unique ID for offline deduplication',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user} — {self.quiz.title}: {self.score}/{self.total}"

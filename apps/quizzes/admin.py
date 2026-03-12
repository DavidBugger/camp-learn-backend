from django.contrib import admin
from .models import Quiz, Question, QuizSubmission


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'total_questions', 'created_at']
    list_filter = ['lesson__course']
    inlines = [QuestionInline]


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total', 'submitted_at']
    list_filter = ['quiz', 'submitted_at']
    readonly_fields = ['submission_uid', 'answers']

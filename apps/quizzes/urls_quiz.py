from django.urls import path
from .views import SubmitQuizView, QuizResultView

urlpatterns = [
    path('<uuid:quiz_id>/submit/', SubmitQuizView.as_view(), name='quiz-submit'),
    path('<uuid:quiz_id>/result/', QuizResultView.as_view(), name='quiz-result'),
]

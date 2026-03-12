from django.urls import path
from .views import CreateQuizView, RetrieveQuizView

urlpatterns = [
    path('lessons/<uuid:lesson_id>/quiz/', CreateQuizView.as_view(), name='quiz-create'),
    path('lessons/<uuid:lesson_id>/quiz/list/', RetrieveQuizView.as_view(), name='quiz-retrieve'),
]

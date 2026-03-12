from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.camps.models import Camp
from apps.courses.models import Course, Lesson
from apps.quizzes.models import Quiz, Question

User = get_user_model()


class CampLearnIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com', username='admin', password='admin_password', role='admin'
        )
        self.admin_client = APIClient()
        refresh = self._get_token('admin@test.com', 'admin_password')
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
        
    def _get_token(self, email, password):
        resp = self.client.post(reverse('auth-login'), {
            'email': email, 'password': password
        })
        return resp.data['access']

    def test_core_user_journey(self):
        # 1. Admin creates a camp
        camp_resp = self.admin_client.post(reverse('camp-list-create'), {
            'name': 'Borno IDP Camp A',
            'location': 'Maiduguri',
        })
        self.assertEqual(camp_resp.status_code, status.HTTP_201_CREATED)
        camp_id = camp_resp.data['id']

        # 2. Student registers and logs in
        reg_resp = self.client.post(reverse('auth-register'), {
            'email': 'student@test.com',
            'username': 'student123',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!',
            'name': 'Test Student',
            'camp': camp_id,
        })
        self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED, reg_resp.data)
        
        student_client = APIClient()
        student_client.credentials(HTTP_AUTHORIZATION=f"Bearer {reg_resp.data['tokens']['access']}")

        # 3. Admin creates a facilitator
        fac_resp = self.admin_client.post(reverse('admin-create-facilitator'), {
            'email': 'teacher@test.com',
            'username': 'teacher123',
            'password': 'StrongPassword123!',
            'name': 'Test Teacher',
            'camp': camp_id,
        })
        self.assertEqual(fac_resp.status_code, status.HTTP_201_CREATED, fac_resp.data)
        
        teacher_client = APIClient()
        teacher_token = self._get_token('teacher@test.com', 'StrongPassword123!')
        teacher_client.credentials(HTTP_AUTHORIZATION=f"Bearer {teacher_token}")

        # 4. Teacher creates course and lesson
        course_resp = teacher_client.post(reverse('course-list-create'), {
            'title': 'Basic English',
            'category': 'Language',
        })
        self.assertEqual(course_resp.status_code, status.HTTP_201_CREATED, course_resp.data)
        course_id = course_resp.data['id']

        lesson_resp = teacher_client.post(
            reverse('lesson-list-create', kwargs={'course_id': course_id}),
            {
                'course': course_id,
                'title': 'Alphabet',
                'duration': 15,
                'content_type': 'text',
                'content_text': 'A B C D',
            }
        )
        self.assertEqual(lesson_resp.status_code, status.HTTP_201_CREATED, lesson_resp.data)
        lesson_id = lesson_resp.data['id']

        # 5. Teacher creates quiz
        quiz_resp = teacher_client.post(
            reverse('quiz-create', kwargs={'lesson_id': lesson_id}),
            {
                'lesson': lesson_id,
                'title': 'Alphabet Quiz',
                'questions': [
                    {
                        'question_text': 'What comes after A?',
                        'option_a': 'Z',
                        'option_b': 'B',
                        'option_c': 'C',
                        'option_d': 'D',
                        'correct_answer': 'b',
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(quiz_resp.status_code, status.HTTP_201_CREATED, quiz_resp.data)
        quiz_id = quiz_resp.data['id']

        # 6. Student views courses
        courses_resp = student_client.get(reverse('course-list-create'))
        self.assertEqual(courses_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(courses_resp.data['results']), 1)

        # 7. Student submits quiz (answers correctly)
        submit_resp = student_client.post(
            reverse('quiz-submit', kwargs={'quiz_id': quiz_id}),
            {'answers': {str(quiz_resp.data['questions'][0]['id']): 'b'}},
            format='json'
        )
        self.assertEqual(submit_resp.status_code, status.HTTP_201_CREATED, submit_resp.data)
        self.assertEqual(submit_resp.data['score'], 1)  # 1/1 correct

        # 8. Student marks lesson complete
        prog_resp = student_client.post(reverse('progress-mark-complete'), {
            'lesson_id': lesson_id
        })
        self.assertEqual(prog_resp.status_code, status.HTTP_200_OK)

        # 9. Verify Gamification (Points awarded for quiz + lesson)
        points_resp = student_client.get(reverse('gamification-points'))
        # 10 points for lesson, 25 points for perfect quiz = 35 points total
        self.assertEqual(points_resp.data['total_points'], 35)

        # 10. Admin checks analytics
        analytics_resp = self.admin_client.get(reverse('analytics-platform'))
        self.assertEqual(analytics_resp.data['total_learners'], 1)
        self.assertEqual(analytics_resp.data['total_courses'], 1)

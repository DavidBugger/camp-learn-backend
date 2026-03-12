from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

from apps.progress.models import LessonProgress
from apps.quizzes.models import QuizSubmission
from .models import PointTransaction, Badge, UserBadge


@receiver(post_save, sender=LessonProgress)
def award_lesson_points(sender, instance, **kwargs):
    """Award points when a lesson is completed."""
    if not instance.completed:
        return

    # Avoid double-awarding: check if points already given for this lesson
    exists = PointTransaction.objects.filter(
        user=instance.user,
        reason='lesson_complete',
        description__contains=str(instance.lesson_id),
    ).exists()
    if exists:
        return

    PointTransaction.objects.create(
        user=instance.user,
        points=10,
        reason='lesson_complete',
        description=f'Completed lesson: {instance.lesson.title} ({instance.lesson_id})',
    )

    _check_badge_awards(instance.user)


@receiver(post_save, sender=QuizSubmission)
def award_quiz_points(sender, instance, created, **kwargs):
    """Award points for quiz submissions."""
    if not created:
        return

    if instance.total > 0:
        percentage = (instance.score / instance.total) * 100

        if percentage == 100:
            PointTransaction.objects.create(
                user=instance.user,
                points=25,
                reason='quiz_perfect',
                description=f'Perfect score on: {instance.quiz.title}',
            )
        elif percentage >= 50:
            PointTransaction.objects.create(
                user=instance.user,
                points=15,
                reason='quiz_pass',
                description=f'Passed quiz: {instance.quiz.title}',
            )

    _check_badge_awards(instance.user)


def _check_badge_awards(user):
    """Check if user qualifies for any new badges."""
    total_points = (
        PointTransaction.objects.filter(user=user)
        .aggregate(total=Sum('points'))['total']
    ) or 0

    total_lessons = LessonProgress.objects.filter(
        user=user, completed=True
    ).count()

    earned_badge_ids = set(
        UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    )

    for badge in Badge.objects.all():
        if badge.id in earned_badge_ids:
            continue
        if (
            (badge.points_required > 0 and total_points >= badge.points_required)
            or (badge.lessons_required > 0 and total_lessons >= badge.lessons_required)
        ):
            UserBadge.objects.create(user=user, badge=badge)

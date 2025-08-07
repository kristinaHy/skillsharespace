# skillsharespace_app/signals.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Question, Answer, Flag

@receiver(post_delete, sender=Question)
def delete_flags_for_question(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Question)
    # Delete flags on the question itself
    Flag.objects.filter(content_type=content_type, object_id=instance.id).delete()

    # Also delete flags on answers of this question
    answer_ct = ContentType.objects.get_for_model(Answer)
    answer_ids = instance.answers.values_list('id', flat=True)
    Flag.objects.filter(content_type=answer_ct, object_id__in=answer_ids).delete()

@receiver(post_delete, sender=Answer)
def delete_flags_for_answer(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Answer)
    Flag.objects.filter(content_type=content_type, object_id=instance.id).delete()

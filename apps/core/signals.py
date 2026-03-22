from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def bootstrap_master_user(sender, **kwargs):
    if sender.name != "apps.core":
        return

    User = get_user_model()
    defaults = {
        "email": "danielguspedev@local.dev",
        "is_staff": True,
        "is_superuser": True,
        "role": "master",
        "full_name": "Daniel Guspe Dev",
    }
    user, created = User.objects.get_or_create(username="danielguspedev", defaults=defaults)
    dirty = created
    for field, value in defaults.items():
        if getattr(user, field) != value:
            setattr(user, field, value)
            dirty = True
    if created or not user.check_password("Dnov@0380"):
        user.set_password("Dnov@0380")
        dirty = True
    if dirty:
        user.save()

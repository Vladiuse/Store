from django.db import models
from store.models import Basket
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    phone = models.CharField(
        max_length=13,
    )
    email = models.EmailField(
        blank=True,
    )
    status = models.SmallIntegerField(
        choices=STATUSES,
        default=CREATED,
    )
    basket_history = models.JSONField()

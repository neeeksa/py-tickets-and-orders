import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order
from django.contrib.auth import get_user_model


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    if not date:
        date = datetime.datetime.now()

    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)

        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=order
            )

        return order


def get_orders(username: str = None) -> QuerySet[Order] | Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()

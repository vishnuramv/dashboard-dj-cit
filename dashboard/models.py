from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bidding(models.Model):
    total_qty = models.IntegerField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class BiddingRow(models.Model):
    slot = models.CharField(max_length=100)
    from_time = models.TimeField()
    to_time = models.TimeField()
    time_block = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.IntegerField()
    bidding = models.ForeignKey(Bidding, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.slot} {self.time_block}"

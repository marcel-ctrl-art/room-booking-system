from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    has_projector = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    date = models.DateField()
    comment = models.CharField(max_length=170)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['date', 'room']]
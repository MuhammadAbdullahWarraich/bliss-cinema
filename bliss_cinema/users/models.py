from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    original_title = models.CharField(max_length=500)
    released = models.DateField()
    poster = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.original_title} ({self.released})"

class TopMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='top_movies')

    def __str__(self):
        return f"Top: {self.movie}"

class NowPlaying(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='now_playing_movies')

    def __str__(self):
        return f"Now Playing: {self.movie}"

class Hall(models.Model):
    id = models.AutoField(primary_key=True)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Hall {self.id}"

class Showtime(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtime')
    show_date = models.DateField()
    show_time = models.TimeField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='showtimes')
    available_tickets = models.IntegerField()
    def __str__(self):
        return f"{self.movie} - {self.show_date} {self.show_time} - Hall {self.hall.id}"

    def save(self, *args, **kwargs):
        # Automatically set the number of tickets to the available seats in the hall
        self.available_tickets = self.hall.available_seats
        super(Showtime, self).save(*args, **kwargs)

@receiver(pre_save, sender=Showtime)
def update_tickets_field(sender, instance, **kwargs):
    instance.available_tickets = instance.hall.available_seats

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='showtime')
    num_tickets = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} booked {self.num_tickets} tickets for {self.showtime.movie}"

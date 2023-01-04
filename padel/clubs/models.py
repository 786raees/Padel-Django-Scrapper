from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class PadelClub(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    price_30_min = models.IntegerField(null=True, blank=True)
    price_60_min = models.IntegerField(null=True, blank=True)
    price_90_min = models.IntegerField(null=True, blank=True)
    price_unit = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Record(models.Model):
    padel_club = models.ForeignKey(PadelClub, on_delete=models.CASCADE)
    no_of_courts = models.IntegerField()
    booked_hours = models.DecimalField(max_digits=5, decimal_places=2)
    available_hours = models.DecimalField(max_digits=5, decimal_places=2)
    utiliation_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.utiliation_rate:
            total_hours = self.available_hours
            self.utiliation_rate = self.booked_hours / total_hours * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        date = self.created_at.strftime('%Y-%m-%d %H:%M')
        return f"{date}"


# class Slot(models.Model):
#     club =              models.ForeignKey(PadelClub, on_delete=models.CASCADE)
#     title =             models.CharField(max_length=100)
#     date =              models.DateField(_("Date"), auto_now_add=False, auto_now=False, default=now)
#     start_time =        models.CharField(_("Start Time"), max_length=10, null=True, blank=True)
#     end_time =          models.CharField(_("End Time"), max_length=10, null=True, blank=True)
#     price =             models.CharField(_("Price"), max_length=100, null=True, blank=True)
#     currency =          models.CharField(_("Currency"), max_length=100, null=True, blank=True)
#     is_booked =         models.BooleanField(_("Is Booked"), default=False)
#     is_not_available =  models.BooleanField(_("Is Not Available"), default=False)
#     created_at =        models.DateTimeField(auto_now_add=True)
#     updated_at =        models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return self.title

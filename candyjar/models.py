# importing from django
from django.db import models


# Database representation of how a measurement by the candyjar should be stored
class Measurement(models.Model):
    raw_measurement = models.DecimalField(max_digits=7, decimal_places=3)   # data point containing the raw sensor data
    weight = models.DecimalField(max_digits=4, decimal_places=2)            # data point containing the weight measured
    timestamp = models.DateTimeField('Date measured')                       # time when data point is entered

    # overwriting the __str__() function of the object to display the relevant description
    def __str__(self):
        return self.timestamp.__str__() + ': ' + self.weight.__str__()


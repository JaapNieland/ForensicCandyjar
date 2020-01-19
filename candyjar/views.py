# importing core libraries
import csv
from datetime import timedelta

# import django libraries
from django.views import generic
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import reverse

# import from elsewhere in the app
from .models import Measurement

# starting with the views (defining the responses to web requests)
class Index(generic.DetailView):
    # Main view when entering the site
    model = Measurement                         # The name of the model that is used
    template_name = 'candyjar/index.html'       # File in /templates that is rendered
    context_object_name = 'last_measurement'    # Variable name that can be used in the template

    # Retrieve the last measurement
    def get_object(self):
        last_measurement = Measurement.objects.all().order_by('-timestamp')[0]  # the latest measurement
        return last_measurement


class LastWeek(generic.ListView):
    # View to inspect the measurements from last week
    template_name = 'candyjar/lastWeek.html'    # File in /templates that is rendered
    context_object_name = 'last_measurements'   # Variable name that can be used in the template

    # Retrieve the measurements collected last week
    def get_queryset(self):
        cutoff_date = timezone.now() - timedelta(weeks=1)       # calculating the date 1 week ago
        last_week_measurements = Measurement.objects.filter(    # retrieving the measurements
            timestamp__gte=cutoff_date                          # filter condition
        )
        return last_week_measurements


def lastWeek_csv(request):
    # View to deliver a csv with all measurements from the past week
    response = HttpResponse(content_type='text/csv')            # specify the response content type (csv)
    response['Content-Disposition'] = 'attachment; filename="lastWeek.csv"' # meta data on the response/csv

    cutoff_date = timezone.now() - timedelta(weeks=1)         # calculating the date 1 week ago
    last_week_measurements = Measurement.objects.filter(      # retrieving the measurements
        timestamp__gte=cutoff_date                            # filter condition
    )

    # csv creation
    writer = csv.writer(response, delimiter=';')                # start the csv writer
    writer.writerow(['timestamp', 'raw_measurement', 'weight']) # write the header

    # itterate through the queryset (measurement from last week)
    for m in last_week_measurements:
        writer.writerow([m.timestamp, m.raw_measurement, m.weight])  # write row with data to csv

    # deliver back
    return response


def collect(request):
    # View to send data to from the candy jar
    try:
        # Extract relevant data points
        raw_measurement = request.POST['raw_measurement']
        weight = request.POST['weight']
    except MultiValueDictKeyError:
        # When required data points could not be found in the request, raise error
        return HttpResponseBadRequest('Need two fields: raw_measurement and weight')
    else:
        # When no error was raised, store data to the database
        time = timezone.now() # additional data point for database determined server side
        m = Measurement(raw_measurement=raw_measurement,    # making the object to store to database
                        weight=weight,
                        timestamp=time)

        m.save()  # committing to database
        return HttpResponseRedirect(reverse('candyjar:index'))  # return to index page





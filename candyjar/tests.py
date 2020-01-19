from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Measurement

# Create your tests here.
class MeasurementCollectViewTests(TestCase):

    def test_posted_data_got_in_database(self):
        """
        Test to check that posted data gets into the database
        """
        # Carry out a post request as if storing data
        c = Client()
        url = reverse('candyjar:collect')
        c.post(url, {'raw_measurement': 10.1, 'weight': 1.11})

        measurements = Measurement.objects.all()
        self.assertEqual(measurements.__len__(), 1)


    def test_posting_no_data_returns_error(self):
        """
        Test to check for error return when no data is posted
        """
        c = Client()
        url = reverse('candyjar:collect')
        c.post(url)

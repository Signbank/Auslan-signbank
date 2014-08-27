from django.conf import settings
from django.test import Client, TestCase
import os, shutil

class PageTests(TestCase):

    def setUp(self):
        
        pass
    
    def test_404_email(self):
        """
        Can customize the 404 page feedback email address
        """
        
        self.assertEqual(settings.ADMIN_EMAIL, "webmaster@auslan.org.au")
        
        response = self.client.get('/xxx/')
        
        self.assertContains(response, "webmaster@auslan.org.au", 2, 404)
        
        with self.settings(ADMIN_EMAIL='test@example.com'):
            response = self.client.get('/xxx/')
            
            self.assertContains(response, "test@example.com", 2, 404)
            self.assertNotContains(response, "webmaster@auslan.org.au", 404)
            
    def test_google_analytics(self):
        """
        Can add Google Analytics javascript by including a code in settings
        """
        
        self.assertEqual(settings.GOOGLE_ANALYTICS_TRACKING_CODE, None)
        
        response = self.client.get('/')
        self.assertNotContains(response, "google-analytics.com")
        
        with self.settings(GOOGLE_ANALYTICS_TRACKING_CODE='UA-TEST-1'):
            response = self.client.get('/')

            self.assertContains(response, "google-analytics.com")
            self.assertContains(response, "UA-TEST-1")
        
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
        
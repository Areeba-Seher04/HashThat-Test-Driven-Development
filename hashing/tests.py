
from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
from django.core.exceptions import ValidationError

# class FunctionalTestCase(TestCase):
#     def setUp(self):  #runs everytime before any test run (runs everytime when any function call)
#         self.browser = webdriver.Firefox()  #open the browser

#     def test_there_is_homepage(self):
#         self.browser.get('http://127.0.0.1:8000')
#         self.assertIn('Enter Hash here:',self.browser.page_source)

#     # def test_hash_of_hello(self):
#     #     self.browser.get('http://127.0.0.1:8000')
#     #     text = self.browser.find_element_by_id('id_text')  #search for textarea(form) where user can enter text,find element in HTML having some ID
#     #     text.send_keys('hello')  #simulate the user typing in textbox
#     #     self.browser.find_element_by_name('submit').click() #submit the form that contain the user typed data & simulate the click by calling the click function
#     #     self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',self.browser.page_source)
        
#     def tearDown(self): #run after all tests
#         self.browser.quit() #close the browser

class UnitTestCase(TestCase):
    '''testing the template at given url is present or not'''
    def test_home_homepage_template(self):
        response = self.client.get('/') #visit the given url and shows all data of that page(check copy)
        self.assertTemplateUsed(response,'hashing/home.html') #checking the template of the given response(url)

    '''testing form is valid or not by populating it with some data'''
    def test_hash_form(self):
        form = HashForm(data={'text':'hello'}) #check form is present/not and populate it with data hello(textfield) {'field':'value'}
        self.assertTrue(form.is_valid()) 

    '''testing the hash function or simply testing a library'''
    def test_hash_func_works(self):
        test_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',test_hash)

    def save_hash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash.save()
        return hash


    '''testing object created in model, 1st create object save it in database then pulled it from database and check 
    the data is saving correctly in database or not, use a test database for this purpose ,check database
    portion in settings.py'''
    def test_hash_object(self):
        hash = self.save_hash()
        pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(hash.text,pulled_hash.text)

    def test_viewing_hash(self):
        hash = self.save_hash()
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response,'hello')

    '''testing is error occured when we are passing wrong data'''
    def test_bad_data(self):
        def BadHash():
            hash = Hash()
            hash.hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824aaaaaaa'
            hash.full_clean()
        self.assertRaises(ValidationError,BadHash)
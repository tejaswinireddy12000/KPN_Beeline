from rest_framework.test import  APITestCase
from django.urls import reverse
from first_app.models import Beeline,Profile
from first_app.serializers import BeelineSerializer,ProfileSerializer
import json
from django.core.files.base import ContentFile
from first_app.tests import fixtures
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from django.core.files import File
import os
from decouple import config
from django.conf import settings
from django.contrib.auth.models import User


file = BytesIO(b"file content")
file.name = "test.txt"
file.content_type = "text/plain"
class TestRegisterViews(APITestCase):
    register_url = reverse('Register')
    login_url = reverse('login')
    password_url = reverse('password')
    user_data_reg={
        'username':"email",
        'email':"email@email.com",
        "first_name":"Teju",
        "last_name":"Reddy",
        'password':config('TEST_CASES_PASSWORD'),
        'password2':config('TEST_CASES_PASSWORD')
    }
    login_data={
        "username":"email",
        "password":config('TEST_CASES_PASSWORD')
    }
    password_data = {
        "username":"email",
        "password1":config('TEST_CASES_PASSWORD'),
        "password2":config('TEST_CASES_PASSWORD')
    }
    password_data_not_match = {
        "username":"email",
        "password1":config('TEST_CASES_PASSWORD'),
        "password2":config('TEST_CASES_PASS_NOT_MATCH')
    }
    username_wrong = {
        "username":"email1",
        "password1":config('TEST_CASES_PASSWORD'),
        "password2":config('TEST_CASES_PASSWORD')
    }

    def test_user_can_register(self):
        res = self.client.post(self.register_url,self.user_data_reg,format="json")
        self.assertEqual(res.status_code,200)

    def test_user_cannot_register(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code,400)

    def test_user_can_login(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.login_url,self.login_data,format="json")
        self.assertEqual(res.status_code,201)

    def test_user_cannot_login(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.login_url)
        self.assertEqual(res.status_code,400)

    def test_login_without_username(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.login_url,data={"password":"email@email.com"})
        self.assertEqual(res.status_code,400)

    def test_login_without_password(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.login_url,data={"username":"email"})
        self.assertEqual(res.status_code,400)
    
    def test_user_password_reset_succes(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.password_url,self.password_data,format="json")
        self.assertEqual(res.status_code,200)
    def test_password_not_match_reset(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.password_url,self.password_data_not_match,format="json")
        self.assertEqual(res.status_code,400)
    def test_username_not_exists(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.password_url,self.username_wrong,format="json")
        self.assertEqual(res.status_code,400)




class TestBeelineViews(APITestCase):
    """this is Test case for LostCountView"""
    url = 'http://localhost:8000/Beeline/'
    url1 = 'http://localhost:8000/Beeline/1'
    
    user_data={
        
        "beeLine_Request_Number": "21000-3",
        "job_description": "IT Support",
        "department": "IT",
        "no_of_positions": 9,
        "priority": "Medium",
        "status": "Open",
        "cv_DeadLine": "2023-03-09",
        "billing_Rate": "$60-$90",
        "hours_per_week": 90,
        "contact_person": "Suraj malavika",
        "date_request": "2023-02-25",
        "prodapt_practice":"SF Practice",
        "prodapt_POC":"Malavika",
        "dutch_Language":"No",
        "location":"Panama",
        "key_skills":"Django,Python"
        
        
    }

    def setUp(self):
        Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",file="",status="Fulfilled")
        Beeline.objects.create(beeLine_Request_Number="2100-2",job_description="Project Manager",department="QA",no_of_positions=4,priority="Medium",cv_DeadLine="2023-03-01",billing_Rate="90$-120$",hours_per_week=90,contact_person="William",date_request="2023-05-24",file="",status="Lost")

        

    def test_lost_count_success(self):
        
        #print(self.lost_count_url)
        res  =self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_post_view_call(self):
        res = self.client.post(self.url,self.user_data,format="json")
        self.assertEqual(res.status_code, 201)

    def test_post_with_no_data(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, 400)

    def test_delete(self):
        
        res = self.client.delete(self.url1)
        self.assertEqual(res.status_code, 404)




class TestBeelineUploadView(APITestCase):
    #This is the test case for BeelineUploadView

    url = 'http://localhost:8000/addbeeline/'
    mail_beeline_url = 'http://localhost:8000/mail_new_beeline/'
    pdf_file = BytesIO()
    pdf_file.write(b"My PDF file contents goes here.")
    content_file = ContentFile(pdf_file.getvalue(),'example.pdf')

    
    user_data={
        "User":json.dumps({"beeLine_Request_Number": "21000-3",
        "job_description": "IT Support",
        "department": "IT",
        "no_of_positions": 9,
        "priority": "Medium",
        "status": "Open",
        "cv_DeadLine": "2023-03-09",
        "billing_Rate": "$60-$90",
        "hours_per_week": 90,
        "contact_person": "Suraj malavika",
        "date_request": "2023-02-25",
        "prodapt_practice":"SF Practice",
        "prodapt_POC":"Malavika",
        "dutch_Language":"No",
        "location":"Panama",
        "key_skills":"Django,Python"}),

        "file":"undefined"
        
    }

    
    
    
    


    def setUp(self):
        
        obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",file="",status="Fulfilled")
        obj2  =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=obj1)

    

    def test_post_view_call(self):
        
        res = self.client.post(self.url,self.user_data,format='json')
        self.assertEqual(res.status_code, 201)
    def test_post_view_call_file(self):
        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            'beeLine_Request_Number': '123',
                'job_description': 'Test job',
                'department': 'Test department',
                'no_of_positions': 1,
                'priority': 'High',
                'status': 'Open',
                'cv_DeadLine': '2022-03-01',
                'billing_Rate': 100,
                'hours_per_week': 40,
                'contact_person': 'Test person',
                'date_request': '2022-02-22',
                "prodapt_practice":"SF Practice",
                "prodapt_POC":"Malavika",
                "dutch_Language":"No",
                "location":"Panama",
                "key_skills":"Django,Python"
        }
        
        

        res = self.client.post(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 201)


    
class TestProfileUploadView(APITestCase):
    #This is the test case for BeelineUploadView
    url = 'http://localhost:8000/addprofile/'
    
    


    def setUp(self):
        
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
        self.obj2  =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.obj1)

    

    def test_post_view_call(self):
        
        profile_data={"User":json.dumps({
            "current_Status":"Open",
            "name_of_candidate":"Tejaswini",
            
            "next_step":"NA",
            
            "location_relocation":"India",
            
            "client_Interview":"YES",
            "comments":"NA",
            "beeline":self.obj1.id
            }),
            "file":"undefined"

            }

        res = self.client.post(self.url,profile_data,format='json')
        self.assertEqual(res.status_code, 201)

        res  =self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
    def test_post_view_call_file(self):
        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            "current_Status":"Open",
            "name_of_candidate":"Tejaswini",
            
            "next_step":"NA",
            
            "location_relocation":"India",
            
            "client_Interview":"YES",
            "comments":"NA",
            "beeline":self.obj1.id
        }
        
        

        res = self.client.post(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 201)


class TestOverallCount(APITestCase):
    url = 'http://localhost:8000/overall/'
    def setUp(self):
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Lost")
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Closed")
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Open")
        #self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
    def test_overall_count_success(self):
        res  =self.client.get(self.url)
        item = Beeline.objects.filter(status="Closed").count()
        self.assertEqual(item,1)
        self.assertEqual(res.status_code, 200)
    
    def test_overall_count_wrong_method(self):
        res  =self.client.put(self.url)
        self.assertEqual(res.status_code, 405)

class TestOverallProfileCount(APITestCase):
    url = 'http://localhost:8000/OverallProfileCount/'
    #url2 = 'http://localhost:8000/practie_count/'
    
    def setUp(self):

        self.beeline1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
        self.beeline2 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Lost")
        self.profile1  =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline1)
        self.profile2 = Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline2)
        self.profile3 = Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline1)
        self.profile4 =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline1)
        self.profile4 =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline1)
        self.profile4 =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline1)
        self.profile5 =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline1)

    def test_overall_count_success(self):

        res  =self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
    
    def test_overall_count_wrong_method(self):
        res  =self.client.put(self.url)
        self.assertEqual(res.status_code, 405)
    """def test_practice_count_success(self):
        res = self.client.get(self.url2)
        self.assertEqual(res.status_code, 202)
    def test_practice_count_wrong_method(self):
        res = self.client.put(self.url2)
        self.assertEqual(res.status_code, 405)"""
class TestNewBeelineMail(APITestCase):
    
    
    url = 'http://localhost:8000/mail_new_beeline/'
    

    
    def test_mail(self):
        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            'beeLine_Request_Number': '123',
                'job_description': 'Test job',
                'department': 'Test department',
                'no_of_positions': 1,
                'priority': 'High',
                'status': 'Open',
                'cv_DeadLine': '2022-03-01',
                'billing_Rate': 100,
                'hours_per_week': 40,
                'contact_person': 'Test person',
                'date_request': '2022-02-22',
                "prodapt_practice":"SF Practice",
                "prodapt_POC":"Malavika",
                "dutch_Language":"No",
                "location":"Panama",
                "key_skills":"Django,Python"
        }
        
        

        res = self.client.post(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 200)

class TestNewProfileMail(APITestCase):
    
    
    url = 'http://localhost:8000/mail_new_profile/'
    url2 = 'http://localhost:8000/mail_updated_profile/'
    
    def setUp(self):

        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
        self.obj2  =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.obj1)
        

    
    def test_profile_mail(self):
        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            "current_Status":"Open",
            "name_of_candidate":"Tejaswini",
            
            "next_step":"NA",
            
            "location_relocation":"India",
            
            "client_Interview":"YES",
            "comments":"NA",
            "beeline":self.obj1.id
        }
        
        

        res = self.client.post(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 200)
        res = self.client.post(self.url2,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 200)
        

class TestUpdatedBeelineMail(APITestCase):
    
    
    url = 'http://localhost:8000/mail_updated_beeline/'
    

    

    
    def test_mail(self):
        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            'beeLine_Request_Number': '123',
                'job_description': 'Test job',
                'department': 'Test department',
                'no_of_positions': 1,
                'priority': 'High',
                'status': 'Open',
                'cv_DeadLine': '2022-03-01',
                'billing_Rate': 100,
                'hours_per_week': 40,
                'contact_person': 'Test person',
                'date_request': '2022-02-22',
                "prodapt_practice":"SF Practice",
                "prodapt_POC":"Malavika",
                "dutch_Language":"No",
                "location":"Panama",
                "key_skills":"Django,Python"
        }
        
        

        res = self.client.post(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 200)
        



class TestBeelineDelete(APITestCase):
    def setUp(self):
        self.beeline = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",file="",status="Fulfilled")
        self.profile = Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=self.beeline)
        self.url = reverse('mail_delete_beeline', kwargs={'pk': self.beeline.pk})
        self.url1 = reverse('mail_profile_beeline', kwargs={'pk': self.profile.pk})
    
    
    def test_beeline_delete(self):

        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            'beeLine_Request_Number': '123',
                'job_description': 'Test job',
                'department': 'Test department',
                'no_of_positions': 1,
                'priority': 'High',
                'status': 'Open',
                'cv_DeadLine': '2022-03-01',
                'billing_Rate': 100,
                'hours_per_week': 40,
                'contact_person': 'Test person',
                'date_request': '2022-02-22',
                "prodapt_practice":"SF Practice",
                "prodapt_POC":"Malavika",
                "dutch_Language":"No",
                "location":"Panama",
                "key_skills":"Django,Python"
        }
        user_data1 = {
            "current_Status":"Open",
            "name_of_candidate":"Tejaswini",
            
            "next_step":"NA",
            
            "location_relocation":"India",
            
            "client_Interview":"YES",
            "comments":"NA",
            "beeline":self.beeline.id
        }
        
        

        res = self.client.post(self.url,user_data)
        self.assertEqual(res.status_code, 200)
        res = self.client.post(self.url1,user_data1)
        self.assertEqual(res.status_code, 200)

class TestContactUs(APITestCase):
    url  = 'http://localhost:8000/mail_contact_us/'
    user_data = {
        "name":"Tejaswini",
        "email":"teja@email.com",
        "mesaage":"hello"
    }
    def test_contact_us(self):
        res = self.client.post(self.url,self.user_data)
        self.assertEqual(res.status_code, 200)
class TestUpdatedBeeline(APITestCase):
    def setUp(self):
        self.beeline = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",file=None,status="Fulfilled")
        self.profile = Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",cv_Attachment=None,beeline=self.beeline)
        self.url = reverse('updated_beeline', kwargs={'pk': self.beeline.pk})
        
        
    def test_beeline_patch(self):
        from io import BytesIO
        from django.core.files import File
        file = BytesIO(b"file content")
        file.name = "test.txt"
        file.content_type = "text/plain"

        user_data = {
            'beeLine_Request_Number': '123',
                'job_description': 'Test job',
                'department': 'Test department',
                'no_of_positions': 1,
                'priority': 'High',
                'status': 'Open',
                'cv_DeadLine': '2022-03-01',
                'billing_Rate': 100,
                'hours_per_week': 40,
                'contact_person': 'Test person',
                'date_request': '2022-02-22',
                "prodapt_practice":"SF Practice",
                "prodapt_POC":"Malavika",
                "dutch_Language":"No",
                "location":"Panama",
                "key_skills":"Django,Python",
                'file':None
        }
        
        

        res = self.client.patch(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 200)
        res = self.client.patch(self.url,{"User": json.dumps(user_data), "file": "undefined"})
        self.assertEqual(res.status_code, 200)
        

class TestUpdatedProfile(APITestCase):
    def setUp(self):
        self.beeline = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
        
        self.profile = Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",cv_Attachment=None,beeline=self.beeline)
        self.profile1 = Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",cv_Attachment="",beeline=self.beeline)
        self.url = reverse('updated_profile', kwargs={'pk': self.profile.pk})
        self.url1 = reverse('updated_profile', kwargs={'pk': self.profile1.pk})

    
    def test_profile_patch(self):
        

        user_data = {
            "current_Status":"Open",
            "name_of_candidate":"Tejaswini",
            
            "next_step":"NA",
            
            "location_relocation":"India",
            
            "client_Interview":"YES",
            "comments":"NA",
            "beeline":self.beeline.id
            
        }
        
        

        res = self.client.patch(self.url,{"User": json.dumps(user_data), "file": "undefined"})
        self.assertEqual(res.status_code, 200)
        res = self.client.patch(self.url,{"User": json.dumps(user_data), "file": file})
        self.assertEqual(res.status_code, 200)
        

        
class TestSendCredentials(APITestCase):
    url = 'http://localhost:8000/SendCrendentials/'
    user_data_reg={
        'username':"email",
        'email':"email@email.com",
        "first_name":"Teju",
        "last_name":"Reddy",
        'password1':config('TEST_CASES_PASSWORD'),
        'password2':config('TEST_CASES_PASSWORD')
    }
    
    def test_send_credentials_post_success(self):


        res = self.client.post(self.url,self.user_data_reg,format='json')
        self.assertEqual(res.status_code, 200)
class TestPasswordResetMail(APITestCase):
    register_url = reverse('Register')
    url = 'http://localhost:8000/ResetPasswordMail/'
    
    

    user_data_reg={
        'username':"email",
        'email':"email@email.com",
        "first_name":"Teju",
        "last_name":"Reddy",
        'password':config('TEST_CASES_PASSWORD'),
        'password2':config('TEST_CASES_PASSWORD')
    }

    data1 = {
        "Username":"email"
    }
    def test_password_rest_mail_success(self):
        self.client.post(self.register_url,self.user_data_reg,format="json")
        res = self.client.post(self.url,self.data1,format='json')
        self.assertEqual(res.status_code, 200)
    
class TestAlertMail(APITestCase):
    alert_url = 'http://localhost:8000/alertsendmail/'
    
        

    def test_alert_mail_success(self):
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-14",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Fulfilled")
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Lost")
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Closed")
        self.obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",status="Open")
        res = self.client.get(self.alert_url)
        self.assertEqual(res.status_code, 201)
    def test_alert_mail_with_empty_beeline(self):
        res = self.client.get(self.alert_url)
        self.assertEqual(res.status_code, 200)
class TestUserInfo(APITestCase):
    #url = 'http://localhost:8000/alertsendmail/'
    def setUp(self):
        
        self.data = User.objects.create_user(username="teju_12",email="email@email.com",first_name="Teju",last_name="Reddy",password=config('TEST_CASES_PASSWORD'))
        self.url = reverse('edituserinfo', kwargs={'pk': self.data.pk})
    


    def test_edit_user_info_post_success(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 201)
    def test_edit_user_info_patch(self):
        user_data = {
            "username":"",
            "first_name":"",
            "last_name":"",
            "email":""
        }
        res = self.client.patch(self.url,user_data,format="json")
        self.assertEqual(res.status_code, 200)













    
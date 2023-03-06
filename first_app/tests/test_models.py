from rest_framework.test import APITestCase
from first_app.models import Beeline,Profile

class BeelineModelTestCase(APITestCase):
    def setUp(self):
        Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",file="",status="Fulfilled")
        Beeline.objects.create(beeLine_Request_Number="2100-2",job_description="Project Manager",department="QA",no_of_positions=4,priority="Medium",cv_DeadLine="2023-03-01",billing_Rate="90$-120$",hours_per_week=90,contact_person="William",date_request="2023-05-24",file="",status="Lost")

    
    def test_check_beeline_info(self):
        qs = Beeline.objects.all()
        self.assertEqual(qs.count(),2)

    def test_find_beeline_Lost_count(self):

        res = Beeline.objects.filter(status="Lost").count()
        self.assertEqual(res,1)
    def test_find_beeline_Close_count(self):
        res = Beeline.objects.filter(status="Closed").count()
        self.assertEqual(res, 0)


class ProfileModelTestCase(APITestCase):
    def setUp(self):
        obj1 = Beeline.objects.create(beeLine_Request_Number="2100-7",job_description="SSE",department="Delivery",no_of_positions=9,priority="High",cv_DeadLine="2023-03-01",billing_Rate="90$",hours_per_week=40,contact_person="Markin",date_request="2023-03-01",file="",status="Fulfilled")
        obj2  =  Profile.objects.create(current_Status="New",name_of_candidate="Manoj",next_step="NA",location_relocation="India",client_Interview="No",comments="NA",beeline=obj1)

    def test_model_created(self):
        qs=Profile.objects.all().count()
        self.assertEqual(qs, 1)
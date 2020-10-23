from django.test import TestCase
from .models import Profile,Project,Comment
from django.contrib.auth.models import User
import datetime as dt
# Create your tests here.

class ProfileTestClass(TestCase):
    def setUp(self):
        self.new_user=User(id=1,username='Jo')
        self.new_profile=Profile(id=2,bio='lionne',profile_pic='default.jpg',full_name='jojo', user=self.new_user, email='joselynejojo740@gmail.com', phone_number='0787753215')


    def test_instance(self): 
        self.assertTrue(isinstance(self.new_profile,Profile))  
        self.assertTrue(isinstance(self.new_user,User))
    

    def test_save_profile(self):
        self.new_profile.save_profile()
        profiles=Profile.objects.all()
        self.assertTrue(len(profiles)>0)


    def tearDown(self):
        Profile.objects.all().delete()
    
    
    def test_delete_profile(self):
        self.new_profile.delete_profile()
        self.assertEqual(len(Profile.objects.all()),0)


class ProjectTestClass(TestCase):
    def setUp(self):

        self.new_user=User(id=1,username='Jo')
        self.new_profile=Profile(id=2,bio='lionne',profile_pic='default.jpg',full_name='jojo', user=self.new_user, email='joselynejojo740@gmail.com', phone_number='0787753215')
        self.new_project=Project(id=3,title='song',image='default.jpg', user=self.new_user, profile=self.new_profile, description='cool',vote=5,)

    def test_instance(self): 
        self.assertTrue(isinstance(self.new_profile,Profile))  
        self.assertTrue(isinstance(self.new_user,User))
        self.assertTrue(isinstance(self.new_project,Project))

    def test_save_project(self):
        self.new_project.save_project()
        projects=Project.objects.all()
        self.assertTrue(len(projects)>0)

    def tearDown(self):
        Project.objects.all().delete()

    def test_delete_project(self):
        self.new_project.delete_project()
        self.assertEqual(len(Project.objects.all()),0)
 
class CommentTestClass(TestCase):
    def setUp(self):

        self.new_user=User(id=1,username='Jo')
        self.new_project=Project(id=3,title='song',image='default.jpg', user=self.new_user, description='cool',vote=5,)
        self.new_comment=Comment(id=4,comment='comments',user=self.new_user, project=self.new_project)

    def test_instance(self): 
        
        self.assertTrue(isinstance(self.new_user,User))
        self.assertTrue(isinstance(self.new_project,Project))
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_save_comment(self):
        self.new_comment.save_comment()
        comments=Comment.objects.all()
        self.assertTrue(len(comments)>0)

    def tearDown(self):
        Comment.objects.all().delete()

    def test_delete_comment(self):
        self.new_comment.delete_comment()
        self.assertEqual(len(Comment.objects.all()),0)
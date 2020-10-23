from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Profile,Project,Comment
from .forms import NewProfileForm,NewProjectForm,VoteForm,NewCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework import status
from django.db.models import Max,F



@login_required(login_url='/accounts/login/')
def welcome(request):
    current_user = request.user
    user_profile= Profile.objects.filter(user=current_user.id).first()
    comment= Comment.objects.filter(user=current_user.id).first()
    projects = Project.objects.all()
    average=0

    for project in projects:
        average=(project.design + project.usability + project.content)/3
        rating = round(average,2)
    return render(request, 'users/index.html', {'user_profile':user_profile, 'projects':projects,'rating':rating,'comment':comment})


@login_required(login_url='/accounts/login/')
def user_profile(request):
    current_user = request.user
    projects = Project.objects.filter(user=current_user).all()
    user_profile = Profile.objects.filter(user=current_user.id).first()
    

    return render(request, 'users/user_profile.html', { 'user_profile':user_profile,'projects':projects})




@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    
    if request.method == 'POST':
        form=NewProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile=form.save(commit=False)
            profile.user = current_user
            profile.save()

            return redirect('user-profile')

    else:
            form=NewProfileForm()

    return render(request, 'users/edit_profile.html', {'form':form,})


@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
  
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()

        return redirect ("welcome")

    else:
        form = NewProjectForm()

    return render(request, 'users/new_project.html', {"form": form})


def search_results(request):

    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_projects = Project.search_project(search_term)
        current_user=request.user
        message = f"{search_term}"
        return render(request, 'users/search.html',{"message":message,"titles": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'users/search.html',{"message":message})




class ProfileList(APIView):
    def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)


class ProjectList(APIView):
    def get(self, request, format=None):
        all_project = Project.objects.all()
        serializers = ProjectSerializer(all_project, many=True)
        return Response(serializers.data)

    
@login_required(login_url='/accounts/login/')
def rating(request,id):
    
    project=Project.objects.get(id=id)
    rating=round(((project.design + project.usability + project.content)/3),1)
    if request.method == 'POST':
        form=VoteForm(request.POST)
        if form.is_valid:
            project.vote+=1
            if project.design ==0:
                project.design = int(request.POST['design'])

            else:
                project.design = (project.design + int(request.POST['design']))/2

            if project.usability == 0:
                project.usability = int(request.POST['usability'])
            else:
                project.usability = (project.design + int(request.POST['usability']))/2
            if project.content == 0:
                project.content = int(request.POST['content'])
            else:
                project.content = (project.design + int(request.POST['content']))/2
            project.save()
            return redirect('welcome')
    else:
        form = VoteForm()
    return render(request,'users/vote.html',{'form':form,'project':project,'rating':rating})    


@login_required(login_url='/accounts/login/')
def new_comment(request, project_id):
    current_user = request.user
    project = Project.objects.get(id=project_id)
    profile = Profile.objects.filter(user=current_user.id).first()
    if request.method == 'POST':
        form=NewCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.project=project
            comment.save()
            
            return redirect('welcome')

    else:
        form = NewCommentForm()

    return render(request, 'users/new_comment.html', {'form': form,'profile':profile, 'project':project, 'project_id':project_id})

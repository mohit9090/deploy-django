from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .models import *

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .decorators import allow_unauthenticated_user, allow_authenticated_user, allow_users

from json import dumps


def home(request):
	""" This is to get the profile photo of google login users """
	# u = User.objects.get(username="mohit2")
	# google_u = u.socialaccount_set.all()[0]
	# google_u_prof_pic = google_u.extra_data['picture'];


	products = Product.objects.all()
	context = {'products':products}
	if request.user.is_authenticated:
		if request.user:
			# print(request.user)
			username = request.user.username
			customer = Customer.objects.get(user=request.user)
			bio = customer.bio
			context['username'] = username
			context['user_bio'] = bio
	return render(request, 'small/home.html', context)

@allow_unauthenticated_user(redirect_url="small:home")
def register(request):
	if request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		bio = request.POST.get('bio')
		register_as = request.POST.get('register_as')
		user = User.objects.create_user(username=username, email=email, password=password)
		if register_as == "employee":
			user.is_staff = True
			group = Group.objects.get(name="employee")
			user.groups.add(group)
		else:
			user.is_staff = False
			group = Group.objects.get(name="customer")
			user.groups.add(group)
		user.save()
		customer = Customer.objects.get(user=user)
		customer.bio = bio
		customer.save()

		# send email to user
		# template = render_to_string('small/email.html', {'name':username, 'email':settings.EMAIL_HOST_USER})
		# email = EmailMessage(
		# 	'Successfull Registration',
		# 	template,
		# 	settings.EMAIL_HOST_USER,
		# 	[email]
		# 	)
		# email.fail_silently = False
		# email.send()

		return redirect('small:home')
	return render(request, 'small/register.html')

@allow_unauthenticated_user(redirect_url="small:home")
def loginPage(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('small:home')

	return render(request, 'small/login.html')


def logoutPage(request):
	logout(request)
	return redirect('small:login')


def articlePage(request):
	articles = Article.objects.all()
	context = {'articles': articles}
	articleList = []
	for article in articles:
		articleDictionary = {}
		articleDict = builtArticleDictionary(articleDictionary, article)

		articleList.append(articleDict)

	# print(articleList)
	articleJSON = dumps(articleList)
	# print(articleJSON)
	context['articleJSON'] = articleJSON

	return render(request, 'small/article.html', context)

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['admin'])
def page1(request):
	return render(request, 'small/page1.html')

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['employee'])
def page2(request):
	return render(request, 'small/page2.html')

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['admin', 'employee'])
def page3(request):
	return render(request, 'small/page3.html')

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['customer'])
def page4(request):
	return render(request, 'small/page4.html')

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['customer', 'admin'])
def page5(request):
	return render(request, 'small/page5.html')

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['customer', 'employee'])
def page6(request):
	return render(request, 'small/page6.html')

@allow_authenticated_user(redirect_url="small:login")
@allow_users(allowed_roles=['admin', 'customer', 'employee'])
def page7(request):
	return render(request, 'small/page7.html')




def builtArticleDictionary(articleDictionary, article):
	articleAuthor = {}

	articleAuthor['name'] = article.author.user.username

	articleDictionary['id'] = article.id
	articleDictionary['title'] = article.title
	articleDictionary['content'] = article.content
	articleDictionary['author'] = articleAuthor
	articleDictionary['like'] = article.like

	return articleDictionary



"""

"""
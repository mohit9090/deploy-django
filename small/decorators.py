from django.http import HttpResponse
from django.shortcuts import redirect

def allow_unauthenticated_user(redirect_url):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.is_authenticated:
				return redirect(redirect_url)
			return view_func(request, *args, **kwargs)
		return wrapper_func
	return decorator



def allow_authenticated_user(redirect_url):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if not request.user.is_authenticated:
				return redirect(redirect_url)
			return view_func(request, *args, **kwargs)
		return wrapper_func
	return decorator


def allow_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse("You are not allowed to access this page")
		return wrapper_func
	return decorator
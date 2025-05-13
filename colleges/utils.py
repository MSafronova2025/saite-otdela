from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('profile')
    return wrapper

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.role == 'manager' or request.user.role == 'admin'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('profile')
    return wrapper

def client_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'client':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('profile')
    return wrapper

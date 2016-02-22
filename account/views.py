from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def user_login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                clean_data = form.cleaned_data
                user = authenticate(username=clean_data['username'], password=clean_data['password'])

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponse('Authenticated successfully')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    return HttpResponse('Invalid login')
        else:
            return render(request, 'account/login.html')
    except Exception as e:
        print(e)



def user_register(request):
    return render(request, 'account/register.html')

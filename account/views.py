from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm

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



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password( form.cleaned_data['password'] )
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {
        'form': form
    })

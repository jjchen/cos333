from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
def login(request):
    def errorHandle(error):
        form = LoginForm()
return render_to_response('login.html', {
        'error' : error,
        'form' : form,
        })
if request.method == 'POST': # If the form has been submitted...
    form = LoginForm(request.POST) # A form bound to the POST data
if form.is_valid(): # All validation rules pass
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Redirect to a success page.
            login(request, user)
            return render_to_response('courses/logged_in.html', {
                    'username': username,
                    })
        else:
            # Return a 'disabled account' error message
            error = u'account disabled'
            return errorHandle(error)
    else:
         # Return an 'invalid login' error message.
        error = u'invalid login'
        return errorHandle(error)
else:
    error = u'form is invalid'
    return errorHandle(error)
else:
    form = LoginForm() # An unbound form
return render_to_response('login.html', {
        'form': form,
        })

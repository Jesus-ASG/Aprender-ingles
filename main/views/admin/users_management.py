from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.http import JsonResponse


def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def index(request):
    if request.method == 'GET':
        users = User.objects.exclude(id=request.user.id).values('id', 'username', 'email', 'is_staff', 'is_superuser')
        users = [request.user] + list(users)
        context = {
            'users': users
        }
        return render(request, 'admin/users_management.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def delete(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        if user:
            if request.user.id == user.id:
                return JsonResponse({'message': 'You can\'t delete your own user'})
            user.delete()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message:' 'not found'})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def update(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        if user:
            if request.user.id == user.id:
                #return JsonResponse({'message': 'You can\'t edit your own user'})
                return redirect('management_users')

            email = request.POST.get('email')
            is_superuser = request.POST.get('is_superuser') == 'on'
            is_staff = request.POST.get('is_staff') == 'on'

            if email=='':
                #return JsonResponse({'message': 'An email is required'})
                return redirect('management_users')

            user.email = email
            user.is_superuser = is_superuser
            user.is_staff = is_staff
            user.save()

            return redirect('management_users')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from .models import Profile

@login_required
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return render(request, 'login.html', {'next': next})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next = request.POST.get('next', '/')
        print(next)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            profile = get_object_or_404(Profile, user=request.user) # Profileテーブルから該当のユーザを取得
            language = profile.language
            request.session['_language'] = language # この通信のsessionに言語を設定する
            return redirect(next)
        else:
            return render(request, 'login.html', {'next': next, 'error': True})

@login_required
def logout_view(request):
    del request.session['_language'] # このsessionの言語設定を削除する
    return auth_views.logout_then_login(request)

# 言語設定用view関数
@login_required
def language(request):
    if request.method == 'GET':
        return render(request, 'language.html')
    elif request.method == 'POST':
        language = request.POST['language']
        profile = get_object_or_404(Profile, user=request.user) # Profileテーブルから該当のユーザを取得
        profile.language = language # Profileにユーザからのリクエスト言語を設定
        profile.save() # DB更新
        request.session['_language'] = language # この通信のsessionに言語を設定する

        return redirect('language')

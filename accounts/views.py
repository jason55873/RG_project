from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # 登入成功後導向首頁（請依實際頁面修改）
        else:
            messages.error(request, "帳號或密碼錯誤")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')  # 登出後導回登入頁


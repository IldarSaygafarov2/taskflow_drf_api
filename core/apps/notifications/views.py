from django.shortcuts import render, redirect
from core.apps.users.models import CustomUser
from .models import Notification
from django.contrib.auth import login
from .forms import CustomUserAuthenticationForm


def show_notifications_example_page(request):
    if request.method == "POST":
        form = CustomUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        return redirect("notifications-page")

    # if not request.user.is_authenticated:
    #     return redirect("notifications-page")

    form = CustomUserAuthenticationForm()
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
    else:
        notifications = []
    context = {"notifications": notifications, "form": form}
    return render(request, "notification_example.html", context)

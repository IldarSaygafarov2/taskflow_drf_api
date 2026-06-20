from django.shortcuts import render


def show_notifications_example_page(request):
    return render(request, "notification_example.html")

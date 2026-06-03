from django.shortcuts import render

from rest_framework import generics


class WorkspacesListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        return ["1", "2"]


class WorkSpacesDetailView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

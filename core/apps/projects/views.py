from django.shortcuts import render
from rest_framework import generics

from . import models, serializers


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ProjectListSerializer
    queryset = models.Project.objects.all()


class ProjectRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    serializer_class = serializers.ProjectListSerializer
    queryset = models.Project.objects.all()

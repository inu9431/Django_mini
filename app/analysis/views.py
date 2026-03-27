from django.shortcuts import render
from rest_framework import generics

from app.analysis.models import Analysis
from app.analysis.serializers import AnalysisSerializer

class AnalysisListView(generics.ListCreateAPIView):
    serializer_class = AnalysisSerializer

    def get_queryset(self):
        queryset = Analysis.objects.filter(user=self.request.user)
        period_type = self.request.query_params.get("type")
        if period_type:
            queryset = queryset.filter(type=period_type)
        return queryset


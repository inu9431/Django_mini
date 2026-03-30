from rest_framework import generics

from app.analysis.models import Analysis
from app.analysis.serializers import AnalysisSerializer

class AnalysisListView(generics.ListAPIView):
    serializer_class = AnalysisSerializer

    def get_queryset(self):
        queryset = Analysis.objects.filter(user=self.request.user)
        period_type = self.request.query_params.get("type")
        if period_type:
            queryset = queryset.filter(period_type=period_type)
        return queryset


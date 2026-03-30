from django.urls import path
from app.analysis.views import AnalysisListView

urlpatterns = [
    path("", AnalysisListView.as_view(), name="analysis_list"),
]


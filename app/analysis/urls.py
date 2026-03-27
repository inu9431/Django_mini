from django.conf import settings
from django.urls import path
from app.analysis.views import AnalysisListView

urlpatterns = [
    path("", AnalysisListView.as_view(), name="analysis_list"),
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('app.users.urls')),
    path('api/budgets/', include('app.budgets.urls')),
    path("api/analysis/", include('app.analysis.urls')),
    path("api/notifications/", include('app.notification.urls')),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG and not settings.TESTING:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

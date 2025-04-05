from django.contrib import admin
from django.urls import path, include

from sending_emeil.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sending/', include("sending_emeil.urls", namespace="sending")),
    #path('authorization/', include("authorization.urls", namespace="auth")),
    path('', HomeView.as_view()),
]

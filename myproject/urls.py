from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403
from django.conf.urls import handler404
from taski.views import custom_permission_denied_view
from taski.views import custom_page_not_found_view

handler403 = custom_permission_denied_view
handler404 = custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('taski.urls')),
    path('', include('dashboard.urls')),
]

from django.urls import path, include

from progressbar.views import create_user_view, UserListView

app_name = "progress_bar"
urlpatterns = [
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('celery-progress/', include('celery_progress.urls', namespace="celery_progress"), name='celery-progress'),
    path('', create_user_view, name='create-users'),
]

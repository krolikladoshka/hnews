from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.views import PostsListViewSet, ScheduleParsingView

router = DefaultRouter()

router.register(r'posts', PostsListViewSet, 'posts')

urlpatterns = [
    path('posts/schedule-parsing', ScheduleParsingView.as_view()),
]
urlpatterns += router.urls

from rest_framework import viewsets, mixins, filters, views, status
from rest_framework.response import Response

from posts.models import Post
from posts.serializer import PostSerializer
from posts.tasks import parse_hackernews_site


class PostsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'


class ScheduleParsingView(views.APIView):
    def post(self, request, *args, **kwargs):
        parse_hackernews_site.delay()

        return Response(status=status.HTTP_202_ACCEPTED)

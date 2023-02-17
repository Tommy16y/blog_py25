from applications.post.serializers import PostSerializer, PostImageSerializer ,CommentSerializer
from rest_framework import generics
from applications.feedback.serializers import RatingSerializer
from applications.post.models import Post , PostImage ,Comment
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from applications.post.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from applications.feedback.models import Like,Rating



count=0
class CustomPagination(PageNumberPagination):
    page_size = 3 
    page_size_query_param = 'page_size'
    max_page_size = 10000



# class PostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostCreateAPIView(generics.CreateAPIView):
#     serializer_class = PostSerializer

# class PostUpdateAPIView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDeleteAPIView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetailAPIView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'id'



# class PostListCreateAPIView(generics.ListCreateAPIView):
    
#     permission_classes = [IsOwner]
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    # pagination_class = CustomPagination

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['owner','title',]

    # search_fields = ['title']
    # ordering_fields = ['id']
#     # def get_queryset(self):
#     #     queryset = super().get_queryset()
#     #     # queryset = queryset.filter(owner=9)
#     #     filter_owner = self.request.query_params.get('owner')
#     #     if filter_owner:
#     #         queryset = queryset.filter(owner=filter_owner)
#     #     return queryset
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class PostDetailDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [IsOwner]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer



class PostModelViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]

    pagination_class = CustomPagination
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner','title',]
    search_fields = ['title']
    ordering_fields = ['id','owner']


    @action(methods=['POST'], detail=True) #localhost:8000/api/v1/post/1/like
    def like(self, request, pk, *args, **kwargs):
        user = request.user
        print(user)
        
        like_obj, _ = Like.objects.get_or_create(owner = user,post_id= pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        status = 'liked'
        if not like_obj.is_like:
            status = 'unliked'
        return Response({'status':status})


    @action(methods=['POST'],detail=True)
    def rating(self, request, pk , *args ,**kwargs): #localhost:8000/api/v1/post/18/rating
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(owner = request.user ,post_id=pk)
        rating_obj.rating = serializer.data['rating']
        rating_obj.save()
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CreateImageAPIView(generics.CreateAPIView):

    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticated]
  # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # representation['name']='John'
    #     # print(representation)
    #     representation['owner'] = instance.owner.email

    #     # representation['title'] = self.get_attribute('email')
    #     return representation

class CommentViewSet(ViewSet): 
    
    def list (self,request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)



class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
        
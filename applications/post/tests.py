from django.test import TestCase
from rest_framework.test import APITestCase , APIRequestFactory, force_authenticate
from applications.post.views import *
from django.contrib.auth import get_user_model



User = get_user_model()

class PostTest(APITestCase):
    """
        Test post view 

    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
    
    @staticmethod
    def setup_user():
        user = User.objects.create_user(email = 'test@test.com', password = 'test123', is_active = True, )
        return user 
    
    def test_get_post(self):
        request = self.factory.get('api/v1/post/')
        view = PostModelViewSet.as_view({'get':'list'})
        response = view(request)


        assert response.status_code == 200     
        assert response.data['count'] == 0
    
    def test_create_post(self):
        data = {
            'description': 'Testttt',
            'title': 'test'
        }
        
        request = self.factory.post('api/v1/post/', data)
        force_authenticate(request, self.user)
        view = PostModelViewSet.as_view({'post':'create'})
        response = view(request)
        print(response.data)

        assert response.status_code == 201
        assert Post.objects.filter(title = 'test').exists()

    






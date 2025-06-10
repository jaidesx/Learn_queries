from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from blogs.models import Blog
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogTests(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(
            email="jamiefox@gmail.com",
            first_name="jamie",
            last_name="fox",
            password="password123@"
        )
        self.client.force_authenticate(user=self.user)

        # Create a sample blog
        self.blog = Blog.objects.create(name="Sinners", tagline="We all sin at One Time")
        self.blog_url = reverse("blog-detail", args=[self.blog.id])
        self.blog_list_url = reverse("blogs")

    # Test creating a new blog
    # Test retrieving all blogs
    # Test retrieving a single blog by ID
    # Test updating an existing blog
    # Test deleting a blog
    # Test accessing a non-existent blog returns 404
    # Test that unauthenticated users cannot access blog endpoints

    def test_create_blog(self):
        """Test creating a new blog"""
        data = {
            "name": "High School Heroes",
            "tagline": "A model student, once focused solely on grades, faces domestic abuse and school bullying."
        }
        response = self.client.post(self.blog_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_blog_creation_without_name(self):
        """Test creating a new blog with no name"""
        data = {
            "name": "",
            "tagline": "Money will come."
        }
        response = self.client.post(self.blog_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_blog_creation_without_tagline(self):
        """Test creating a new blog with no tagline"""
        data = {
            "name": "Jamiefox",
            "tagline": ""
        }
        response = self.client.post(self.blog_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_all_blogs(self):
        """Test retrieving all blogs"""
        response = self.client.get(self.blog_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_blog(self):
        """Test retrieving a single blog by ID"""
        response = self.client.get(self.blog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.blog.name)

    def test_update_blog(self):
        """Test updating an existing blog"""
        updated_data = {"name": "Good Boy", "tagline": "Medalist joins Police to Arrest criminals."}
        response = self.client.put(self.blog_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Good Boy")

    def test_delete_blog(self):
        """Test deleting a blog"""
        response = self.client.delete(self.blog_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blog.objects.filter(id=self.blog.id).exists())

    def test_blog_not_found(self):
        """Test accessing a non-existent blog returns 404"""
        url = reverse("blog-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access blog endpoints"""
        self.client.force_authenticate(user=None)  # Logout
        response = self.client.get(self.blog_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

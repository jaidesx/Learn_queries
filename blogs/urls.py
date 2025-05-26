from django.urls import path

from blogs.views import BlogList, BlogDetail

urlpatterns = [
    path("", BlogList.as_view(), name="blogs"),
    path("<int:pk>/", BlogDetail.as_view(), name="blog-detail"),
]
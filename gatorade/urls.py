"""
URL configuration for gatorade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from gatoradeapi.views import (register_user, login_user, AuthorViewSet, CategoryViewSet,
                               CommentViewSet, SubscriptionViewSet, PostView, TagView, ReactionView,
                               deactivate_user, activate_user)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'authors', AuthorViewSet, 'author')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'comments', CommentViewSet, 'comment')
router.register(r'subscriptions', SubscriptionViewSet, 'subscription')
router.register(r'posts', PostView, 'post')
router.register(r'tags', TagView, 'tag')
router.register(r'reactions', ReactionView, 'reaction')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('deactivate/<int:pk>', deactivate_user),
    path('activate/<int:pk>', activate_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]

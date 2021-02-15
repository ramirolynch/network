from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'likes', views.LikeViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [


    # I added the word api in the route to make it different from the empty path
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addpost", views.addpost, name="addpost"),
    path("allposts", views.allposts, name="allposts"),
    path("postpages", views.postpages, name="postpages"),
    path("following", views.following, name="following"),
    path("liketoggle/<int:post_id>", views.liketoggle, name="liketoggle"),
    path("user/<str:author>/", views.user_list, name="user_list"),

     # API Routes
    
    # path("likes/<int:post_id>", views.postLiker, name="postLiker")
   
]




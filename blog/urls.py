from django.urls import path,include

from rest_framework import routers
from . import views
from rest_framework_swagger.views import get_swagger_view


schema_view=get_swagger_view(title='Blog Api Documentation')

router=routers.DefaultRouter()
router.register('',views.blog,basename="blog")

# blogviewsets=views.blogs.as_view({
#     'get':'list',
#     "post":"create"
# })
urlpatterns = [
    path('blog/',include(router.urls)),
    path('documentation/',schema_view),
    path('register/',views.createuserView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    # path('blog/',blogviewsets),
]

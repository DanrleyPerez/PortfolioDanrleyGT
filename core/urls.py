from django.urls import path
from .views import index,  loginz, singup, logado
from .form import FormularioLogin

urlpatterns = [
    path('', index.as_view()),
    path('loginz/', loginz.as_view()),
    path('singup/', singup.as_view()),
    path('logado/', logado),

]
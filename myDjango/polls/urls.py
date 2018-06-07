from django.urls import path
from . import views

urlpatterns = [
	path('<int:question_id>/', views.detail, name='detail'),
	path('<int:question_id>/', views.results, name='results'),
	path('<int:question_id>/', views.vote, name='vote'),
]
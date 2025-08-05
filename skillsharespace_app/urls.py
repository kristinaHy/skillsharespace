from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question-list'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question-edit'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:pk>/answer/', views.AnswerCreateView.as_view(), name='answer-create'),
    path('moderator/', views.ModeratorDashboardView.as_view(), name='mod-dashboard'),
    path('moderator/approve/<str:content_type>/<int:object_id>/', views.approve_content, name='approve-content'),
    path('moderator/dismiss/<int:flag_id>/', views.dismiss_flag, name='dismiss-flag'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]

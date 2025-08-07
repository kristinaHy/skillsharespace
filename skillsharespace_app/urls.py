from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question-list'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question-update'),  
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:pk>/answer/', views.AnswerCreateView.as_view(), name='answer-create'),
    path('answer/<int:pk>/update/', views.AnswerUpdateView.as_view(), name='answer-update'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='answer-delete'),


    path('moderator/', views.ModeratorDashboardView.as_view(), name='mod-dashboard'),
    path('moderator/unapproved-questions/', views.UnapprovedQuestionListView.as_view(), name='moderator-unapproved-questions'),
    path('moderator/unapproved-answers/', views.UnapprovedAnswerListView.as_view(), name='moderator-unapproved-answers'),

    path('moderator/approve/<str:content_type>/<int:object_id>/', views.approve_content, name='approve-content'),
    path('moderator/dismiss/<int:flag_id>/', views.dismiss_flag, name='dismiss-flag'),

    path('moderator/question/<int:pk>/approve/', views.ApproveQuestionView.as_view(), name='approve-question'),
    path('moderator/question/<int:pk>/unapprove/', views.UnapproveQuestionView.as_view(), name='unapprove-question'),
    path('moderator/answer/<int:pk>/approve/', views.ApproveAnswerView.as_view(), name='approve-answer'),
    path('moderator/answer/<int:pk>/unapprove/', views.UnapproveAnswerView.as_view(), name='unapprove-answer'),
    path('moderator/question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='moderator-question-edit'),
    path('moderator/question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='moderator-question-delete'),
    path('moderator/answer/<int:pk>/edit/', views.AnswerUpdateView.as_view(), name='moderator-answer-edit'),
    
    path('moderator/answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='moderator-answer-delete'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]

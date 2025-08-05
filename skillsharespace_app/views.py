from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Question, Answer, Flag
from .forms import QuestionForm, AnswerForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qa/question_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Question.objects.filter(approved=True)
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return qs.order_by('-created_at')

class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_detail.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return super().get(request, *args, **kwargs)

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'qa/question_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'qa/question_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('question-list')
    template_name = 'qa/question_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'qa/answer_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)

class ModeratorDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Flag
    template_name = 'qa/mod_dashboard.html'
    context_object_name = 'flags'

    def test_func(self):
        return self.request.user.is_staff

def approve_content(request, content_type, object_id):
    if not request.user.is_staff:
        return redirect('question-list')
    model = Question if content_type == 'question' else Answer
    obj = get_object_or_404(model, id=object_id)
    obj.approved = True
    obj.save()
    return redirect('mod-dashboard')

def dismiss_flag(request, flag_id):
    if not request.user.is_staff:
        return redirect('question-list')
    flag = get_object_or_404(Flag, id=flag_id)
    flag.resolved = True
    flag.save()
    return redirect('mod-dashboard')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/signup.html'

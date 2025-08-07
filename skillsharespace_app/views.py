from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Question, Answer, Flag
from .forms import QuestionForm, AnswerForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm


from django.db.models import Q

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qa/question_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        user = self.request.user


        if user.is_authenticated:
            if user.is_staff:

                qs = Question.objects.all()
            else:

                qs = Question.objects.filter(Q(approved=True) | Q(author=user))
        else:

            qs = Question.objects.filter(approved=True)

        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(body__icontains=query))

        return qs.order_by('-created_at')

from django.db.models import Q
from django.http import Http404
from .models import Question

class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'qa/question_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user


        if user.is_authenticated and user.is_staff:
            return obj


        if obj.approved or (user.is_authenticated and obj.author == user):
            return obj


        if user.is_authenticated:
            from .models import Answer
            if Answer.objects.filter(question=obj, author=user).exists():
                return obj


        raise Http404("This question is not approved.")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        user = self.request.user


        if user.is_authenticated and user.is_staff:
            answers = question.answers.all()
        elif user.is_authenticated:
            answers = question.answers.filter(Q(approved=True) | Q(author=user))
        else:
            answers = question.answers.filter(approved=True)

        context['answers'] = answers.order_by('created_at')
        return context

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return super().get(request, *args, **kwargs)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'qa/question_form.html'
    success_url = reverse_lazy('question-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__  
        return context
    
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
        form.instance.approved = False  # mark unapproved initially
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        return context

    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk': self.kwargs['pk']})

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
    
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Question

class ApproveQuestionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = []  # No form fields, just updating approved status
    template_name = 'moderator/approve_confirm.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.approved = True
        messages.success(self.request, "Question approved successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('moderator-unapproved-questions').url

from .models import Answer

class ApproveAnswerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    fields = []
    template_name = 'moderator/approve_confirm.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.approved = True
        messages.success(self.request, "Answer approved successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('moderator-unapproved-answers').url


class UnapproveQuestionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = []
    template_name = 'moderator/confirm_unapprove.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.approved = False
        messages.success(self.request, "Question marked as unapproved.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mod-dashboard')


class UnapproveAnswerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    fields = []
    template_name = 'moderator/confirm_unapprove.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.approved = False
        messages.success(self.request, "Answer marked as unapproved.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mod-dashboard')

from django.http import Http404

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'qa/answer_form.html'

    def test_func(self):
        answer = self.get_object()
        user = self.request.user

        return user.is_staff or answer.author == user

    def get_success_url(self):
        question = self.get_object().question
        user = self.request.user


        if question.approved or (user.is_authenticated and (user.is_staff or question.author == user)):
            return reverse_lazy('question-detail', kwargs={'pk': question.pk})
        else:

            return reverse_lazy('question-list')


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'qa/answer_confirm_delete.html'
    success_url = reverse_lazy('question-list')  # You can change this to redirect to the question page

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author or self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404("You are not allowed to delete this answer.")




from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Question, Answer, Flag

class ModeratorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'moderator/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unapproved_questions'] = Question.objects.filter(approved=False)
        context['unapproved_answers'] = Answer.objects.filter(approved=False)
        context['unresolved_flags'] = Flag.objects.filter(resolved=False)
        return context



from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Question, Answer


class UnapprovedQuestionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Question
    template_name = 'moderator/unapproved_questions.html'
    context_object_name = 'questions'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Question.objects.filter(approved=False).order_by('-created_at')


class UnapprovedAnswerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Answer
    template_name = 'moderator/unapproved_answers.html'
    context_object_name = 'answers'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Answer.objects.filter(approved=False).order_by('-created_at')


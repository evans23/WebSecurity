from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from .models import RsaQuestion, TheWorldIsOver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from doctor_evils_layer.forms import BreakPrivateKeyForm, CreatePrivateKeyForm, EndGameForm, TransferMoneyForm, UploadFileForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

def redirect_if_game_over():
    end_game_object = TheWorldIsOver.objects.get(pk=1)
    if(end_game_object.game_is_over):
        return HttpResponseRedirect(reverse('victory-screen'))
    return None

class CurrentProfile(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get(self, request):
        should_redirect_to_victory = redirect_if_game_over()
        if should_redirect_to_victory:
            return should_redirect_to_victory
        self.queryset = User.objects.get(pk=request.user.pk)
        return super().get(request)

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'
    def get(self, request, pk):
        should_redirect_to_victory = redirect_if_game_over()
        if should_redirect_to_victory:
            return should_redirect_to_victory
        return super().get(request, pk)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update_form.html'
    fields = ['first_name', 'last_name']

    def get(self, request, pk):
        should_redirect_to_victory = redirect_if_game_over()
        if should_redirect_to_victory:
            return should_redirect_to_victory
        if request.user.pk != pk:
            return self.http_method_not_allowed(request, pk)
        return super().get(request, pk)

    def post(self, request, pk):
        should_redirect_to_victory = redirect_if_game_over()
        if should_redirect_to_victory:
            return should_redirect_to_victory

        form = UserUpdateForm(request.POST)
        request.user.first_name = form.data['first_name']
        request.user.last_name = form.data['last_name']
        request.user.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'pk': request.user.pk}))

class AboutDoctorEvil(LoginRequiredMixin, generic.TemplateView):
    template_name = 'about_doctor_evil.html'

    def get(self, request):
        should_redirect_to_victory = redirect_if_game_over()
        if should_redirect_to_victory:
            return should_redirect_to_victory
        return super().get(request)

@csrf_exempt
@login_required
def transfer_money(request):
    should_redirect_to_victory = redirect_if_game_over()
    if should_redirect_to_victory:
        return should_redirect_to_victory

    message = 'Last Transaction Succeeded!'
    if request.method == 'POST':
        form = TransferMoneyForm(request.POST)
        if form.is_valid():
            if float(form.data['transaction_amount']) <= request.user.bank_account.value:
                recipient = User.objects.get(pk=int(form.data['transfer_friend']))
                request.user.bank_account.successful_transaction = True

                request.user.bank_account.value -= float(form.data['transaction_amount'])
                request.user.bank_account.save()

                recipient.bank_account.value += float(form.data['transaction_amount'])
                recipient.bank_account.save()
                form = TransferMoneyForm(initial={'transfer_friend': User.objects.get(username='doctor_evil').pk, 'transaction_amount': 1000000})

                if recipient.username == 'doctor_evil':
                    message = f'{request.user.username}, THANK YOU FOR YOUR DONATION. I will be sure to use it ... FOR EVILLLLLLL'
            else:
                message = 'Insufficient funds to complete the transaction. Woops, somebody is out of money...'
                request.user.bank_account.successful_transaction = False
                form = TransferMoneyForm(initial={'transfer_friend': User.objects.get(username='doctor_evil').pk, 'transaction_amount': 1000000})
        else:
            message = 'Last Transaction Failed! I only accept positive amounts to real users. Sorry!'
            request.user.bank_account.successful_transaction = False
            form = TransferMoneyForm(initial={'transfer_friend': User.objects.get(username='doctor_evil').pk, 'transaction_amount': 1000000})
    else:
        message = ''
        form = TransferMoneyForm(initial={'transfer_friend': User.objects.get(username='doctor_evil').pk, 'transaction_amount': 1000000})
    file_form = UploadFileForm(initial={'title': 'I love EVILLLLL'})
    context = {
        'current_value': request.user.bank_account.value,
        'message': message,
        'last_transaction_successful': request.user.bank_account.successful_transaction,
        'file_form': file_form,
        'form': form,
    }
    return render(request, 'transfer_money_form.html', context)

@csrf_exempt
@login_required
def upload_file(request):
    should_redirect_to_victory = redirect_if_game_over()
    if should_redirect_to_victory:
        return should_redirect_to_victory
    def handle_uploaded_file(f):
        with open(f'doctor_evils_layer/templates/{request.user.username}_Uploaded_File.html', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        else:
            form = UploadFileForm()
        return HttpResponseRedirect(reverse('transfer-money'))

@csrf_exempt
@login_required
def open_evil_statement(request):
    should_redirect_to_victory = redirect_if_game_over()
    if should_redirect_to_victory:
        return should_redirect_to_victory
    return render(request, f'{request.user.username}_Uploaded_File.html')

@login_required
def rsa_challenge(request):
    should_redirect_to_victory = redirect_if_game_over()
    if should_redirect_to_victory:
        return should_redirect_to_victory
    if request.method == 'GET':
        question_form_dicts = []
        if request.user.profile.is_user_done():
            return HttpResponseRedirect(reverse('about-doctor-evil'))
        for question in request.user.rsa_questions.all():
            if question.create_rsa_pair:
                question_form_dicts.append({'question': question, 'form': CreatePrivateKeyForm()})
            else:
                form = BreakPrivateKeyForm()
                form.public_key_n = question.public_key_n
                form.public_key_e = question.public_key_e
                question_form_dicts.append({'question': question, 'form': form})
        context = {
            'question_form_dicts': question_form_dicts
        }
        return render(request, 'rsa_challenge.html', context)

@login_required
def rsa_challenge_check_rsa_pair(request, pk):
    should_redirect_to_victory = redirect_if_game_over()
    if should_redirect_to_victory:
        return should_redirect_to_victory
    if request.method == 'POST':
        question=RsaQuestion.objects.get(pk=pk)
        if question.owner != request.user:
            raise PermissionDenied()
        if question.create_rsa_pair:
            form = CreatePrivateKeyForm(request.POST)
            if form.is_valid():
                question.public_key_n = int(form.cleaned_data['public_key_n'])
                question.public_key_e = int(form.cleaned_data['public_key_e'])
                question.private_key = int(form.cleaned_data['private_key'])
                question.completed = True
                question.message = 'Great Work Question Complete!'
            else:
                question.completed = False
                question.message = 'That key is invalid. Please try again!'
        else:
            form = BreakPrivateKeyForm(request.POST)
            form.public_key_n = question.public_key_n
            form.public_key_e = question.public_key_e
            if form.is_valid():
                question.private_key = int(form.cleaned_data['private_key'])
                question.completed = True
                question.message = 'Great Work! Question Complete!'
            else:
                question.completed = False
                question.message = 'That key is invalid. Please try again!'
    question.save()
    if request.user.profile.is_user_done():
        return HttpResponseRedirect(reverse('about-doctor-evil'))
    else:
        return HttpResponseRedirect(reverse('rsa-challenge'))

@login_required
def the_end_of_the_game(request):
    end_game_object = TheWorldIsOver.objects.get(pk=1)
    form = EndGameForm(request.POST)
    form.is_valid()
    try:
        end_game_object.end_the_game(form.cleaned_data['username'])
    except:
        if 'forgot' not in end_game_object.groups_to_defeat_doctor_evil:
            end_game_object.end_the_game('Some agent that forgot to enter a username...')
        else:
            end_game_object.end_the_game('Another nameless agent...')
    return HttpResponseRedirect(reverse('victory-screen'))

@login_required
def restart_the_game(request):
    end_game_object = TheWorldIsOver.objects.get(pk=1)
    end_game_object.restart_the_game()
    return HttpResponseRedirect(reverse('logout'))

@login_required
def victory_screen(request):
    end_game_object = TheWorldIsOver.objects.get(pk=1)
    if not end_game_object.game_is_over:
        return HttpResponseRedirect(reverse('current-profile'))
    context = {
        'end_game_object': end_game_object,
    }
    return render(request, 'victory_screen.html', context)

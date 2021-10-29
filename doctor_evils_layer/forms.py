import datetime
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from doctor_evils_layer.models import BankAccount
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

test_ints = [0, 1, 2, 4, 3, 6, 7, 9, 16, 23, 512, 1024, 2056, 513, 112, 111, 100, 233]

class UserUpdateForm(forms.Form):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {'first_name':_('Enter your new first name'), 'last_name': _('Enter your new last name')}

class TransferMoneyForm(ModelForm):
    def clean_transfer_friend(self):
        data = self.cleaned_data['transfer_friend']
        if data == None:
            raise ValidationError(_('Invalid transfer partner. Must select a user to transfer money to.'))
        return data

    def clean_transaction_amount(self):
        data = self.cleaned_data['transaction_amount']
        if data <= 0:
            raise ValidationError(_('Invalid Transaction amount, data must be non-negative.'))
        return data

    class Meta:
        model = BankAccount
        fields = ['transaction_amount', 'transfer_friend']
        labels = {'transaction_amount': _('How much would you like to send me, Dr. Evil, today?'), 'transfer_to':_('Send me the money.')}

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def rsa_pair_is_valid(n, e, d):
    valid = True
    for test_int in test_ints:
        if test_int < n:
            print(f'testing {test_int}')
            cyper_text = pow(test_int, e, mod=n)
            plain_text = pow(cyper_text, d, mod=n)
            if test_int != plain_text:
                valid = False
                break
    return valid

class CreatePrivateKeyForm(forms.Form):
    public_key_n = forms.IntegerField()
    public_key_e = forms.IntegerField()
    private_key = forms.IntegerField()

    def clean_private_key(self):
        try:
            n = int(self.cleaned_data['public_key_n'])
            e = int(self.cleaned_data['public_key_e'])
            d = int(self.cleaned_data['private_key'])
        except:
            raise ValidationError(_('Invalid input. Parameters not parsing.'))
        if not rsa_pair_is_valid(n, e, d):
            raise ValidationError(_('Invalid rsa pair. Plain text following encrypt/decrypt cyle did not match the orignal input.'))
        return d

    class Meta:
        labels = {'public_key_n': _('Public Key n:'), 'public_key_e': _('Public Key exponent:'), 'private_key':_('Private Key:')}
        help_text = {'public_key_n': _('Remember n = p * q where p and q are your selected primes.')}

class BreakPrivateKeyForm(forms.Form):
    public_key_n = 0
    public_key_e = 0
    private_key = forms.IntegerField()

    def clean_private_key(self):
        try:
            d = int(self.cleaned_data['private_key'])
        except:
            raise ValidationError(_('Invalid input. Parameters not parsing.'))
        if not rsa_pair_is_valid(self.public_key_n, self.public_key_e, d):
            raise ValidationError(_('Invalid rsa pair. Plain text following encrypt/decrypt cyle did not match the orignal input.'))
        return d

    class Meta:
        labels = {'private_key':_('Private Key:')}
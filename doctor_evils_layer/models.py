from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BankAccount(models.Model):
    value = models.FloatField(blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_account')
    transfer_friend = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='transfer to')
    transaction_amount = models.FloatField(blank=True, null=True)
    successful_transaction = models.BooleanField(null=True)

    @receiver(post_save, sender=User)
    def create_user_bank_account(sender, instance, created, **kwargs):
        if created:
            BankAccount.objects.create(owner=instance, value=3000000)

class RsaQuestion(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsa_questions')
    public_key_n = models.BigIntegerField(null=True, blank=True)
    public_key_e = models.BigIntegerField(null=True, blank=True)
    private_key = models.BigIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    create_rsa_pair = models.BooleanField(default=False)
    message = models.CharField(max_length=200, default='Good Luck!', null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_bank_account(sender, instance, created, **kwargs):
        questions_per_user = 5
        if created:
            while questions_per_user > 0:
                RsaQuestion.objects.create(owner=instance, create_rsa_pair=True)
                questions_per_user -= 1

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    all_questions_completed = models.BooleanField(default=False)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance, all_questions_completed=False)

    def is_user_done(self):
        user_is_done = all([question.completed for question in self.owner.rsa_questions.all()])
        self.all_questions_completed = user_is_done
        self.save()
        return user_is_done
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import sympy
from rsa_key_gen import RSA_key_gen

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

    question_paramenters = [
        (3, 14, None),
        (10, 50, None),
        (10, 1000, None),
        (1000, 10000000, "You will fail.")
    ]

    def create_make_key_question(owner):
        RsaQuestion.objects.create(owner=owner, create_rsa_pair=True)

    def create_break_key_question(owner, min_prime_size, max_prime_size, message=None):
        message = 'Good Luck!' if message == None else message
        key_maker = RSA_key_gen(min_prime_size, max_prime_size)
        key_maker.create_pair()
        RsaQuestion.objects.create(owner=owner, public_key_n=key_maker.n, public_key_e=key_maker.e, create_rsa_pair=False, message=message)

    @receiver(post_save, sender=User)
    def create_user_bank_account(sender, instance, created, **kwargs):
        if created:
            RsaQuestion.create_make_key_question(owner=instance)
            for parameter_set in RsaQuestion.question_paramenters:
                RsaQuestion.create_break_key_question(instance, parameter_set[0], parameter_set[1], parameter_set[2])

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

class TheWorldIsOver(models.Model):
    groups_to_defeat_doctor_evil = models.TextField(blank=True, null=True)
    game_is_over = models.BooleanField(default=False)

    def end_the_game(self, winning_group):
        self.game_is_over = True
        self.groups_to_defeat_doctor_evil = f'{self.groups_to_defeat_doctor_evil}, {winning_group}'
        self.save()

    def restart_the_game(self):
        self.game_is_over = False
        self.save()
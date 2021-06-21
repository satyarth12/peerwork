from django.contrib import admin
from account.models import Account, Review, EmailConfirmed, UserProfile, BankDetail

admin.site.register(Account)

admin.site.register(EmailConfirmed)

admin.site.register(Review)

admin.site.register(UserProfile)

admin.site.register(BankDetail)
from itertools import chain
from django.views.generic import ListView


from account.models import Account
from users.models import Preference,Verify
from django.contrib.auth import get_user_model

class SearchView(ListView):
    template_name = 'search/view.html'
    paginate_by = 20
    count = 0
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        name=self.request.user

        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['users']=get_user_model().objects.exclude(email=name)
        context['preference_list']=Preference.objects.exclude(user=name)
        context['verify']=Preference.objects.exclude(user=name)
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if query is not None and query!="":
            name=self.request.user
            
            account_results        = Account.objects.search(query)
            account_results=account_results.exclude(email=name)

            preference_results      = Preference.objects.search(query)
            preference_results=preference_results.exclude(user=name)


            # combine querysets 
            queryset_chain = chain(
                    account_results,
                    preference_results
            )        
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Account.objects.exclude(email=self.request.user) # just an empty queryset as default
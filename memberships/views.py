from django.shortcuts import render
from django.views.generic import ListView
from .models import Membership, UserMembership

# Gets the current memebership
def get_user_membership(request):
    user_membership_queryset = UserMembership.objects.filter(user=request.user)
    if user_membership_queryset.exists():
        return user_membership_queryset.first()
    return None


# Takes you to your selected membership page
class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

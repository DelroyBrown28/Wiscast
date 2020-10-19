from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from .models import Membership, UserMembership, Subscription


# Gets the current memebership
def get_user_membership(request):
    user_membership_queryset = UserMembership.objects.filter(user=request.user)
    if user_membership_queryset.exists():
        return user_membership_queryset.first()
    return None


def get_user_subscription(request):
    user_sub_queryset = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_sub_queryset.exists():
        user_subscription = user_sub_queryset.first()
        return user_subscription
    return None


# Takes you to your selected membership page
class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    # Handles POST from membership selection
    def post(self, request, **kwargs):
        selected_membership_type = request.POST.get('membership_type')

        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_queryset = Membership.objects.filter(
            membership_type=selected_membership_type)
        if selected_membership_queryset.exists():
            selected_membership = selected_membership_queryset.first()
        """
        =================
        VALIDATION CHECKS
        =================
        """
        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, "This is your current tier. Your \
                        next payment will be due on {}".format('get value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # Assign to session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))

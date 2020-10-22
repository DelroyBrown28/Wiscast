from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse
from .models import Membership, UserMembership, Subscription
import stripe


def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription,
    }
    return render(request, 'memberships/profile.html', context)


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


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_queryset = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_queryset.exists():
        return selected_membership_queryset.first()
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


def PaymentView(request):
    user_membership = get_user_membership(request)
    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("memberships:select"))
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']

            # UPDATE FOR STRIPE API CHANGE 2018-05-21

            '''
            First we need to add the source for the customer
            '''

            customer = stripe.Customer.retrieve(
                user_membership.stripe_customer_id)
            customer.source = token  # 4242424242424242
            customer.save()

            '''
            Now we can create the subscription using only the customer as we don't need to pass their
            credit card source anymore
            '''

            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {"plan": selected_membership.stripe_plan_id},
                ]
            )

            return redirect(reverse('memberships:update-transactions',
                                    kwargs={
                                        'subscription_id': subscription.id
                                    }))

        except:
            messages.info(
                request, "An error has occurred, investigate it in the console")

    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }

    return render(request, "memberships/membership_payments.html", context)


def updateTransactionRecords(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, "successfully created {} tier level".format(
        selected_membership))
    return redirect('memberships:select')

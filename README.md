Model Arch Planning

Membership
    -slug
    -type (basic, standard, enterprise)
    -price
    -stripe payments

UserMembership
    -user (custom or default)       (foreignkey to default user)
    -stripe customer ID
    -membership type                (foreignkey to Membership)

Subscription
    -user membership
    -stripe subscription id         (foreignkey to UserMembership)
    -active

Podcasts
    -slug
    -title
    -description
    -allowed memberships            (foreignkey to Membership)

ThePodcast - Audio
    -slug
    -title
    -course                         (foreignkey to Course)
    -position
    -video
    -thumbnail
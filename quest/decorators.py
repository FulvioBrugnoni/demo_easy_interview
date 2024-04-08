from django.contrib.auth.decorators import login_required, user_passes_test

active_required = user_passes_test(lambda user: user.is_staff)


user_is_recruiter = user_passes_test(lambda u: True if u.is_recruiter() else False)


def login_active_required(f):
    decorated_f = login_required(active_required(f))
    return decorated_f

def login_recruiter_required(f):
    decorated_f = login_required(user_is_recruiter(f))
    return decorated_f

from django.contrib.auth.decorators import login_required
from django.views.generic import View


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class TestEmail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        1/0

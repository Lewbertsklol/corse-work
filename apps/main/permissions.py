from django.contrib.auth.mixins import AccessMixin


class OwnerPermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import View


# super user permission mixin class for accessing administration panel
class AdminPermission(PermissionRequiredMixin, View):
    permission_required = 'is_superuser'


# administration Home
class Home(AdminPermission, View):
    template_name = 'administration/home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


# add-member
class AddMember(AdminPermission, View):
    template_name = 'administration/add-member.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass

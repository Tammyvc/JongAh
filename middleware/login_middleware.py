from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect

loginRequired = ['/qq/settings/','/qq/edit/']

class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):
        # print(request.path)
        if request.path in loginRequired:
            username = request.session.get('user_name',None)
            if not username:
                return render(request,'account/login.html')


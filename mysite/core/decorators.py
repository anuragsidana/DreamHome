from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test




from django.core.exceptions import PermissionDenied
from .models import User,Customer,Docs


from django.shortcuts import render
def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.profile.is_admin==True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap




def user_is_valid(function):
    def wrap(request, *args, **kwargs):

        try:
           # import pdb;pdb.set_trace()
            if str(request.user.profile.id) == kwargs.get('pk', '') or request.user.profile.is_admin == True:
                ans=function(request,*args,**kwargs)
                return ans
            else:
                raise PermissionDenied
        except :
            raise PermissionDenied


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def customer_profile_access(function):
    def wrap(request,*args,**kwargs):

        id = kwargs.get('pk', '')
        customer=Customer.objects.get(id=id)

        try:
            if customer.agent.id == request.user.id or request.user.profile.is_admin == True:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except :
            raise PermissionDenied



    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def doc_access(function):
    def wrap(request,*args,**kwargs):
        # import pdb;pdb.set_trace()
        id=kwargs.get('pk','')
        doc=Docs.objects.get(id=id)
        customer=doc.customer
        try:
            if customer.agent.id == request.user.id or request.user.profile.is_admin == True:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



# def customer_docs_access(function):
#     def wrap(request, *args, **kwargs):
#         id=kwargs.get('pk','')
#         if id:
#
#
#         # import pdb;pdb.set_trace()
#         if str(request.user.profile.id)==kwargs.get('pk','') or request.user.profile.is_admin==True:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap



# def user_is_entry_author(function):
#     def wrap(request, *args, **kwargs):
#         entry = Entry.objects.get(pk=kwargs['entry_id'])
#         if entry.created_by == request.user:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
#






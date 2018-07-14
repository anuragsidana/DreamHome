from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404

from mysite.core.forms import ExecutiveSignUpForm,CustomerSignUpForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .decorators import user_is_admin, user_is_valid,customer_profile_access,doc_access
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
@user_is_admin
#view to create Executives
def signup(request):
    if request.method == 'POST':
        form = ExecutiveSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.is_admin=form.cleaned_data.get('admin')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            import pdb;pdb.set_trace()
            if(request.user.profile.is_admin==False):
              login(request, user)
            return redirect('home')
    else:
        form = ExecutiveSignUpForm()
    return render(request, 'signup.html', {'form': form})



# get default authenticate backend
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# create a function to resolve email to username
def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

from django.contrib.auth.forms import AuthenticationForm
class EmailLoginForm(AuthenticationForm):
    def clean(self):
        try:

            self.cleaned_data["username"] = User.objects.get(email=self.data["username"])
        except User.DoesNotExist:
            self.cleaned_data["username"] = "a_username_that_do_not_exists_anywhere_in_the_site"
        return super(EmailLoginForm, self).clean()



# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Profile,Customer,Docs
from django.utils.decorators import method_decorator
from django.db.models import Q

#way to apply the methpd decorators on a class based view,, here dispatch is the inbilt method of the class
decorators=[login_required,user_is_admin]


@method_decorator([login_required, user_is_valid], name='dispatch')
class ExecutiveCustomerListView(generic.ListView):
    model = Customer
    template_name = 'executive/executive_customers.html'

    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_customers'

    title = "My Customers"

    def get_queryset(self):
        # query passed in the search box
        query = self.request.GET.get("q")
        if query:
            # title changed
            self.title = "Search Results"
            return Profile.objects.filter(
                Q(customer_first_name__icontains=query) |
                Q(custoemr_last_name__icontains=query)

            )

        # import  pdb;pdb.set_trace()
        key = self.kwargs['pk']
        # if its a simple call to get all the objects then  it will return all list items in object_list variable by default
        return Customer.objects.filter(agent__id=key)

        # this is used to pass extra context data in case of generic classes

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(ExecutiveCustomerListView, self).get_context_data()

        context['page_title'] = self.title
        return context


@method_decorator(decorators,name='dispatch')
class ExecutiveListView(generic.ListView):
    model = Profile

    # redirect_field_name = 'members/index.html'
    template_name = 'executive/all_executives.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_executives'

    title="Executives"
    def get_queryset(self):
        # query passed in the search box
        query = self.request.GET.get("q")
        # if its a query then this
        if query:
            # title changed
            self.title = "Search Results"
            return Profile.objects.filter(
                Q(user_username__icontains=query) |
                Q(location__icontains=query)

            )

        # if its a simple call to get all the objects then  it will return all list items in object_list variable by default
        #return Profile.objects.exclude(is_admin=True)
        return Profile.objects.all()

        # this is used to pass extra context data in case of generic classes

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(ExecutiveListView, self).get_context_data()

        context['page_title'] = self.title
        return context


@method_decorator([login_required,user_is_valid],name='dispatch')
class ExecutiveDetailView(generic.DetailView):
    model = Profile
    template_name ='executive/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ExecutiveDetailView, self).get_context_data()
        context['user_name']=Profile.objects.get(id=self.kwargs['pk']).user.username
        return context



@method_decorator(decorators,name='dispatch')
class ExecutiveDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile

    template_name = 'core/confirm_delete.html'

    # after deletion where to redirect
    success_url = reverse_lazy('home')






#customer .............................................................................................

@method_decorator([login_required,user_is_valid], name='dispatch')
class CustomerCreateView(CreateView):
    # for which u wanna create a view
    model = Customer
    # the fields u wanna return
    fields = ['first_name', 'last_name']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(CustomerCreateView, self).get_context_data()

        context['page_title'] = 'Add a new Customer'
        return context

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.agent=Profile.objects.get(pk=self.kwargs['pk'])
        return super(CustomerCreateView, self).form_valid(form)


    # def get_initial(self):
    #     initial = super(CustomerCreateView, self).get_initial()
    #     initial['agent']= Profile.objects.get(pk=self.kwargs['pk'])
    #     profile = Profile.objects.get(pk=self.kwargs['pk'])
    #     # return {'agent': profile}
    #     return initial


# def create_customer(request):
#
#
#     if request.method == 'POST':
#         form = ExecutiveSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.profile.birth_date = form.cleaned_data.get('birth_date')
#             user.profile.is_admin = form.cleaned_data.get('admin')
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = ExecutiveSignUpForm()
#     return render(request, 'signup.html', {'form': form})
#

@method_decorator([login_required, customer_profile_access], name='dispatch')
class CustomerDocumentListView(generic.ListView):
    template_name = 'customer/customer_docs.html'
    title = "My Documents"
    context_object_name = "all_documents"

    def get_queryset(self):
        # import  pdb;pdb.set_trace()
        key = self.kwargs['pk']
        return Docs.objects.filter(customer__id=key)

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(CustomerDocumentListView, self).get_context_data()

        context['page_title'] = self.title
        return context

@method_decorator(decorators,name='dispatch')
class CustomerListView(generic.ListView):
    model = Customer

    template_name = 'customer/all_customers.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_customers'

    title="Customers"
    def get_queryset(self):
        # query passed in the search box
        query = self.request.GET.get("q")
        # if its a query then this
        if query:
            # title changed
            self.title = "Search Results"
            return Profile.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)

            )

        # if its a simple call to get all the objects then  it will return all list items in object_list variable by default
        return Customer.objects.all()

        # this is used to pass extra context data in case of generic classes

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(CustomerListView, self).get_context_data()

        context['page_title'] = self.title
        return context




@method_decorator([login_required, customer_profile_access], name='dispatch')
class CustomerDetailView(generic.DetailView):
    model = Customer
    context_object_name = "customer"
    template_name = 'customer/detail.html'

@method_decorator([login_required, customer_profile_access], name='dispatch')
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'core/confirm_delete.html'

    # after deletion where to redirect
    success_url = reverse_lazy('home')








# Documents ..........................................................


from .utils import saveToDoc
class DocumentCreateView(generic.CreateView):
    model = Docs
    template_name = 'docs/docs_form.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_customers'
    title="Create Document"
    fields = ['doc_type','doc_file']

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(DocumentCreateView, self).get_context_data()

        context['page_title'] = self.title

        return context


    def form_valid(self, form):
        docs = form.save(commit=False)
        docs.customer=Customer.objects.get(id=self.kwargs['pk'])

        form.save(commit=True)

        #add this document to doc file
        saveToDoc(self.kwargs['pk'])

        return super(DocumentCreateView, self).form_valid(form)


    #
    # def get_initial(self):
    #     cstmr=Customer.objects.get(id=self.kwargs['pk'])
    #     return {'customer':cstmr}


@method_decorator(decorators,name='dispatch')
class DocumentListView(generic.ListView):
    model = Docs
    template_name = 'docs/all_docs.html'
    title = "All Documents"
    context_object_name = "all_documents"
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            self.title = "Search Result"

            docs = Docs.objects.filter(Q(doc_type__contains=query))
            return docs
        return Docs.objects.all()

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(DocumentListView, self).get_context_data()

        context['page_title'] = self.title
        return context


@method_decorator([login_required,doc_access],name="dispatch")
class DocumentDetailView(generic.DetailView):
    model = Docs
    context_object_name = "document"
    template_name = 'docs/detail.html'


@method_decorator([login_required,doc_access],name="dispatch")
class DocumentDeleteView(DeleteView):
    model = Docs
    template_name = 'core/confirm_delete.html'
    
    # after deletion where to redirect
    success_url = reverse_lazy('home')


from django.views.generic import TemplateView


from .decorators import user_is_admin
@user_is_admin
def SignUp(request):
    return render(request,'test.html')














































#####################################################################################
from rest_framework import viewsets,generics
from .serializers import ExecutiveSerializers,CustomerSerializers
from django.views.decorators.csrf import csrf_exempt
from .models import Customer,Profile
from django.http import HttpResponse,JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from .permissions import IsAdmin




@csrf_exempt
def customer_list(request):
    if request.method=='GET':
        customers=Customer.objects.all()
        serializer=CustomerSerializers(customers,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method=='POST':
        from django.utils.six import BytesIO
        stream = BytesIO(request)
        data=JSONParser.parse(stream)
        serializer=CustomerSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors, status=400)

class ApiAgentCustomerList(generics.ListCreateAPIView):

    serializer_class = CustomerSerializers

    permission_classes = (permissions.IsAuthenticated,)

  # returns the queryset that should be used for  for list views, and that should be used as the base for lookups in detail views.Defaults to returning the queryset specified by the queryset attribute.
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        query_params=self.request.GET


        if(self.request.user.profile.is_admin==False):
            customers = Customer.objects.filter(agent__id=self.request.user.id)
        elif id in query_params:
            customers = Customer.objects.filter(agent__id=query_params['id'])
        elif all in  query_params:
            customers=Customer.objects.all()
        else:
            customers=None


        return customers

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.profile)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 100





class ApiExecutiveList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ExecutiveSerializers

    permission_classes = (permissions.IsAuthenticated,IsAdmin,)

    def get_queryset(self):
            return Profile.objects.all()

    # def perform_create(self, serializer):
    #     data=serializer.data
    #     if serializer.is_valid(raise_exception=ValueError) :
    #         serializer.create(validated_data=data)
    #         return

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 100


class ApiCustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()

    serializer_class = CustomerSerializers

    # def get_object(self):
    #     username=self.kwargs['username']
    #     return get_object_or_404(Customer,username=username)

from .serializers import UserUpdateSerialier
class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    # permission_classes = (permissions.IsAdminUser,)
    #queryset = User.objects.all()
    serializer_class = UserUpdateSerialier

    def get_object(self):
        import pdb;pdb.set_trace()
        data=self.request.POST
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)












class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class ExecutiveViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ExecutiveSerializers

from rest_framework import status
from .serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
class ApiChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model=User
    permission_classes = (permissions.IsAuthenticated,)




    def get_object(self):
        #import pdb;pdb.set_trace()
        # if(self.request.user.profile.is_admin==True)
        #     obj
        obj=self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        is_admin=self.request.user.profile.is_admin
        if(is_admin):
            self.object=User.objects.get(id=kwargs['pk'])
        else:
             self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)
        #import pdb;pdb.set_trace()

        if serializer.is_valid():
            if(not is_admin):
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request,self.object)


            return Response("Success",status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






#Creatng an endpoint for the root of our api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework.reverse import reverse

def api_root(request,format=None):
    return  JsonResponse(
        {
            'users':reverse('customer-list',request=request,format=format),
            'executives':reverse('executive-list',request=request,format=None)
        }

    )










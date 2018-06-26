from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

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
        return Profile.objects.exclude(is_admin=True)

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


@method_decorator([login_required, customer_profile_access], name='dispatch')
class DocumentCreateView(generic.CreateView):
    model = Docs
    template_name = 'docs/docs_form.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_customers'
    title="Create Document"
    fields = ['doc_type']

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(DocumentCreateView, self).get_context_data()
        # import pdb;pdb.set_trace()
        context['page_title'] = self.title
        return context


    def form_valid(self, form):
        docs = form.save(commit=False)
        docs.customer=Customer.objects.get(id=self.kwargs['pk'])
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



from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from mysite.core import views as core_views
from django.urls import reverse
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'api-customer',core_views.CustomerViewSet)
router.register(r'api-executive',core_views.ExecutiveViewSet)
urlpatterns = [


    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^emaillogin/$', auth_views.login, name="login", kwargs={'template_name': 'login.html',"authentication_form": core_views.EmailLoginForm}),

    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),

    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^sign/$',core_views.SignUp,name='sign'),
    url(r'^executive/all',core_views.ExecutiveListView.as_view(),name="executive_list"),
    url(r'^executive/(?P<pk>[0-9]+)/$',core_views.ExecutiveDetailView.as_view(),name="executive_detail"),
    url(r'^executive/(?P<pk>[0-9]+)/createCustomer$',core_views.CustomerCreateView.as_view(),name="create_customer"),
    url(r'^executive/(?P<pk>[0-9]+)/all/$', core_views.ExecutiveCustomerListView.as_view(), name="customer_list"),
    url(r'^executive/(?P<pk>[0-9]+)/delete/$', core_views.ExecutiveDeleteView.as_view(), name="executive_delete"),

    url(r'^customer/all', core_views.CustomerListView.as_view(), name="customer_list_all"),
    url(r'^customer/(?P<pk>[0-9]+)/$',core_views.CustomerDetailView.as_view(),name="customer_detail"),
    url(r'^customer/(?P<pk>[0-9]+)/createDocument$',
        core_views.DocumentCreateView.as_view(), name="create_document"),
    url(r'^customer/(?P<pk>[0-9]+)/delete$', core_views.CustomerDeleteView.as_view(), name="customer_delete"),

    url(r'^document/(?P<pk>[0-9]+)/all', core_views.CustomerDocumentListView.as_view(), name="document_list"),
    url(r'^document/(?P<pk>[0-9]+)/$', core_views.DocumentDetailView.as_view(), name="document_detail"),
    url(r'^document/all', core_views.DocumentListView.as_view(), name="document_list_all"),
    url(r'^document/(?P<pk>[0-9]+)/delete$', core_views.DocumentDeleteView.as_view(), name="document_delete"),


    url('^', include('django.contrib.auth.urls')),




    #########################
    url(r'^ar$', core_views.customer_list,name='api_add_customer'),

    url(r'^api/customer/$', core_views.ApiAgentCustomerList.as_view(),name='customer-list'),
    url(r'^api/executives', core_views.ApiExecutiveList.as_view(),name='executive-list'),
    url(r'api/customer_detail/(?P<pk>[0-9]+)$', core_views.ApiCustomerDetailView.as_view(), name='customer-detail'),
    url(r'api/user_update/(?P<username>[a-zA-Z]+)/$',core_views.UserUpdateAPIView.as_view()),
    url(r'^', include(router.urls)),
    url(r'api/change_password/(?P<pk>[0-9]+)$',core_views.ApiChangePasswordView.as_view(),name='api-changePassword'),

    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^root$',core_views.api_root,name='api-root')








]

# urlpatterns=format_suffix_patterns(urlpatterns)
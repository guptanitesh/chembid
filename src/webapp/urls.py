from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from webapp import views as core_views



urlpatterns = [

    url(r'^$', core_views.homepage, name='homepage'),
	url(r'^$',views.homepage, name='homepage'),
	url(r'^products/$', views.product_list, name='product_list'),
	url(r'^product/(?P<pk>\d+)/$',views.product_detail, name='product_detail'),
	url(r'^product/new/$', views.product_new, name='product_new'),
	url(r'^product/(?P<pk>\d+)/edit/$', views.product_edit, name='product_edit'),

	url(r'^login/$', auth_views.login, {'template_name': 'webapp/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),

	url(r'^mainproducts/$', views.mainproduct_list, name='mainproduct_list'),
	url(r'^mainproduct/new/$', views.mainproduct_new, name='mainproduct_new'),
	url(r'^mainproduct/(?P<pk>\d+)/edit/$', views.mainproduct_edit, name='mainproduct_edit'),
	url(r'^mainproduct/(?P<pk>\d+)/$',views.mainproduct_detail, name='mainproduct_detail'),
	url(r'^search/(?P<name>[A-z ]+)/$', views.search, name='search'),
	
	url(r'^impurities/$', views.impurity_list, name='impurity_list'),
	url(r'^impurities/(?P<pk>\d+)$', views.impurity_detail, name='impurity_detail'),
	url(r'^impurity/new/$', views.impurity_new, name='impurity_new'),
		
	url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),

    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),

	url(r'^productavailabilities/$', views.productavailability_list, name='productavailability_list'),
	url(r'^productavailability/(?P<pk>\d+)/$',views.productavailability_detail, name='productavailability_detail'),
	url(r'^productavailability/new/(?P<pk>\d+)$', views.productavailability_new, name='productavailability_new'),
	url(r'^productavailability/(?P<pk>\d+)/edit/$', views.productavailability_edit, name='productavailability_edit'),

	url(r'^impurityavailabilities/$', views.impurityavailability_list, name='impurityavailability_list'),
	url(r'^impurityavailability/(?P<pk>\d+)/$',views.impurityavailability_detail, name='impurityavailability_detail'),
	url(r'^impurityavailability/new/(?P<pk>\d+)$', views.impurityavailability_new, name='impurityavailability_new'),
	url(r'^impurityavailability/(?P<pk>\d+)/edit/$', views.impurityavailability_edit, name='impurityavailability_edit'),

]
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Product,impurity
from .models import Mainproduct
from .models import ProductAvailability
from .models import ImpurityAvailability
from .models import Api
from .forms import ProductForm
from .forms import MainproductForm
from .forms import ImpurityAvailabilityForm
from .forms import ProductAvailabilityForm
from .forms import ApiForm,ImpurityForm
from taggit.models import Tag
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from webapp.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.contrib import messages
import json
import urllib
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
import django_excel as excel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Need to create functions for adding mainproducts through admin site

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            
            if result['success']:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.profile.email = form.cleaned_data.get('email')
                user.profile.company_name = form.cleaned_data.get('company_name')
                user.profile.company_type = form.cleaned_data.get('company_type')
                user.profile.phone_no = form.cleaned_data.get('phone_no')
                
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your Chembid Account'
                message = render_to_string('webapp/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            
            return render(request, 'webapp/account_activation_sent.html')
    else:   
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'webapp/home.html')
        # return render(request, 'webapp/base.html')
    else:
        return render(request, 'webapp/account_activation_invalid.html')



def account_activation_sent(request):
    return render(request, 'webapp/account_activation_sent.html')


def homepage(request):
    return render(request, 'webapp/home.html')


def product_list(request):
    products = Product.objects.filter(added_date__lte=timezone.now()).order_by('added_date')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render(request, 'webapp/product_list.html', {'products': products})


def product_detail(request, pk):
	product = get_object_or_404(Product, pk=pk)
	return render(request, 'webapp/product_detail.html', {'product' : product})

@login_required
def product_new(request):
    # print(request.user.profile.email_confirmed)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.added_date = timezone.now()
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'webapp/product_edit.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.added_date = timezone.now()
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'webapp/product_edit.html', {'form': form})



def mainproduct_list(request):
    mainproducts = Mainproduct.objects.filter(added_date__lte=timezone.now()).order_by('added_date')
    paginator = Paginator(mainproducts, 3)
    page = request.GET.get('page')
    try:
        mainproducts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mainproducts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        mainproducts = paginator.page(paginator.num_pages)
    # return render(request, 'webapp/product_list.html', {'products': products})

    return render(request, 'webapp/mainproduct_list.html', {'mainproducts': mainproducts})


def mainproduct_new(request):
    if request.method == "POST":
        form = MainproductForm(request.POST)
        if form.is_valid():
            mainproduct = form.save(commit=False)
            mainproduct.added_date = timezone.now()
            mainproduct.save()
            components = mainproduct.components.split(",")
            for i in components:
                print(i)
                api = Api(name= str(i.strip()), mainproduct=mainproduct)
                api.save()
            return redirect('mainproduct_detail', pk=mainproduct.pk)
    else:
        form = MainproductForm()
    return render(request, 'webapp/mainproduct_edit.html', {'form': form})

# May not work
def mainproduct_edit(request, pk):
    mainproduct = get_object_or_404(Mainproduct, pk=pk)
    if request.method == "POST":
        form = MainproductForm(request.POST, instance=mainproduct)
        if form.is_valid():
            mainproduct = form.save(commit=False)
            mainproduct.added_date = timezone.now()
            mainproduct.save()
            return redirect('mainproduct_detail', pk=product.pk)
    else:
        form = MainproductForm(instance=mainproduct)
    return render(request, 'webapp/mainproduct_edit.html', {'form': form})


def mainproduct_detail(request, pk):
    mainproduct = get_object_or_404(Mainproduct, pk=pk)
    return render(request, 'webapp/mainproduct_detail.html', {'mainproduct' : mainproduct})

@login_required
def search(request, name):
    print(name)
    apis = Api.objects.filter(name__contains=name)
    return render(request, 'webapp/search_list.html', {'apis' : apis})

def impurity_list(request):
    impurities = impurity.objects.all()
    paginator = Paginator(impurities, 3)
    page = request.GET.get('page')
    try:
        impurities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        impurities = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        impurities = paginator.page(paginator.num_pages)

    return render(request, 'webapp/impurity_list.html', {'impurities': impurities})

def impurity_detail(request,pk):
    impurit=get_object_or_404(impurity,pk=pk)
    return render(request,'webapp/impurity_detail.html', {'impurity':impurit})

def impurity_new(request):
    if request.method == "POST":
        form = ImpurityForm(request.POST)
        if form.is_valid():
            impurity = form.save(commit=False)
            impurity.added_date = timezone.now()
            
            impurity.save()
            return redirect('impurity_detail', pk=impurity.pk)
    else:
        form = ImpurityForm()
    return render(request, 'webapp/impurity_edit.html', {'form': form})


class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            record = filehandle.get_dict()
            list1 = record['Product Name']
            list2 = record['Composition']
            length = len(list2)
            for i in range(length):
                mainproduct = Mainproduct(name = list1[i], components = list2[i])
                mainproduct.added_date = timezone.now()
                mainproduct.save()

                components = list2[i].split(",")
                for j in components:
                    api = Api(name= str(j.strip()), mainproduct=mainproduct)
                    api.save()
            return render(request, 'webapp/home.html')
            # return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, 'webapp/upload_form.html', {'form': form})


def productavailability_list(request):
    productavailabilities = ProductAvailability.objects.filter(added_date__lte=timezone.now()).order_by('added_date')
    return render(request, 'webapp/productavailability_list.html', {'productavailabilities': productavailabilities})


def productavailability_detail(request, pk):
    productavailability = get_object_or_404(ProductAvailability, pk=pk)
    return render(request, 'webapp/productavailability_detail.html', {'productavailability' : productavailability})

@login_required
def productavailability_new(request, pk):
    # print(request.user.profile.email_confirmed)
    product = get_object_or_404(Product, pk=pk)

    productavailability = ProductAvailability(name = request.user.username, email = request.user.profile.email, company_name = request.user.profile.company_name,
        phone_no = request.user.profile.phone_no, product_name = product.name, Cas = product.Cas, grade = product.grade, quantity = product.quantity, added_date = timezone.now())

    productavailability.save()
    return render(request, 'webapp/product_detail.html', {'product' : product})
    # return redirect('productavailability_detail', pk=productavailability.pk)


@login_required
def productavailability_edit(request, pk):
    productavailability = get_object_or_404(ProductAvailability, pk=pk)
    if request.method == "POST":
        form = ProductAvailabilityForm(request.POST, instance=productavailability)
        if form.is_valid():
            productavailability = form.save(commit=False)
            productavailability.added_date = timezone.now()
            productavailability.save()
            return redirect('productavailability_detail', pk=productavailability.pk)
    else:
        form = ProductAvailabilityForm(instance=productavailability)
    return render(request, 'webapp/productavailability_edit.html', {'form': form})


def impurityavailability_list(request):
    impurityavailabilities = ImpurityAvailability.objects.filter(added_date__lte=timezone.now()).order_by('added_date')
    return render(request, 'webapp/impurityavailability_list.html', {'impurityavailabilities': impurityavailabilities})


def impurityavailability_detail(request, pk):
    impurityavailability = get_object_or_404(ImpurityAvailability, pk=pk)
    return render(request, 'webapp/impurityavailability_detail.html', {'impurityavailability' : impurityavailability})

@login_required
def impurityavailability_new(request, pk):
    # print(request.user.profile.email_confirmed)
    imp = get_object_or_404(impurity, pk=pk)

    impurityavailability = ImpurityAvailability(name = request.user.username, email = request.user.profile.email, company_name = request.user.profile.company_name,
        phone_no = request.user.profile.phone_no, impurity_name = imp.name, Cas = imp.Cas, grade = imp.grade, quantity = imp.quantity, added_date = timezone.now())

    impurityavailability.save()
    return render(request, 'webapp/impurity_detail.html', {'impurity' : imp})
    # return redirect('impurityavailability_detail', pk=impurityavailability.pk)


@login_required
def impurityavailability_edit(request, pk):
    impurityavailability = get_object_or_404(ImpurityAvailability, pk=pk)
    if request.method == "POST":
        form = ImpurityAvailabilityForm(request.POST, instance=impurityavailability)
        if form.is_valid():
            impurityavailability = form.save(commit=False)
            impurityavailability.added_date = timezone.now()
            impurityavailability.save()
            return redirect('impurityavailability_detail', pk=impurityavailability.pk)
    else:
        form = ImpurityAvailabilityForm(instance=impurityavailability)
    return render(request, 'webapp/impurityavailability_edit.html', {'form': form})


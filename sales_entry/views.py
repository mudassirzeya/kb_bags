from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, SalesEntryData
from django.contrib import messages
from datetime import datetime
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            staffProfile = UserProfile.objects.get(user=user)
            if staffProfile.user_status == 'Active':
                login(request, user)
                if staffProfile.is_super_admin:
                    return redirect('sales_report_page')
                else:
                    return redirect('/')
            else:
                messages.warning(request, 'You don\'t have access to login')
        else:
            messages.info(request, 'Username or Password is in correct')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('user_login')


@login_required(login_url='user_login')
def sales_entry_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    if staffProfile.is_super_admin and not staffProfile.user.is_superuser:
        return redirect('sales_report_page')
    if request.method == 'POST':
        if 'save_new_sales_data' in request.POST:
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')
            product_quantity = request.POST.get('product_quantity')
            payment_type = request.POST.get('payment_type')
            if 'product_image' in request.FILES:
                product_image = request.FILES["product_image"]
            else:
                product_image = None
            SalesEntryData.objects.create(
                staff=staffProfile,
                product_name=product_name,
                product_quantity=product_quantity,
                product_price=product_price,
                payment_type=payment_type,
                product_image=product_image
            )
            messages.info(request, "Successfully Added!!")
        return redirect('sales_entry_page')
    context = {'staffProfile': staffProfile}
    return render(request, 'sales_entry_page.html', context)


@login_required(login_url='user_login')
def sales_report_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    today_date = datetime.today().date()
    selling_date = request.GET.get('selling_date')
    if not selling_date:
        url_with_today_date = f"/sales_report_page/?selling_date={today_date}"
        return redirect(url_with_today_date)

    this_date_sales_list = []
    this_day_total_sale = 0
    this_day_total_sale_in_cash = 0
    this_day_total_sale_in_online = 0
    if selling_date:
        sales_data = SalesEntryData.objects.filter(added_date=selling_date)
        for each_data in sales_data:
            temp = {}
            temp['id'] = each_data.id
            temp['added_by'] = each_data.staff.user.username
            temp['product_name'] = each_data.product_name
            temp['quantity'] = each_data.product_quantity
            temp['price'] = each_data.product_price
            temp['total_price'] = int(
                each_data.product_price) * int(each_data.product_quantity)
            temp['payment_type'] = each_data.payment_type
            try:
                temp['image'] = each_data.product_image.url
            except Exception:
                temp['image'] = None
            this_day_total_sale += temp['total_price']
            if temp['payment_type'] == 'Cash':
                this_day_total_sale_in_cash += temp['total_price']
            if temp['payment_type'] == 'Online':
                this_day_total_sale_in_online += temp['total_price']
            this_date_sales_list.append(temp)
    context = {'sales_data': this_date_sales_list,
               'staffProfile': staffProfile,
               'selling_date': selling_date,
               'this_date_sales_list': this_date_sales_list,
               'this_day_total_sale': this_day_total_sale,
               'this_day_total_sale_in_online': this_day_total_sale_in_online,
               'this_day_total_sale_in_cash': this_day_total_sale_in_cash}
    return render(request, 'report_page.html', context)

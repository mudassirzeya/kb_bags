from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, SalesEntryData
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from datetime import date
import json
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
            today_date = date.today()
            # if 'product_image' in request.FILES:
            #     product_image = request.FILES["product_image"]
            # else:
            #     product_image = None
            SalesEntryData.objects.create(
                staff=staffProfile,
                product_name=product_name,
                product_quantity=product_quantity,
                product_price=product_price,
                payment_type=payment_type,
                added_date=today_date
                # product_image=product_image
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
    from_selling_date = request.GET.get('from_selling_date')
    to_selling_date = request.GET.get('to_selling_date')
    if not from_selling_date:
        from_selling_date = today_date
    if not to_selling_date:
        to_selling_date = from_selling_date

    if request.GET.get('from_selling_date') is None:
        url_with_today_date = f"/sales_report_page/?from_selling_date={from_selling_date}"
        if to_selling_date:
            url_with_today_date += f"&to_selling_date={to_selling_date}"
        return redirect(url_with_today_date)

    this_date_sales_list = []
    this_day_total_sale = 0
    this_day_total_sale_in_cash = 0
    this_day_total_sale_in_online = 0

    sales_data = SalesEntryData.objects.filter(
        added_date__gte=from_selling_date, added_date__lte=to_selling_date)

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
        # try:
        #     temp['image'] = each_data.product_image.url
        # except Exception:
        #     temp['image'] = None
        this_day_total_sale += temp['total_price']
        if temp['payment_type'] == 'Cash':
            this_day_total_sale_in_cash += temp['total_price']
        if temp['payment_type'] == 'Online':
            this_day_total_sale_in_online += temp['total_price']
        this_date_sales_list.append(temp)
    if request.method == 'POST':
        if 'edit_existing_sales_data' in request.POST:
            sales_data_id = request.POST.get('sales_data_pk')
            product_name = request.POST.get('edit_product_name')
            product_price = request.POST.get('edit_product_price')
            product_quantity = request.POST.get('edit_product_quantity')
            payment_type = request.POST.get('edit_payment_type')
            # if 'edit_product_image' in request.FILES:
            #     product_image = request.FILES["edit_product_image"]
            # else:
            #     product_image = None

            try:
                sales_data = SalesEntryData.objects.get(id=int(sales_data_id))
            except Exception:
                sales_data = None
            if sales_data:
                sales_data.product_name = product_name
                sales_data.product_price = product_price
                sales_data.product_quantity = product_quantity
                sales_data.payment_type = payment_type
                # if product_image:
                #     sales_data.product_image = product_image
                sales_data.save()
                messages.info(request, "Successfully Edited!!")
        if 'delete_sales_data' in request.POST:
            sales_data_id = request.POST.get('delete_sales_data_pk')
            try:
                sales_data = SalesEntryData.objects.get(id=int(sales_data_id))
            except Exception:
                sales_data = None
            if sales_data:
                sales_data.delete()
        if from_selling_date:
            url_with_date_parameter = f"/sales_report_page/?from_selling_date={from_selling_date}"
            if to_selling_date:
                url_with_date_parameter += f"&to_selling_date={to_selling_date}"
            return redirect(url_with_date_parameter)
        else:
            return redirect('sales_report_page')

    context = {'sales_data': this_date_sales_list,
               'staffProfile': staffProfile,
               'from_selling_date': from_selling_date,
               'to_selling_date': to_selling_date,
               'this_date_sales_list': this_date_sales_list,
               'this_day_total_sale': this_day_total_sale,
               'this_day_total_sale_in_online': this_day_total_sale_in_online,
               'this_day_total_sale_in_cash': this_day_total_sale_in_cash}
    return render(request, 'report_page.html', context)


def get_sales_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        got_query = data['data_obj']
        # print("data", got_query)
        try:
            sales_query = SalesEntryData.objects.get(
                id=int(got_query))
        except Exception:
            sales_query = None

        audit_json = serializers.serialize('json', [sales_query])
        return JsonResponse({"msg": "success",
                            "sales_data_json": json.loads(audit_json)})

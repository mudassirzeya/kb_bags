from django.urls import path
from .views import login_page, logout_user, sales_entry_page, sales_report_page, get_sales_data
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('user_login/', login_page, name='user_login'),
    path('user_logout/', logout_user, name='user_logout'),
    path('', sales_entry_page, name='sales_entry_page'),
    path('sales_report_page/', sales_report_page, name='sales_report_page'),
    path('get_sales_data/', get_sales_data, name='get_sales_data'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

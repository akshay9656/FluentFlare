from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('signOut/', views.signOut, name='signOut'),
    path('paymentDecisionPage/', views.paymentDecisionPage, name='paymentDecisionPage'),
    path('paymentpage/', views.paymentpage, name='paymentpage'),
    path('UserHome/', views.UserHome, name='UserHome'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('GrammerPage/', views.GrammerPage, name='GrammerPage'),
    path('FirstTask/', views.FirstTask, name='FirstTask'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('taskpage/<int:id>/', views.taskpage, name='taskpage'),
    path('myadminpage/', views.myadminpage, name='myadminpage'),
    path('addtask/', views.addtask, name='addtask'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('termsofservice/', views.termsofservice, name='termsofservice'),
    path('changepayment/', views.changepayment, name='changepayment'),
    path('changegrouplink/', views.changegrouplink, name='changegrouplink'),
    path('allusers/', views.allusers, name='allusers'),
    path('lastmonthusers/', views.lastmonthusers, name='lastmonthusers'),
    path('enrolledusers/', views.enrolledusers, name='enrolledusers'),
    path('notenrolledusers/', views.notenrolledusers, name='notenrolledusers'),
    path('newmessages/', views.newmessages, name='newmessages'),
    path('promoter_dashboard/<str:promoter_username>/', views.promoter_dashboard, name='promoter_dashboard'),
    path('showpromoters/', views.showpromoters, name='showpromoters'),
    path('changemessagestatus/<int:id>/', views.changemessagestatus, name='changemessagestatus'),
    path('toggle-admin/<int:id>/', views.toggle_admin_status, name='toggle_admin_status'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle-promoter-status/<int:user_id>/', views.toggle_promoter_status, name='toggle_promoter_status'),
   
]

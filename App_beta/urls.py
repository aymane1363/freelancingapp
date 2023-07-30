from django.urls import path, reverse_lazy
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name="App_beta"
urlpatterns = [
    path('', views.home.as_view(), name='all'),
    path('freelancer_home/', views.FreelancerHome, name='freelancer_home'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='service_detail'),
    path('freelancer_space/', views.FreelancerSpace, name='freelancer_space'),
    path('freelancer_proposals/', views.FreelancerProposals, name='freelancer_proposals'),
    path('freelancer_services/', views.FreelancerServices.as_view(), name='freelancer_services'),
    path('client_space/', views.ClientSpace, name='client_space'),
    # path('main/create/', views.FreelancerCreate.as_view(), name='freelancer_create'),
    path('freelancer/create',views.FreelancerCreateView.as_view(success_url=reverse_lazy('App_beta:all')), name='freelancer_create'),
    path('apply_service/<int:pk>/', views.ProjectCreateView.as_view(), name='apply_service'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
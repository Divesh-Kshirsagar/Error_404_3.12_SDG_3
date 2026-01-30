from django.urls import path
from .views import IntakeView, DashboardView, QueuePartialView, TokenView

app_name = 'clinic'

urlpatterns = [
    path('', IntakeView.as_view(), name='intake'),
    path('token/<int:case_id>/', TokenView.as_view(), name='token'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/queue-update/', QueuePartialView.as_view(), name='queue_update'),
]

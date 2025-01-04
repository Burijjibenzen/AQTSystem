from django.urls import path
from .views import RegisterView, LoginView, AdviceView, QueryDataView, SaveQueryRecordsView, QueryAnalysisView, GetStationsLocationView, PasswordResetView, QueryRecordView, DataDetailsView, DeleteRecordView, AdviceListView, StationListView, IndicatorListView, DataCreateView, StationManagementView, AnalysisCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('advice/', AdviceView.as_view(), name='submit_advice'),
    path('query-data/', QueryDataView.as_view(), name='query-data'),
    path('save-query-records/', SaveQueryRecordsView.as_view(), name='save_query_records'),
    path('query-analysis/', QueryAnalysisView.as_view(), name='query_analysis'),
    path('get-stations-location/', GetStationsLocationView.as_view(), name='get-stations-location'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('query-records/', QueryRecordView.as_view(), name='query-records'),
    path('data-details/', DataDetailsView.as_view(), name='data-details'),
    path('delete-record/', DeleteRecordView.as_view(), name='delete-record'),
    path('advices/', AdviceListView.as_view(), name='advice-list'),
    path("stations/", StationListView.as_view(), name="station-list"),
    path("indicators/", IndicatorListView.as_view(), name="indicator-list"),
    path("data/", DataCreateView.as_view(), name="data-create"),
    path('all-stations/', StationManagementView.as_view(), name='station-management-list'),
    path('station-management/', StationManagementView.as_view(), name='station-management'),
    path('analysis/', AnalysisCreateView.as_view(), name='analysis-create'),
]
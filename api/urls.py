from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    ClientCreate,
    ClientUpdateDestroy,
    DistributionCreate,
    DistributionDetailedStatisticsView,
    DistributionGeneralStatisticsView,
    DistributionUpdateDestroy,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view()),
    path(
        "clients/",
        include(
            [
                path("", ClientCreate.as_view()),
                path("<int:pk>", ClientUpdateDestroy.as_view()),
            ]
        ),
    ),
    path(
        "distributions/",
        include(
            [
                path("", DistributionCreate.as_view()),
                path("<int:pk>", DistributionUpdateDestroy.as_view()),
            ]
        ),
    ),
    path(
        "statistics/",
        include(
            [
                path("general", DistributionGeneralStatisticsView.as_view()),
                path(
                    "detailed/<int:pk>",
                    DistributionDetailedStatisticsView.as_view(),
                ),
            ]
        ),
    ),
]

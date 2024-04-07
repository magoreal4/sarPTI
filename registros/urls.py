from django.urls import path
from .views import (
    LoginAPIView,
    RegistroLlegadaList,
    RegistroLocalidadList,
    RegistroPropietarioList,
    RegistroPropiedadList,
    RegistroSitioList,
    RegistroSitioImagenesList,
    RegistioElectricoList
    )

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/registrollegada/', RegistroLlegadaList.as_view(), name='registrollegada'),
    path('api/registrolocalidad/', RegistroLocalidadList.as_view(), name='registrolocalidad'),
    path('api/registropropietario/', RegistroPropietarioList.as_view(), name='registropropietario'),
    path('api/registropropiedad/', RegistroPropiedadList.as_view(), name='registropropiedad'),
    path('api/registrositio/', RegistroSitioList.as_view(), name='registrositio'),
    path('api/registrositioimagen/', RegistroSitioImagenesList.as_view(), name='registrositioimagen'),
    path('api/registroelectrico/', RegistioElectricoList.as_view(), name='registroelectrico'),
]

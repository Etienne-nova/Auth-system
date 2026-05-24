from django.urls import path, include

#from apps.authentication.api.v1.routes import auth_urls


urlpatterns = [

    path(
        'auth/',
        include(
           'apps.authentication.api.v1.routes.auth_urls'
        )
    ),
]
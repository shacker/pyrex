from django.conf.urls import url
from django.contrib import admin

from itl import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^albums/$', views.AlbumListView.as_view(), name='albums'),
    url(r'^albums/(?P<pk>\d+)$', views.AlbumDetailView.as_view(), name='album_detail'),

    url(r'^artists/$', views.ArtistListView.as_view(), name='artists'),
    url(r'^artists/(?P<pk>\d+)$', views.ArtistDetailView.as_view(), name='artist_detail'),

    url(r'^tracks/$', views.TrackListView.as_view(), name='tracks'),
    url(r'^tracks/(?P<pk>\w+)$', views.TrackDetailView.as_view(), name='track_detail'),

    url(r'^kinds/$', views.KindListView.as_view(), name='kinds'),
    url(r'^kinds/(?P<pk>\d+)$', views.KindDetailView.as_view(), name='kind_detail'),

    url(r'^admin/', admin.site.urls),
]

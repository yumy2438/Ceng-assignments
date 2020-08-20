from django.conf.urls import include, url

from project import views

urlpatterns = [
    url(r'^$', views.log),
    url(r'^home$', views.home),
    url(r'^lookup$', views.lookup),
    url(r'^chooseitem$', views.chooseitem),
    url(r'^additem$', views.additem),
    url(r'^borrowedby$', views.borrowedby),
    url(r'^setfriend$', views.setfriend),
    url(r'^listitems$', views.listitems),
    url(r'^friend', views.friend),
    url(r'^changepassword', views.changepassword),
    url(r'^watchuser', views.watchuser),
    url(r'^logout$', views.logout1),
    url(r'^getnotifs$', views.getnotifs),
    url(r'^item$', views.itemhtml),
    url(r'^returned$', views.returned),
    url(r'^borrowedreq$', views.borrowedreq),
    url(r'^comment$', views.comment),
    url(r'^commentlist$', views.commentlist),
    url(r'^getrating$', views.getrating),
    url(r'^rate$', views.rate),
    url(r'^setstate$', views.setstate),
    url(r'^locate$', views.locate),
    url(r'^announce$', views.announce),
    url(r'^view$', views.view),
    url(r'^detail$', views.detail),
    url(r'^delete$', views.delete),
    url(r'^watchitem$', views.watchitem),
    url(r'^search$', views.search),
]

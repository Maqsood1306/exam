from django.conf.urls import url
from .views import index,log,admin,logout_view,addstud,modify,confirm,marks,studmark,resultgen,hallgen,rev,pho,addnot
from .userviews import userlog,userregister,home,results,phot,revals,resultpdf,userhall,user_logout_view

app_name = 'examcell'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^adminlog/$', log, name='login'),
    url(r'^adminsite/$', admin, name='admin'),
    url(r'^adminout/$', logout_view, name='logout'),
    url(r'^add/$', addstud, name='addstud'),
    url(r'^modify/$', modify, name='modify'),
    url(r'^confirm/$', confirm, name='confirm'),
    url(r'^addmark/$', marks, name='marks'),
    url(r'^studmark/$', studmark, name='studmark'),
    url(r'^resultgen/$', resultgen, name='resultgen'),
    url(r'^hallgen/$', hallgen, name='hallgen'),
    url(r'^rev/$', rev, name='rev'),
    url(r'^photo/$', pho, name='pho'),
    url(r'^adnot/$', addnot, name='adnot'),

    url(r'^userlogin/$', userlog, name='userlogin'),
    url(r'^userlogout/$', user_logout_view, name='userlogout'),
    url(r'^userregister/$', userregister, name='userregister'),
    url(r'^student/$', home, name='home'),
    url(r'^results/$', results, name='results'),
    url(r'^phot/$', phot, name='phot'),
    url(r'^revals/$', revals, name='reval'),
    url(r'^resultpdf/$', resultpdf, name='resultpdf'),
    url(r'^hallpdf/$', userhall, name='hallpdf'),


]
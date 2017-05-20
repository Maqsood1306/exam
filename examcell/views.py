from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, render_to_response
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout,user_logged_in,get_user
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import stud_id, student, dept, subject, result, hallticket,nc_student,reval,photo,notice
from django.utils import timezone
from django.db.models import Q
from itertools import chain
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#
# def cal(self, a):
#     if a >= 80:
#         return 10
#     elif a < 80 and a >= 75:
#         return 9
#     elif a < 75 and a >= 70:
#         return 8
#     elif a < 70 and a >= 60:
#         return 7
#     elif a < 60 and a >= 50:
#         return 6
#     elif a < 50 and a >= 45:
#         return 5
#     elif a < 45 and a >= 40:
#         return 4
#     else:
#         pass
#     return 0
#
# def grade(self):
#     thc = subject.objects.get(sb_code=self.sb_code).theory_credit
#     twc = subject.objects.get(sb_code=self.sb_code).tw_prc_credit
#     t1 = subject.objects.get(sb_code=self.sb_code).test1
#     t2 = subject.objects.get(sb_code=self.sb_code).test2
#     th_m = subject.objects.get(sb_code=self.sb_code).sem +((t1+t2)/2)
#     tw_m = subject.objects.get(sb_code=self.sb_code).oral + subject.objects.get(sb_code=self.sb_code).tw
#     thper = ((((self.test1m + self.test2m)/2 ) +self.semm))/th_m*100
#     twper = (self.oralm+self.twm)/tw_m*100
#     thgrade = self.cal(thper)*thc
#     twgrade = self.cal(twper)*twc
#     return thgrade + twgrade



# Create your views here.
def index(request):
    return render(request, 'examcell/index.html',{})



#@login_required(login_url='examcell:login')
def log(request):
    if request.method=='POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('examcell:admin')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'examcell/login.html', {'msg' : 'login Fails'})
    return render(request, 'examcell/login.html')


def logout_view(request):
    logout(request)
    return redirect('examcell:index')


@staff_member_required(login_url='examcell:login')
def admin(request):
    s = get_user(request)
    ts = student.objects.all().count()
    tr = reval.objects.all().count()
    tp = photo.objects.all().count()
    tc = nc_student.objects.all().count()
    n = notice.objects.all().order_by('-time')
    return render(request,'examcell/admin.html',{'s':s,'ts':ts,'tr':tr,'tp':tp,'tc':tc,'n':n})


@staff_member_required(login_url='examcell:login')
def addstud(request):
    if request.method =='POST':
        s = stud_id.objects.filter(studid=request.POST['sid'])
        if not s:
            id = request.POST['sid']
            name = request.POST['name']
            s = stud_id(studid=id, studname=name)
            email = request.POST['email']
            su = 'Congratulation! %s you are Successfully Added' % (s.studname)
            message = 'Hi %s\nyou have assigned a rollno i.e "%s" now you have register yourself using this rollno\n and also confirm you details'%(s.studname,s.studid)
            from_email = 'noreply@examcell.com'
            to_list = [email, settings.EMAIL_HOST_USER]
            send_mail(su, message, from_email, to_list, fail_silently=True)
            s.save()
            return render(request,'ExamCell/addstud.html', {'msg':'Student Added Successfully', 'std': stud_id.objects.all()})
        return render(request, 'ExamCell/addstud.html', {'msg': 'Student already Exist', 'std': stud_id.objects.all()})
    else:
        return render(request, 'ExamCell/addstud.html',{ 'std': stud_id.objects.all()})


@staff_member_required(login_url='examcell:login')
def modify(request):
    if request.method=='POST':
        if request.POST['flag']=='1':
            try:
                s = student.objects.get(sid=request.POST['sid'])
                if s:
                    return render(request, 'examcell/modify.html', {'stud': s, 'dept': dept.objects.all()})
                else:
                    return render(request, 'examcell/modify.html', {'msg': 'Student does not exist'})
            except ObjectDoesNotExist:
                return render(request, 'examcell/modify.html', {'msg': 'Incorrect Student id'})
        else:
            try:
                s = student.objects.get(sid=request.POST['sid'])
                s.s_fname = request.POST['fname']
                s.s_mname = request.POST['mname']
                s.s_lname = request.POST['lname']
                s.s_email = request.POST['email']
                #s.s_image = request.POST['pic']
                #s.s_password = request.POST['pwd']
                s.s_contact = request.POST['cont']
                s.dname = dept.objects.get(dname=request.POST['dname'])
                s.s_gender = request.POST['gender']
                s.save()
                return render(request, 'ExamCell/modify.html', {'msg': 'successfully updated'})
            except ObjectDoesNotExist:
                return render(request, 'examcell/modify.html', {'msg': 'Incorrect Student id'})
    else:
        return render(request,'examcell/modify.html',{})


@staff_member_required(login_url='examcell:login')
def confirm(request):
    if request.method=='POST':
        if request.POST['flag']=='2':
            try:
                stud = student.objects.get(sid=request.POST['sid'])
                return render(request, 'ExamCell/confirm.html', {'msg': 'Student Already Comfirmed','nc':nc_student.objects.all()})
            except ObjectDoesNotExist:
                try:
                    s = nc_student.objects.get(sid=request.POST['sid'])
                    return render(request, 'examcell/confirm.html', {'stud': s, 'dept': dept.objects.all(),'nc':nc_student.objects.all()})
                except ObjectDoesNotExist:
                    return render(request, 'examcell/confirm.html', {'msg': 'No Such Id is assigned','nc':nc_student.objects.all()})
        else:
            try:
                ns = nc_student.objects.get(sid=request.POST['sid'])
                s =  student(sid=ns.sid,
                            s_fname=ns.s_fname,
                            s_mname=ns.s_mname,
                            s_lname=ns.s_lname,
                            s_image=ns.s_image,
                            s_email=ns.s_email,
                            s_password=ns.s_password,
                            s_address=ns.s_address,
                            s_contact=ns.s_contact,
                            dname=ns.dname,
                            s_gender=ns.s_gender)
                s.save()

                s  = 'Congratulation! %s have Confirmed your Details'%(s.s_fname)
                message = 'Hi %s\nYou have confirmed you Details now you can login with your rollno and password and can take benefit of E-Exam Cell System'
                from_email = settings.EMAIL_HOST_USER
                to_list = [ns.s_email,settings.EMAIL_HOST_USER]
                send_mail(s, message, from_email, to_list, fail_silently=True)
                ns.delete()
                return render(request, 'ExamCell/confirm.html', {'msg': 'Student Record comfirmed','nc':nc_student.objects.all()})
            except ObjectDoesNotExist :
                return render(request, 'examcell/confirm.html', {'msg': 'No Such Id is assigned','nc':nc_student.objects.all()})
    else:
        return render(request, 'examcell/confirm.html', {'nc':nc_student.objects.all()})


@staff_member_required(login_url='examcell:login')
def marks(request):
    if request.method=='POST':
        if request.POST['flag']=='1':
            branch = request.POST['dname']
            sem = request.POST['sem']
            sub = subject.objects.filter(dname=branch,sem_no=sem)
            context={
                'sub': sub,
                'pdname': branch,
                'psem': sem,
                'dept': dept.objects.all(),
                'sem': [1, 2, 3, 4, 5, 6, 7, 8]
            }
            return render(request,'examcell/addmark.html',context)
        elif request.POST['flag']=='2':
            branch = request.POST['dname']
            sem = request.POST['sem']
            psub = request.POST['sub']
            sub = subject.objects.filter(dname=branch, sem_no=sem)
            s = subject.objects.filter(sb_name=psub).values('test1','test2','sem','tw','oral')
            subp = []
            for key,value in s[0].items():
                if value!=0:
                    subp.append(key)
            context={
                'exam':subp,
                'pdname':branch,
                'psem':sem,
                'psub':psub,
                'sub':sub,
                'dept':dept.objects.all(),
                'sem':[1, 2, 3, 4, 5, 6, 7, 8]}
            return render(request,'examcell/addmark.html',context)
        elif request.POST['flag']=='3':
            branch = request.POST['dname']
            sem = request.POST['sem']
            psub = request.POST['sub']
            exam = request.POST['exam']
            sub = subject.objects.filter(dname=branch, sem_no=sem)
            s = subject.objects.filter(sb_name=psub).values('test1', 'test2', 'sem', 'tw', 'oral')
            subp = []
            for key, value in s[0].items():
                if value != 0:
                    subp.append(key)
            stud = student.objects.filter(dname=branch,s_semno=sem)
            m = []
            for i in stud:
                rs = i.result_set.get_or_create(sid=i.sid,sb_code=subject.objects.get(sb_name=psub),r_semno=sem)
                m.append(getattr(rs[0],'%sm'%(exam)))
            context = {
                'pexam':exam,
                'exam': subp,
                'pdname': branch,
                'psem': sem,
                'psub': psub,
                'sub': sub,
                'dept': dept.objects.all(),
                'sem': [1, 2, 3, 4, 5, 6, 7, 8],
                'stud':stud,
                'm':m
            }

            return render(request, 'examcell/addmark.html',context)
        elif request.POST['flag']=='4':
            branch = request.POST['dname']
            sem = request.POST['sem']
            psub = request.POST['sub']
            exam = request.POST['exam']
            sub = subject.objects.filter(dname=branch, sem_no=sem)
            length = len(sub)
            stud = student.objects.filter(dname=branch, s_semno=sem)
            i=0
            for s in stud:
                i+=1
                sb=subject.objects.get(sb_name=psub)
                r = s.result_set.get_or_create(sid=s, sb_code=sb, r_semno=sem)[0]
                m=request.POST['m%s'%(i)]
                if exam=='tw' and int(m)<=int(sb.tw):
                    r.twm=m
                elif exam=='sem' and int(m)<=int(sb.sem):
                    r.semm=m
                elif exam=='oral' and int(m)<=int(sb.oral):
                    r.oralm = m
                elif exam=='test1' and int(m)<=int(sb.test1):
                    r.test1m = m
                elif exam=='test2' and int(m)<=int(sb.test2):
                    r.test2m = m
                else:
                    context = {
                        'dept': dept.objects.all(),
                        'sem': [1, 2, 3, 4, 5, 6, 7, 8],
                        'msg': 'Marks were entered incorrectly'
                    }
                    return render(request, 'examcell/addmark.html', context)
                r.save()
            context = {
                'dept': dept.objects.all(),
                'sem': [1, 2, 3, 4, 5, 6, 7, 8],
                'msg':'sucessfully updated'
            }
            return render(request, 'examcell/addmark.html', context)

    else:
        context={
            'dept':dept.objects.all(),
            'sem':[1, 2, 3, 4, 5, 6, 7, 8]
        }
        return render(request,'examcell/addmark.html', context)

@staff_member_required(login_url='examcell:login')
def  studmark(request):
    if request.method=='POST':
        if request.POST['flag']=='1':
            sid = request.POST['sid']
            sem = request.POST['sem']
            semsub = subject.objects.filter(sem_no=sem)
            #res = student.objects.get(sid=sid).result_set.filter(r_semno=sem)
            a=[None for i in semsub]
            i=0
            for x in semsub:
                a[i]=result.objects.get_or_create(sb_code=x,sid=student.objects.get(sid=sid),r_semno=sem)[0]
                i+=1
            return render(request,'examcell/studmark.html',{'result':result,'sub':semsub,'sem':sem,'stud':student.objects.get(sid=sid),'r':a,'i':i})
        elif request.POST['flag']=='2':
            sid = request.POST['sid']
            sem = request.POST['sem']
            semsub = subject.objects.filter(sem_no=sem)
            #res = student.objects.get(sid=sid).result_set.filter(r_semno=sem)
            #a=[None for i in semsub]
            i=1
            for x in semsub:
                a=result.objects.get_or_create(sb_code=x,sid=student.objects.get(sid=sid),r_semno=sem)[0]
                a.test1m = request.POST['test1%d' % (i)]
                a.test2m = request.POST['test2%d' % (i)]
                a.testavg = request.POST['testavg%d' % (i)]
                a.semm = request.POST['sem%d' % (i)]
                a.twm = request.POST['tw%d' % (i)]
                a.oralm = request.POST['oral%d' % (i)]
                a.totalm = request.POST['total%d' % (i)]
                print('check point')
                # if request.POST['test1%d'%(i)]!= '0':
                #     a[i].test1m = request.POST['test1%d'%(i)]
                # if request.POST['test2%d'%(i)]!= '0':
                #     a[i].test2m = request.POST['test2%d'%(i)]
                # if request.POST['testavg%d'%(i)]!= '0':
                #     a[i].testavg = request.POST['testavg%d'%(i)]
                # if request.POST['sem%d'%(i)]!= '0':
                #     a[i].semm = request.POST['sem%d'%(i)]
                # if request.POST['tw%d'%(i)]!= '0':
                #     a[i].twm = request.POST['tw%d'%(i)]
                # if request.POST['oral%d'%(i)]!= '0':
                #     a[i].oralm = request.POST['oral%d'%(i)]
                # if request.POST['total%d'%(i)]!= '0':
                #     a[i].totalm = request.POST['total%d'%(i)]
                a.save()
                i+=1
            return render(request, 'examcell/studmark.html', {'msg':'result updated'})

    return render(request,'examcell/studmark.html',{})

def divid(a,b):
    try:
        return a/b
    except:
        return 0

@staff_member_required(login_url='examcell:login')
def resultgen(request):
    if request.method == 'POST':
        if request.POST['flag']=='1':
            branch = request.POST['dname']
            sem = request.POST['sem']
            stud1 = student.objects.filter(s_semno=sem,dname=dept.objects.get(dname=branch)).order_by('sid')
            m = 'sem%d' % (int(sem))
            stud2 = student.objects.filter(**{m:2},dname=dept.objects.get(dname=branch)).order_by('sid')
            stud = list(chain(stud1,stud2))
            res=[]
            grad = []
            for r in stud:
                res.append(r.result_set.filter(r_semno=sem))
            i = 0
            pointer = []
            for r in stud:
                tresult = r.result_set.filter(r_semno=sem)
                k=0
                f=0
                total_sub_point= 0
                tw_total_point = 0
                th_total_point = 0
                grad.append([])
                for s in tresult:
                    j = subject.objects.get(sb_code=s.sb_code.sb_code)
                    grad[i].append([])
                    grad[i][k].append(s.grade(s.test1m,j.test1))
                    grad[i][k].append(s.grade(s.test2m, j.test2))
                    grad[i][k].append(s.grade(s.avg, j.test2))
                    grad[i][k].append(s.grade(s.semm, j.sem))
                    grad[i][k].append(s.grade(s.thtot, (j.test2+j.sem)))
                    grad[i][k].append(s.grade(s.oralm, j.oral))
                    grad[i][k].append(s.grade(s.twm, j.tw))
                    grad[i][k].append(s.grade(s.ptot, (j.oral+j.tw)))
                    grad[i][k].append(s.grade(s.total, (j.test2+j.sem+j.oral+j.tw)))
                    if (s.grade(s.avg,j.test2))=='F': f=1
                    elif (s.grade(s.semm, j.sem)) == 'F': f = 1
                    elif (s.grade(s.oralm, j.oral)) == 'F': f = 1
                    elif (s.grade(s.twm, j.tw)) == 'F': f = 1

                    total_sub_point += j.tw_prc_credit
                    total_sub_point += j.theory_credit
                    tw_total_point += s.ppoint
                    th_total_point += s.thpoint
                    k+=1
                i+=1
                p = "{0:.2f}".format(divid((tw_total_point+th_total_point),(total_sub_point)))
                if f==1:
                    pointer.append((tw_total_point+th_total_point,'F'))
                else:
                    pointer.append((tw_total_point + th_total_point,p))
            z  = [x for x in range(i)]
            res = zip(z,res)
            #d=request.POST['flag9']
            return render(request,'examcell/rgen.html',{'stud':stud,'sem':sem,'res':res,'grad':grad,'x':0,'y':0,'z':0,'pointer':pointer,'dept':branch})
        else:
            sem = request.POST['sem']
            d = request.POST['dept']
            stud1 = student.objects.filter(s_semno=sem, dname=dept.objects.get(dname=d)).order_by('sid')
            m = 'sem%d' % (int(sem))
            stud2 = student.objects.filter(**{m: 2}, dname=dept.objects.get(dname=d)).order_by('sid')
            stud = list(chain(stud1, stud2))

            for r in stud:
                tresult = r.result_set.filter(r_semno=sem)
                f = 0
                for s in tresult:
                    j = subject.objects.get(sb_code=s.sb_code.sb_code)
                    if (s.grade(s.avg,j.test2))=='F': f=1
                    elif (s.grade(s.semm, j.sem)) == 'F': f = 1
                    elif (s.grade(s.oralm, j.oral)) == 'F': f = 1
                    elif (s.grade(s.twm, j.tw)) == 'F': f = 1
                x = 'sem%d' % (int(sem))
                if f == 1:
                    setattr(r,x,2)
                    #student.objects.filter(sid=r.sid).update(**{x :2})
                else:
                    setattr(r,x,1)
                    #student.objects.filter(sid=r.sid).update(**{x: 1})
                if int(sem)>4:
                    x = 'sem%d' % (int(sem)-4)
                    st = getattr(r,x)
                    if st == 2:
                        r.s_semno=0
                    else:
                        r.s_semno=int(sem)+1
                r.save()
            #d = request.POST['flag9']
            return render(request,'examcell/rgen.html',{'msg':'Result is Issued Successfully'})
    else:
        return render(request,'examcell/rgen.html',{'dept':dept.objects.all()})



def hallgen(request):
    if request.method == 'POST':
        d = request.POST['dname']
        sem = request.POST['sem']
        stud = student.objects.filter(s_semno= sem,dname=dept.objects.get(dname=d))
        i=0
        for h in stud:
            seatno = '%s%02d'%(int(sem),i)
            hallticket.objects.get_or_create(seatno=seatno,sid=h,hsem=sem)
            i+=1
        f = 'sem%d'%(int(sem))
        stud = student.objects.filter(**{f:2})
        for h in stud:
            seatno = '%d%02d'%(int(sem), i)
            hallticket.objects.get_or_create(seatno=seatno, sid=h, hsem=sem)
            i += 1
        hall = hallticket.objects.filter(hsem=sem)
        return render(request,'examcell/hallgen.html',{'hall':hall})
    else:
        return render(request,'examcell/hallgen.html',{'dept':dept.objects.all()})

def rev(request):
    r = reval.objects.all()
    return render(request,'examcell/reval.html',{'r':r,'tname':'Reval'})

def pho(request):
    r = photo.objects.all()
    return render(request,'examcell/reval.html',{'r':r,'tname':'Photo Copy'})

def addnot(request):
    if request.method=='POST':
        sub = request.POST['sub']
        msg = request.POST['msg']
        obj = notice(sub=sub,text=msg)
        obj.save()
        return render(request,'examcell/addnot.html',{'msg':'Notice Added'})
    else:
        return render(request, 'examcell/addnot.html', {})
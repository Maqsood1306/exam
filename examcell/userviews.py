from django.shortcuts import render, redirect, render_to_response
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout, get_user,user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import stud_id, student, dept, subject, result, photo, reval, hallticket, nc_student,notice
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def userlog(request):
    if request.method == 'POST':
        username = request.POST['sid']
        password = request.POST['pwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('examcell:home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'examcell/user/userlogin.html', {'msg': 'login Fails'})
    else:
        return render(request, 'examcell/user/userlogin.html', {})

def user_logout_view(request):
    logout(request)
    return redirect('examcell:index')

@login_required(login_url='examcell:userlogin')
def home(request):
    s = get_user(request)

    n = notice.objects.all().order_by('-time')
    return render(request, 'examcell/user/home.html',{'sid':s,'n':n})

def userregister(request):
    if request.method=='POST':
        try:
            sid = request.POST['sid']
            sd = stud_id.objects.filter(studid=sid)
            sdd = student.objects.filter(sid=sid)
            if sd and not sdd:
                fname = request.POST['sname']
                mname = request.POST['mname']
                lname = request.POST['lname']
                pic = request.POST['pic']
                email = request.POST['email']
                pwd = request.POST['pwd']
                addr = request.POST['addr']
                cont = request.POST['mob']
                dep = dept.objects.get(dname=request.POST['dname'])
                gen = request.POST['gender']
                s = nc_student(sid=sid,
                        s_fname=fname,
                        s_mname=mname,
                        s_lname=lname,
                        s_image=pic,
                        s_email=email,
                        s_password=pwd,
                        s_address=addr,
                        s_contact=cont,
                        dname=dep,
                        s_gender=gen)
                user = User.objects.create_user(sid, email, pwd)
                user.save()
                s.save()
                return redirect('examcell:userlogin')
            else:
                return render(request, 'examcell/user/userregister.html', {'msg': 'Invalid Student ID'})
        except student.DoesNotExist :
            sid=None
    else:
        return render(request, 'examcell/user/userregister.html', {'dept': dept.objects.all()})


def divid(a,b):
    try:
        return a/b
    except:
        return 0

@login_required(login_url='examcell:userlogin')
def results(request):
    if request.method=='POST':

        s = get_user(request)
        semno = request.POST['sem']
        sid = student.objects.get(sid=s.username)
        p = getattr(sid,'sem%s'%(semno))
        if p!=0:
            r = student.objects.get(sid=s.username)
            tresult = r.result_set.filter(r_semno=semno)
            k = 0
            f = 0
            total_sub_point = 0
            tw_total_point = 0
            th_total_point = 0

            grad=[]
            for s in tresult:
                j = subject.objects.get(sb_code=s.sb_code.sb_code)
                grad.append([])
                grad[k].append(s.grade(s.test1m, j.test1))
                grad[k].append(s.grade(s.test2m, j.test2))
                grad[k].append(s.grade(s.avg, j.test2))
                grad[k].append(s.grade(s.semm, j.sem))
                grad[k].append(s.grade(s.thtot, (j.test2 + j.sem)))
                grad[k].append(s.grade(s.oralm, j.oral))
                grad[k].append(s.grade(s.twm, j.tw))
                grad[k].append(s.grade(s.ptot, (j.oral + j.tw)))
                grad[k].append(s.grade(s.total, (j.test2 + j.sem + j.oral + j.tw)))
                if (s.grade(s.avg, j.test2)) == 'F':
                    f = 1
                elif (s.grade(s.semm, j.sem)) == 'F':
                    f = 1
                elif (s.grade(s.oralm, j.oral)) == 'F':
                    f = 1
                elif (s.grade(s.twm, j.tw)) == 'F':
                    f = 1

                total_sub_point += j.tw_prc_credit
                total_sub_point += j.theory_credit
                tw_total_point += s.ppoint
                th_total_point += s.thpoint
                k += 1
            p = "{0:.2f}".format(divid((tw_total_point + th_total_point), (total_sub_point)))
            if f == 1:
                pointer = (tw_total_point + th_total_point, 'F')
            else:
                pointer = (tw_total_point + th_total_point, p)
            return render(request, 'examcell/user/result.html',
                          {'stud': r, 'sem': semno, 'res': tresult, 'grad': grad,'pointer': pointer})
            #return render(request, 'examcell/user/result.html', {'rs': rs})
        else:
            return render(request, 'examcell/user/result.html', {'msg': 'Result is not yet issued'})


    else:
        return render(request,'examcell/user/result.html',{})

def resultpdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="result.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    p.save()
    return response

@login_required(login_url='examcell:userlogin')
def phot(request):
    if request.method=='POST':
        if request.POST['flag'] == '1':
            sem = request.POST['sem']
            sub = subject.objects.filter(sem_no=sem)
            #j = subject.objects.get(sem=sem)
            return render(request,'examcell/user/phot.html',{'sub':sub,'sem':sem})
        else:
            sub = request.POST['sub']
            s = get_user(request)
            rs = student.objects.get(sid=s.username).result_set.get(sb_code=subject.objects.get(sb_code=sub))
            photo.objects.get_or_create(res=rs)
            return render(request, 'examcell/user/phot.html', {'msg': 'You have Successfully applied for Photo copy'})

    else:
        return render(request,'examcell/user/phot.html',{'tname':'PhotoCopy'})


@login_required(login_url='examcell:userlogin')
def revals(request):
    if request.method=='POST':
        if request.POST['flag'] == '1':
            sem = request.POST['sem']
            sub = subject.objects.filter(sem_no=sem)
            #j = subject.objects.get(sem=sem)
            return render(request,'examcell/user/phot.html',{'sub':sub,'sem':sem})
        else:
            sub = request.POST['sub']
            s = get_user(request)
            rs = student.objects.get(sid=s.username).result_set.get(sb_code=subject.objects.get(sb_code=sub))
            reval.objects.get_or_create(res=rs)
            return render(request, 'examcell/user/phot.html', {'msg': 'You have Successfully applied for Reval'})

    else:
        return render(request,'examcell/user/phot.html',{'tname':'Reval'})

def userhall(request):
    if request.method == 'POST':
        sem = request.POST['sem']
        s = get_user(request)
        stud = student.objects.get(sid=s.username)
        #try:
        x = getattr(stud,'sem%d'%(int(sem)))
        subc=[]
        subd = subject.objects.filter(sem_no=sem, dname=stud.dname, sem__gt=0)
        if x == 0 or x==1:
            sub = subject.objects.filter(sem_no=sem,dname=stud.dname,sem__gt=0)
            for i in sub:
               subc.append('Eligible')
        elif x == 2:
            sub = stud.result_set.filter(r_semno=sem,semm__gt=39)
            for i in sub:
               subc.append('Eligible')
            for i in range(4-len(sub)):
                subc.append('pass')
        hall = hallticket.objects.get(sid=stud, hsem=sem)
        context = {
            'seat':hall.seatno,
            'name':stud.s_fname+' '+stud.s_mname+' '+stud.s_lname,
            'sem':sem,
            's1': subc[0],
            's2': subc[1],
            's3': subc[2],
            's4': subc[3],
            'sub1': subd[0].sb_name,
            'sub2': subd[1].sb_name,
            'sub3': subd[2].sb_name,
            'sub4': subd[3].sb_name,
        }
        pdf = render_to_pdf('examcell/user/hallpdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s_%d.pdf" % (stud.s_fname,stud.sid)
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        #except Exception:
         #   return render(request, 'examcell/user/hall.html', {'msg': 'Hall Ticket is not ye issued'})
    else:
        return render(request,'examcell/user/hall.html',{})




from django.db import models
from django.utils import timezone

class dept(models.Model):
    dname = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.dname



class subject(models.Model):
    sb_code = models.CharField(max_length=10, primary_key=True)
    sb_name = models.CharField(max_length=40)
    test1 = models.IntegerField()
    test2 = models.IntegerField()
    sem = models.IntegerField()
    tw = models.IntegerField()
    oral = models.IntegerField()
    theory_credit = models.IntegerField()
    tw_prc_credit = models.IntegerField()
    dname = models.ForeignKey(dept, on_delete=models.CASCADE)
    sem_no = models.IntegerField()
    def __str__(self):
        return self.sb_name

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name, None)
            yield (field_name, value)


class nc_student(models.Model):
    sid = models.IntegerField(primary_key=True, )
    s_fname = models.CharField(max_length=15)
    s_mname = models.CharField(max_length=15)
    s_lname = models.CharField(max_length=15)
    s_image = models.ImageField()
    s_email = models.EmailField(max_length=100)
    s_password = models.CharField(max_length=25)
    s_address = models.CharField(max_length=200)
    s_contact = models.IntegerField()
    s_gender = models.CharField(max_length=7)
    dname = models.ForeignKey(dept, on_delete=models.CASCADE)
    s_semno = models.IntegerField(default=1)
    s_confirm = models.IntegerField(default=0)
    sem1 = models.IntegerField(default=0)
    sem2 = models.IntegerField(default=0)
    sem3 = models.IntegerField(default=0)
    sem4 = models.IntegerField(default=0)
    sem5 = models.IntegerField(default=0)
    sem6 = models.IntegerField(default=0)
    sem7 = models.IntegerField(default=0)
    sem8 = models.IntegerField(default=0)
    def __str__(self):
        return self.s_fname


class student(models.Model):
    sid = models.IntegerField(primary_key=True, )
    s_fname = models.CharField(max_length=15)
    s_mname = models.CharField(max_length=15)
    s_lname = models.CharField(max_length=15)
    s_image = models.ImageField()
    s_email = models.EmailField(max_length=100)
    s_password = models.CharField(max_length=25)
    s_address = models.CharField(max_length=200)
    s_contact = models.IntegerField()
    s_gender = models.CharField(max_length=7)
    dname = models.ForeignKey(dept, on_delete=models.CASCADE)
    s_semno = models.IntegerField(default=1)

    sem1 = models.IntegerField(default=0)
    sem2 = models.IntegerField(default=0)
    sem3 = models.IntegerField(default=0)
    sem4 = models.IntegerField(default=0)
    sem5 = models.IntegerField(default=0)
    sem6 = models.IntegerField(default=0)
    sem7 = models.IntegerField(default=0)
    sem8 = models.IntegerField(default=0)
    def __str__(self):
        return self.s_fname


class hallticket(models.Model):
    seatno = models.IntegerField()
    sid =  models.ForeignKey(student,on_delete=models.CASCADE)
    hsem = models.IntegerField()
    def __str__(self):
        return self.sid.s_fname

class result(models.Model):
    sid = models.ForeignKey(student, on_delete=models.CASCADE)
    sb_code = models.ForeignKey(subject, on_delete=models.CASCADE)
    test1m = models.IntegerField(default=0)
    test2m = models.IntegerField(default=0)
    testavg = models.IntegerField(default=0)
    semm = models.IntegerField(default=0)
    twm = models.IntegerField(default=0)
    oralm = models.IntegerField(default=0)
    totalm = models.IntegerField(default=0)
    r_semno = models.IntegerField(default=0)
    def __str__(self):
        return self.sid.s_fname

    @property
    def thtot(self):
        return int((self.avg + self.semm))

    @property
    def thpoint(self):
        thcred = self.sb_code.theory_credit
        thto = int(self.sb_code.test2)+int(self.sb_code.sem)
        grad = self.gradepoint(self.thtot, thto)
        return int(thcred)*int(grad)

    @property
    def ppoint(self):
        thcred = self.sb_code.tw_prc_credit
        thto = int(self.sb_code.tw)+int(self.sb_code.oral)
        grad = self.gradepoint(self.ptot, thto)
        return int(thcred)*int(grad)


    @property
    def ptot(self):
        return (self.twm + self.oralm)

    @property
    def avg(self):
        return int((self.test1m + self.test2m)/2)

    @property
    def total(self):
        return int((self.test1m + self.test2m)/2)+self.semm+self.oralm+self.twm


    def grade(self,m,n):
        try:
            per=m/n*100
            if per>=80:
                return 'O'
            elif per>=75 and per<80:
                return 'A'
            elif per>=70 and per<75:
                return 'B'
            elif per>=60 and per<70:
                return 'C'
            elif per>=50 and per<60:
                return 'D'
            elif per>=45 and per<50:
                return 'E'
            elif per>=40 and per<45:
                return 'p'
            elif per<40:
                return 'F'
        except ZeroDivisionError:
            return '-'

    def gradepoint(self,m,n):
        try:
            per=m/n*100
            if per>=80:
                return '10'
            elif per>=75 and per<80:
                return '9'
            elif per>=70 and per<75:
                return '8'
            elif per>=60 and per<70:
                return '7'
            elif per>=50 and per<60:
                return '6'
            elif per>=45 and per<50:
                return '5'
            elif per>=40 and per<45:
                return '4'
            elif per<40:
                return '0'
        except ZeroDivisionError:
            return '0'




class stud_id(models.Model):
    studid = models.IntegerField(primary_key=True)
    studname = models.CharField(max_length=50)
    def __str__(self):
        return self.studname


class reval(models.Model):
    res = models.ForeignKey(result,on_delete=models.CASCADE)

class photo(models.Model):
    res = models.ForeignKey(result,on_delete=models.CASCADE)

class notice(models.Model):
    sub = models.TextField(max_length=100)
    text = models.TextField(max_length=500)
    time = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.sub









# Create your models here.

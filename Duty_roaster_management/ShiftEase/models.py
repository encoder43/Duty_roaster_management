from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.views import View

class EmployeeDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empcode = models.CharField(max_length=50,unique=True,null=True)
    empdept = models.CharField(max_length=50, null=True)
    designation = models.CharField(max_length=75, null=True)
    contact = models.CharField(max_length=12,unique=True, null=True, validators=[RegexValidator(r'^\d{1,10}$')]) # Added RegexValidator to validate phone number
    gender = models.CharField(max_length=50, null=True)
    supervisorcode = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    employee_name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10)

class Request(models.Model):
    employee = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='Pending')

class Announcement(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

class Shift(models.Model):
    employee = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    area = models.CharField(max_length=50)

class Company(models.Model):
    cName = models.CharField(primary_key='true',max_length=50,unique='true')
    cEmail = models.EmailField()
    cLogo = models.ImageField(upload_to="images", blank=True)
    cUrl = models.CharField(max_length=50)
    class Meta:
        db_table = "company"
def show_employee_details(request):
    employees = EmployeeDetail.objects.all()  # Retrieve all employees from the database
    context = {'EmployeeDetail': employees}
    return render(request, 'showemp.html', context)

class EditEmployeeView(models.Model):
    model = EmployeeDetail
    fields = ['user','empcode','empdept', 'designation', 'contact','gender','supervisorcode']

    def get_success_url(self):
        return reverse('sup_home')

class EmployeeUpdateView(UpdateView):
    queryset = EmployeeDetail.objects.all()
    template_name = 'edit.html'
    model = EmployeeDetail
    fields = ['user', 'empcode', 'empdept', 'designation', 'contact','gender', 'supervisorcode']

    def get_success_url(self):
        return reverse('employee_list')
class HelpdeskTicket(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name
class HelpdeskView(View):
    def get(self, request):
        tickets = HelpdeskTicket.objects.all()
        context = {
            'tickets': tickets,
        }
        return render(request, 'helpdesk.html', context)

class Message(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
class ShiftChangeRequest(models.Model):
    employee_id = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

class LeaveRequest(models.Model):
    employee = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.employee.name + ' - ' + self.start_date + ' to ' + self.end_date
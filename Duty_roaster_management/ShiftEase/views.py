from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ShiftEase.models import *
from django.contrib import messages
from ShiftEase.models import Company,EmployeeDetail
from ShiftEase.forms import CompanyForm,EmployeeForm
from ShiftEase.models import Message
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect


def home(request):
    return render(request, 'home.html')


def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST.get("firstname")
        ln = request.POST.get("lastname")
        ec = request.POST.get("empcode")
        em = request.POST.get("email")
        pwd = request.POST.get("pwd")
        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=em, password=pwd)
            employee = EmployeeDetail.objects.create(user=user, empcode=ec)
            error = "no"
        except Exception as e:
            error = "yes"
            print(str(e))
    return render(request, 'registration.html', {'error': error})


def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "no"
            if not hasattr(user, 'employee_detail'):
                employee = EmployeeDetail.objects.create(user=user)
        else:
            error = "yes"
    return render(request, 'emp_login.html', locals())


@login_required
def emp_home(request):
    employee = request.user.employee_detail
    attendance_records = Attendance.objects.filter(employee=employee)
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()
    chart_data = {
        'labels': ['Present', 'Absent'],
        'values': [present_count, absent_count]
    }
    return render(request, 'emp_home.html', {'chart_data': chart_data})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('emp_home'))
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def edit_profile(request):
    employee = EmployeeDetail.objects.filter(user=request.user).first()
    if request.method == 'POST':
        employee.empcode = request.POST.get('empcode')
        employee.empdept = request.POST.get('empdept')
        employee.designation = request.POST.get('designation')
        employee.contact = request.POST.get('contact')
        employee.gender = request.POST.get('gender')
        employee.supervisorcode = request.POST.get('supervisorcode')
        employee.save()
        return redirect(reverse('view_profile'))
    return render(request, 'edit_profile.html', {'employee': employee})


@login_required
def view_profile(request):
    user = request.user
    emp_details = EmployeeDetail.objects.filter(user=user).first()
    return render(request, 'view_profile.html', {'user': user, 'emp_details': emp_details})


@login_required
def emp_logout(request):
    logout(request)
    return redirect(reverse('emp_login'))

def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_home.html')


def sup_login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('sup_home')
            else:
                error = "You are not authorized to access this page."
        else:
            error = "Invalid username or password."
    context = {'error': error}
    return render(request, 'sup_login.html', context)

@login_required
def assign_shift(request):
    if request.method == 'POST':
        # Get form data
        employee_id = request.POST.get('employee_id')
        shift_date = request.POST.get('shift_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        area = request.POST.get('area')

        # Create new shift object
        employee = EmployeeDetail.objects.get(id=employee_id)
        shift = Shift(employee=employee, shift_date=shift_date, start_time=start_time, end_time=end_time, area=area)
        shift.save()

        # Redirect to confirmation page
        return render(request, 'shift_assigned.html', {'shift': shift})

    else:
        # Get list of employees
        employees = EmployeeDetail.objects.all()

        # Render form page
        return render(request, 'assign_shift.html', {'employees': employees})

@login_required
def record_attendance(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        status = request.POST.get('status')
        date = request.POST.get('date')
        attendance = Attendance(employee_id=employee_id, status=status, date=date)
        attendance.save()
        messages.success(request, 'Attendance recorded successfully')
        return redirect('record_attendance')
    else:
        employees = User.objects.filter(is_staff=True)
        return render(request, 'record_attendance.html', {'employees': employees})

@login_required
def view_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'view_attendance.html', {'attendances': attendances})

def sup_home(request):
    attendance_data = Attendance.objects.all()
    context = {'attendance_data': attendance_data}
    return render(request,'sup_home.html', context)


# To create Company
@login_required
def comp(request):
    if request.method == "POST":

        form = CompanyForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/show")
            except:
                pass
    else:
        form = CompanyForm()
    return render(request, "index.html", {'form': form})


# To retrieve Company details
@login_required
def show(request):
    companies = Company.objects.all()
    return render(request, "show.html", {'companies': companies})


# To Edit Company details
@login_required
def edit(request, cName):
    company = Company.objects.get(cName=cName)
    return render(request, "edit.html", {'company': company})


# To Update Company
@login_required
def update(request, cName):
    company = Company.objects.get(cName=cName)
    form = CompanyForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, "edit.html", {'company': company})


# To Delete Company details
@login_required
def delete(request, cName):
    company = Company.objects.get(cName=cName)
    company.delete()
    return redirect("/show")


# To create employee
@login_required
def emp(request):
    if request.method == "POST":

        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:

                form.save()
                return redirect("/showemp")
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request, "addemp.html", {'form': form})


# To show employee details
@login_required
def showemp(request):
    employee = EmployeeDetail.objects.filter(user=request.user).first()
    if request.method == 'POST':
        employee.empcode = request.POST.get('empcode')
        employee.empdept = request.POST.get('empdept')
        employee.designation = request.POST.get('designation')
        employee.contact = request.POST.get('contact')
        employee.gender = request.POST.get('gender')
        employee.supervisorcode = request.POST.get('supervisorcode')
        employee.save()
        return redirect(reverse('showemp'))
    return render(request, 'showemp.html', {'employee': employee})
# To delete employee details
@login_required
def deleteemployee(request, empcode):
    employee = get_object_or_404(EmployeeDetail, id=empcode)
    employee.delete()
    return redirect("sup_home")



# To edit employee details
@login_required
def editemployee(request, empcode):
    employee = get_object_or_404(EmployeeDetail, id=empcode)
    if request.method == "POST":
        # Update the employee's details
        employee.first_name = request.POST["first_name"]
        employee.last_name = request.POST["last_name"]
        employee.email = request.POST["email"]
        employee.phone_number = request.POST["phone_number"]
        employee.save()
        return redirect("sup_home")
    else:
        # Render the edit employee template
        return render(request, "editemployee.html", {"employee": employee})



# To update employee details
@login_required
def updateEmp(request, eFname):
    employee = EmployeeDetail.objects.get(eFname=eFname)
    form = EmployeeForm(request.POST, instance=employee)
    print('Hello1')
    if form.is_valid():
        form.save()
        return redirect("/showemp")
    return render(request, "editemployee.html", {'employee': employee})
@login_required
def helpdesk(request):
    tickets = HelpdeskTicket.objects.all()
    context = {
        'tickets': tickets,
    }
    return render(request, 'helpdesk.html', context)
@login_required
def index(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})
@login_required
def send_message(request):
    if request.method == 'POST':
        if 'subject' in request.POST:
            subject = request.POST['subject']
            # Continue with your logic to process the subject

            return HttpResponse("Message sent successfully!")  # Example response
        else:
            return HttpResponseBadRequest("Subject field is missing.")
    else:
        return render(request, 'send_message.html')
@login_required
def shift_change_request(request):
    if request.method == "POST":
        # Validate the request data
        employee_id = request.POST["employee_id"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        reason = request.POST["reason"]

        # Create a new shift change request object
        shift_change_request = ShiftChangeRequest(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
        )

        # Save the shift change request object to the database
        shift_change_request.save()

        # Redirect the user to a confirmation page
        return redirect("shift_change_request_confirmation")

    else:
        return render(request, "shift_change_request.html")

@login_required
def submit_leave_request(request):
    employee = request.user
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    reason = request.POST['reason']

    new_leave_request = LeaveRequest.objects.create(employee=employee, start_date=start_date, end_date=end_date, reason=reason, status='Pending')

    return redirect('submit_leave_request')
def assign_duties_view(request):
    if request.method == 'POST':
        duties = request.POST.getlist('duties[]')
        # Process the duties assignment here

        # Redirect to a success page or perform any other desired action
        return HttpResponseRedirect('/success-page/')
    else:
        employees = []  # Replace this with your employee data retrieval logic
        context = {'employees': employees}
        return render(request, 'assign_duties.html', context)
def view_duties_view(request):
    # Fetch the assigned duties from the database
    assigned_duties = EmployeeDetail.objects.all()

    context = {
        'AssignedDuties': assigned_duties
    }
    return render(request, 'view_duties.html', context)
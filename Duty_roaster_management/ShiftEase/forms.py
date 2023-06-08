from django import forms
from ShiftEase.models import EmployeeDetail
from ShiftEase.models import Company

# This is for employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetail
        fields = "__all__"

#this is for company
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

#class loginForm(forms.ModelForm):
    #class Meta:
        #model = Login
        #fields = "__all__"
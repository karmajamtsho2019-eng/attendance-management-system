from django import forms

from apps.academics.models import Department, Subject


class AttendanceSessionForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label='Select department',
    )
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    class_name = forms.CharField(max_length=100, required=False, label='Class / Section')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    session = forms.IntegerField(min_value=1, max_value=8, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        department = None
        if self.data.get('department'):
            department = Department.objects.filter(pk=self.data.get('department')).first()
        elif self.initial.get('department'):
            department = self.initial['department']

        if department:
            self.fields['subject'].queryset = Subject.objects.filter(department=department)
        else:
            self.fields['subject'].queryset = Subject.objects.all()


class AttendanceExportForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label='All departments',
    )
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        department = None
        if self.data.get('department'):
            department = Department.objects.filter(pk=self.data.get('department')).first()
        elif self.initial.get('department'):
            department = self.initial['department']

        if department:
            self.fields['subject'].queryset = Subject.objects.filter(department=department)
        else:
            self.fields['subject'].queryset = Subject.objects.all()

from django import forms

class JoinStudyGroupForm(forms.Form):
    full_name = forms.CharField(label="Full name", max_length=100)
    email = forms.EmailField(label="Email address")
    course_code = forms.CharField(label="Course code", max_length=20)
    message = forms.CharField(
        label="Message to the group owner",
        widget=forms.Textarea,
        required=False,
    )

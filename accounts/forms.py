from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class':'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        
    }))

   

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
                

            )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        
        if '@' in data or '-' in data or '|' in data or '#' in data or '$' in data:
           raise forms.ValidationError("Name should not have special characters.")
        return data
    
    def clean_last_name(self):
        lname = self.cleaned_data['last_name']
        
        if '@' in lname or '-' in lname or '|' in lname or '#' in lname or '$' in lname:
           raise forms.ValidationError("Last Name should not have special characters.")
        return lname



# for css login page
    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            


   



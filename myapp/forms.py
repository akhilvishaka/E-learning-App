from django import forms
from myapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect(attrs={'class': 'radio'}),
            'order_date': forms.SelectDateWidget(attrs={'class':'years=date.today()'})
        }
        labels = {
            'student': 'Student Name',
            'order_date': 'Order Date'
        }


class InterestForm(forms.Form):
    interested_choices = ((1, 'Yes'), (0, 'No'))
    interested = forms.IntegerField(widget=forms.RadioSelect(choices=interested_choices))
    levels = forms.IntegerField(initial=1,min_value=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')


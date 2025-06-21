from datetime import datetime
from django import forms
from .models import Reserve, Image


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ("customer", "starting_date", "end_date", "people")
        widgets = {
            "starting_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ReservationForm, self).__init__(*args, **kwargs)
        if user and not user.is_staff:
            self.fields.pop("customer")

    def clean_starting_date(self):
        starting_date = self.cleaned_data.get("starting_date")
        if starting_date < datetime.now().date():
            self.add_error("starting_date", "La fecha de inicio debe ser mayor a la fecha de hoy.")
        return starting_date
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get("end_date")
        starting_date = self.cleaned_data.get("starting_date")
        if end_date <= starting_date:
            self.add_error("end_date","La fecha de fin debe ser posterior a la fecha de inicio.")
        return end_date


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(),
        }

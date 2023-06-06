from django import forms

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {"class": "form-control"}

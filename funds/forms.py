from django import forms

class FundUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV",
        help_text="Upload a .csv file matching the sample format.",
        widget=forms.ClearableFileInput(attrs={"accept": ".csv"})
    )
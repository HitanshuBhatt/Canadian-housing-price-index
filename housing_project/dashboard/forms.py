from django import forms 

class CSVUploadForm(forms.Form):
    csv_file=forms.FileField(label='upload a csv file')
    
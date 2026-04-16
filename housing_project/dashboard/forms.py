from django import forms

#  form used to upload csv file
class CSVUploadForm(forms.Form):
    #  input field to select file 
    csv_file = forms.FileField(label="Upload a CSV file")

# validatio for uploaded file
    def clean_csv_file(self):
        #  get uploaded file from cleaned from from data
        csv_file = self.cleaned_data["csv_file"]

# check if it is a .csv file 
        if not csv_file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a valid CSV file.")

#  check if file contains data and is not empty by checking size 
        if csv_file.size == 0:
            raise forms.ValidationError("The uploaded file is empty.")
#  return the validated file 
        return csv_file
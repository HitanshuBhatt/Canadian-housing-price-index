from django import forms


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload a CSV file")

    def clean_csv_file(self):
        csv_file = self.cleaned_data["csv_file"]

        if not csv_file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a valid CSV file.")

        if csv_file.size == 0:
            raise forms.ValidationError("The uploaded file is empty.")

        return csv_file
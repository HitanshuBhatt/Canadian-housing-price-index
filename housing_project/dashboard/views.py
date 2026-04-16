import csv
import io
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import HousingData

def upload_csv(request):
    success = False  # Initialize as False
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Read and decode the file
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) # Skip the header row
            
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                # This saves the data to your SQLite database
                HousingData.objects.update_or_create(
                    date=column[0],
                    geo=column[1],
                    category=column[2],
                    value=column[3]
                )
            success = True  # Update to True after the loop finishes to show success message 
    else:
        form = CSVUploadForm()
    
    return render(request, 'dashboard/upload.html', {'form': form, 'success': success})
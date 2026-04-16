<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======
import csv
import io
import json
from django.shortcuts import render
from django.db.models import Max
from .forms import CSVUploadForm
from .models import HousingData


def upload_csv(request):
    success = False
    form = CSVUploadForm()

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]

            try:
                data_set = csv_file.read().decode("utf-8-sig")
                io_string = io.StringIO(data_set)
                next(io_string, None)

                HousingData.objects.all().delete()

                for column in csv.reader(io_string, delimiter=",", quotechar='"'):
                    if len(column) >= 4:
                        try:
                            HousingData.objects.create(
                                date=column[0].strip(),
                                geo=column[1].strip(),
                                category=column[2].strip().lower(),
                                value=float(column[3])
                            )
                        except ValueError:
                            continue

                success = True

            except Exception:
                success = False

    return render(request, "dashboard/upload.html", {"form": form, "success": success})


def chart_view(request):
    national_data = HousingData.objects.filter(geo="Canada", category="house").order_by("date")
    line_labels = [str(d.date) for d in national_data]
    line_values = [float(d.value) for d in national_data]

    latest_date = HousingData.objects.aggregate(Max("date"))["date__max"]

    provinces = [
        "Alberta", "British Columbia", "Manitoba", "New Brunswick",
        "Newfoundland and Labrador", "Nova Scotia", "Ontario",
        "Prince Edward Island", "Quebec", "Saskatchewan"
    ]

    prov_data = HousingData.objects.filter(
        date=latest_date,
        geo__in=provinces,
        category="house"
    )

    bar_labels = [d.geo for d in prov_data]
    bar_values = [float(d.value) for d in prov_data]

    toronto = HousingData.objects.filter(
        geo="Toronto, Ontario",
        category="house"
    ).order_by("date")

    vancouver = HousingData.objects.filter(
        geo="Vancouver, British Columbia",
        category="house"
    ).order_by("date")

    comp_labels = [str(d.date) for d in toronto]
    toronto_vals = [float(d.value) for d in toronto]
    vancouver_vals = [float(d.value) for d in vancouver]

    context = {
        "line_labels": json.dumps(line_labels),
        "line_values": json.dumps(line_values),
        "bar_labels": json.dumps(bar_labels),
        "bar_values": json.dumps(bar_values),
        "comp_labels": json.dumps(comp_labels),
        "toronto_vals": json.dumps(toronto_vals),
        "vancouver_vals": json.dumps(vancouver_vals),
        "latest_date": latest_date,
    }

    return render(request, "dashboard/charts.html", context)
>>>>>>> Stashed changes

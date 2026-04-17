# CSV handling imports
import csv
import io
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Django imports for database queries and rendering templates
from django.db import transaction
from django.db.models import Max, Min
from django.shortcuts import render

# Import form and model
from .forms import CSVUploadForm
from .models import HousingData


# Second upload_csv function
def upload_csv(request):
    # Track whether upload succeeded
    success = False

    # Store any error message
    error_message = ""

    # Run when form is submitted
    if request.method == "POST":
        # Create form with request data and uploaded file
        form = CSVUploadForm(request.POST, request.FILES)

        # Check if form is valid
        if form.is_valid():
            # Get uploaded file
            csv_file = form.cleaned_data["csv_file"]

            try:
                # Read file contents
                data = csv_file.read().decode("utf-8-sig")
                io_string = io.StringIO(data)

                # Read CSV rows as dictionaries
                reader = csv.DictReader(io_string)

                # Clean field names and map them in uppercase form
                fieldnames = [name.strip() for name in (reader.fieldnames or [])]
                normalized_map = {name.upper(): name for name in fieldnames}

                # Required column names expected in CSV
                required_columns = {"DATE", "GEO", "CATEGORY", "VALUE"}

                # Check whether required columns exist
                if not required_columns.issubset(set(normalized_map.keys())):
                    missing = required_columns - set(normalized_map.keys())
                    error_message = f"Missing required column(s): {', '.join(missing)}"
                else:
                    # Run all database writes inside one transaction
                    with transaction.atomic():
                        # Process every CSV row
                        for row in reader:
                            # Read values using normalized header names
                            raw_date = (row.get(normalized_map["DATE"]) or "").strip()
                            raw_geo = (row.get(normalized_map["GEO"]) or "").strip()
                            raw_category = (row.get(normalized_map["CATEGORY"]) or "").strip().lower()
                            raw_value = (row.get(normalized_map["VALUE"]) or "").strip()

                            # Skip incomplete rows
                            if not raw_date or not raw_geo or not raw_category or not raw_value:
                                continue

                            # Convert date string to Python date
                            try:
                                parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                            except ValueError:
                                continue

                            # Convert numeric value safely
                            try:
                                parsed_value = Decimal(raw_value)
                            except (InvalidOperation, ValueError):
                                continue

                            # Update existing row or create a new one
                            HousingData.objects.update_or_create(
                                date=parsed_date,
                                geo=raw_geo,
                                category=raw_category,
                                defaults={"value": parsed_value},
                            )

                    # Mark upload as successful
                    success = True

            # Handle wrong encoding
            except UnicodeDecodeError:
                error_message = "Could not read the file. Please upload a UTF-8 CSV file."

            # Handle unexpected errors
            except Exception as e:
                error_message = f"Unexpected error: {e}"
    else:
        # Show blank upload form on first page load
        form = CSVUploadForm()

    # Return upload template with context
    return render(
        request,
        "dashboard/upload.html",
        {
            "form": form,
            "success": success,
            "error_message": error_message,
        },
    )


# Charts page view
def charts(request):
    # Selected category used for all charts
    selected_category = "house"

    # List of provinces used in province comparison chart
    province_names = [
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Nova Scotia",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
    ]

    # Query national Canada trend data
    national_qs = HousingData.objects.filter(
        geo="Canada",
        category=selected_category
    ).order_by("date")

    # Find latest available date in selected category
    latest_date = HousingData.objects.filter(
        category=selected_category
    ).aggregate(latest=Max("date"))["latest"]

    # Start with empty queryset for province comparison
    province_qs = HousingData.objects.none()

    # Get province data only if latest date exists
    if latest_date:
        province_qs = HousingData.objects.filter(
            date=latest_date,
            geo__in=province_names,
            category=selected_category
        ).order_by("geo")

    # Query Toronto trend data
    toronto_qs = HousingData.objects.filter(
        geo="Toronto, Ontario",
        category=selected_category
    ).order_by("date")

    # Query Vancouver trend data
    vancouver_qs = HousingData.objects.filter(
        geo="Vancouver, British Columbia",
        category=selected_category
    ).order_by("date")

    # Labels and values for Canada line chart
    line_labels = [item.date.strftime("%Y-%m") for item in national_qs]
    line_values = [float(item.value) for item in national_qs]

    # Labels and values for province bar chart
    bar_labels = [str(item.geo) for item in province_qs]
    bar_values = [float(item.value) for item in province_qs]

    # Labels and values for Toronto vs Vancouver chart
    comp_labels = [item.date.strftime("%Y-%m") for item in toronto_qs]
    toronto_vals = [float(item.value) for item in toronto_qs]
    vancouver_vals = [float(item.value) for item in vancouver_qs]

    # Send chart data to template
    context = {
        "latest_date": latest_date.strftime("%Y-%m-%d") if latest_date else "No data",
        "selected_category": selected_category.title(),
        "line_labels": json.dumps(line_labels),
        "line_values": json.dumps(line_values),
        "bar_labels": json.dumps(bar_labels),
        "bar_values": json.dumps(bar_values),
        "comp_labels": json.dumps(comp_labels),
        "toronto_vals": json.dumps(toronto_vals),
        "vancouver_vals": json.dumps(vancouver_vals),
    }

    # Render charts page
    return render(request, "dashboard/charts.html", context)

#  homepage 


# Home page view
def home(request):
    # Calculate dynamic stats for the homepage
    stats = {
        # Count all rows in database
        'total_records': HousingData.objects.count(),

        # Get earliest date in dataset
        'date_start': HousingData.objects.aggregate(Min('date'))['date__min'],

        # Get latest date in dataset
        'date_end': HousingData.objects.aggregate(Max('date'))['date__max'],

        # Count unique cities excluding Canada and provinces
        'city_count': HousingData.objects.exclude(geo__in=[
            'Canada', 'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 
            'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 
            'Prince Edward Island', 'Quebec', 'Saskatchewan'
        ]).values('geo').distinct().count(),

        # Get unique province names
        'provinces': HousingData.objects.filter(geo__in=[
            'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 
            'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 
            'Prince Edward Island', 'Quebec', 'Saskatchewan'
        ]).values_list('geo', flat=True).distinct()
    }

    # Render homepage with calculated statistics
    return render(request, 'dashboard/home.html', {'stats': stats})
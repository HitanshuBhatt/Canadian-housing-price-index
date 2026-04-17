# CSV handling imports
import csv
import io
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Django imports for auth, database queries and rendering templates
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Max, Min
from django.shortcuts import redirect, render

# Import forms and models
from .forms import CSVUploadForm, LoginForm, SignUpForm
from .models import HousingData, UserProfile


# login page using email and password
def login_view(request):
    # if user is already logged in then no need to show login page again
    if request.user.is_authenticated:
        return redirect("home")

    error_message = ""

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]

            # django login works with username, so first i find the user by email
            try:
                matched_user = User.objects.get(email__iexact=email)
                user = authenticate(
                    request,
                    username=matched_user.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                error_message = "Invalid email or password."
    else:
        form = LoginForm()

    return render(
        request,
        "dashboard/login.html",
        {
            "form": form,
            "error_message": error_message,
        },
    )


# signup page for new users
def signup_view(request):
    # if user is already logged in then just send them home
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"].strip()
            last_name = form.cleaned_data["last_name"].strip()
            dob = form.cleaned_data["dob"]
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]

            # using email as username too because it makes login simpler
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            # saving date of birth in profile table
            UserProfile.objects.create(
                user=user,
                dob=dob
            )

            # logging user in right after signup
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(
        request,
        "dashboard/signup.html",
        {
            "form": form,
        },
    )


# logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# upload_csv function
@login_required
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
@login_required
def charts(request):
    # selected category for all charts
    selected_category = "house"

    # --- 1. National Trend Data (Line) ---
    national_data = HousingData.objects.filter(
        geo="Canada",
        category=selected_category
    ).order_by("date")
    line_labels = [str(d.date) for d in national_data]
    line_values = [float(d.value) for d in national_data]

    # --- 2. Province Comparison Data (Bar) ---
    latest_date = HousingData.objects.aggregate(Max("date"))["date__max"]
    provinces = [
        "Alberta", "British Columbia", "Manitoba", "New Brunswick",
        "Newfoundland and Labrador", "Nova Scotia", "Ontario",
        "Prince Edward Island", "Quebec", "Saskatchewan"
    ]
    prov_data = HousingData.objects.filter(
        date=latest_date,
        geo__in=provinces,
        category=selected_category
    )
    bar_labels = [d.geo for d in prov_data]
    bar_values = [float(d.value) for d in prov_data]

    # --- 3. Toronto vs Vancouver Data (Comparison Line) ---
    toronto = HousingData.objects.filter(
        geo="Toronto, Ontario",
        category=selected_category
    ).order_by("date")
    vancouver = HousingData.objects.filter(
        geo="Vancouver, British Columbia",
        category=selected_category
    ).order_by("date")
    comp_labels = [str(d.date) for d in toronto]
    toronto_vals = [float(d.value) for d in toronto]
    vancouver_vals = [float(d.value) for d in vancouver]

    # --- 4. Interactive Explorer Data ---
    all_housing_data = HousingData.objects.filter(category=selected_category).order_by("date")
    structured_data = {}

    for entry in all_housing_data:
        if entry.geo not in structured_data:
            structured_data[entry.geo] = []
        structured_data[entry.geo].append({"x": str(entry.date), "y": float(entry.value)})

    all_geos = HousingData.objects.values_list("geo", flat=True).distinct()
    cities = [g for g in all_geos if g not in provinces and g != "Canada"]

    # Date time frame for interactive chart to allow user to select start and end date
    date_range = HousingData.objects.aggregate(
        earliest=Min("date"),
        latest=Max("date")
    )
    earliest_date = date_range["earliest"]
    latest_date = date_range["latest"]

    context = {
        "line_labels": json.dumps(line_labels),
        "line_values": json.dumps(line_values),
        "bar_labels": json.dumps(bar_labels),
        "bar_values": json.dumps(bar_values),
        "comp_labels": json.dumps(comp_labels),
        "toronto_vals": json.dumps(toronto_vals),
        "vancouver_vals": json.dumps(vancouver_vals),
        "full_dataset": json.dumps(structured_data),
        "province_list": provinces,
        "city_list": sorted(cities),
        "latest_date": latest_date,
        "earliest_date": earliest_date,
        "selected_category": selected_category.title(),
    }
    return render(request, "dashboard/charts.html", context)


# Home page view
@login_required
def home(request):
    # Calculate dynamic stats for the homepage
    stats = {
        # Count all rows in database
        "total_records": HousingData.objects.count(),

        # Get earliest date in dataset
        "date_start": HousingData.objects.aggregate(Min("date"))["date__min"],

        # Get latest date in dataset
        "date_end": HousingData.objects.aggregate(Max("date"))["date__max"],

        # Count unique cities excluding Canada and provinces
        "city_count": HousingData.objects.exclude(geo__in=[
            "Canada", "Alberta", "British Columbia", "Manitoba", "New Brunswick",
            "Newfoundland and Labrador", "Nova Scotia", "Ontario",
            "Prince Edward Island", "Quebec", "Saskatchewan"
        ]).values("geo").distinct().count(),

        # Get unique province names
        "provinces": HousingData.objects.filter(geo__in=[
            "Alberta", "British Columbia", "Manitoba", "New Brunswick",
            "Newfoundland and Labrador", "Nova Scotia", "Ontario",
            "Prince Edward Island", "Quebec", "Saskatchewan"
        ]).values_list("geo", flat=True).distinct()
    }

    # Render homepage with calculated statistics
    return render(request, "dashboard/home.html", {"stats": stats})
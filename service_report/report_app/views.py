from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .models import Activity, Person  
from .forms import ActivityForm, PersonForm, UserRegistrationForm
from datetime import timedelta 
import re
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')  

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            # Redirect to the login page after successful signup:
            return redirect('login')  # uses the URL name 'login'
            # or: return redirect('/login/')  # absolute path
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def landing_page(request):
    if request.user.is_authenticated:
        # Only fetch data for the logged-in user
        total_reports = Activity.objects.filter(user=request.user).count()
        total_return_visits = Person.objects.filter(user=request.user).count()

        recent_reports_raw = Activity.objects.filter(user=request.user).order_by('-date')[:5]
        recent_visits = Person.objects.filter(user=request.user).order_by('-next_appointment')[:5]
    else:
        # No data for anonymous users
        total_reports = 0
        total_return_visits = 0
        recent_reports_raw = []
        recent_visits = []

    # Format time for reports
    recent_reports = []
    for report in recent_reports_raw:
        if report.time_spent:
            hours = report.time_spent // 60
            minutes = report.time_spent % 60
            formatted_time = f"{hours}h {minutes}m"
        else:
            formatted_time = "0h 0m"

        recent_reports.append({
            'date': report.date,
            'formatted_time': formatted_time,
        })

    context = {
        'total_reports': total_reports,
        'total_return_visits': total_return_visits,
        'recent_reports': recent_reports,
        'recent_visits': recent_visits,
    }

    return render(request, 'landing_page.html', context)
@login_required
def add_report(request):
    if request.method == 'POST':
        hours_minutes = request.POST.get('time_spent', '')
        match = re.match(r'(\d+):(\d+)', hours_minutes)  # Match HH:MM format
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))

            if hours < 0 or minutes < 0 or minutes >= 60:
                messages.error(request, 'Invalid time format. Please enter in HH:MM.')
                return render(request, 'add_report.html')  # Replace with your template

            total_minutes = hours * 60 + minutes

            # Create Activity instance with the current user
            report = Activity(
                date=request.POST['date'],
                time_spent=total_minutes,
                user=request.user  # Associate the activity with the logged-in user
            )
            report.save()

            messages.success(request, 'Report successfully added!')
            return redirect('report_list')  # Adjust according to your URL configuration
        else:
            messages.error(request, 'Invalid time format. Please enter in HH:MM.')

    return render(request, 'add_report.html') 
   
@login_required
def report_list(request):
    reports = Activity.objects.all()
    report_data = []

    for report in reports:
        if report.id:  # Check if the report has a valid ID
            hours = report.time_spent // 60
            minutes = report.time_spent % 60
            report_data.append({
                'id': report.id,
                'date': report.date,
                'time_spent': f"{hours}:{minutes:02d}",  # Format to HH:MM
                'user': report.user.username if report.user else "Unknown",
            }) 
        else:
            print(f"Invalid report ID detected: {report}")  # Debugging line for invalid IDs

    return render(request, 'report_list.html', {'reports': report_data})

@login_required
def edit_report(request, id):
    report = get_object_or_404(Activity, id=id)

    if request.method == 'POST':
        print("Form submitted")
        form = ActivityForm(request.POST, instance=report)
        if form.is_valid():
            print("Form is valid")
            # Convert "HH:MM" to minutes if necessary
            hours, minutes = map(int, form.cleaned_data['time_spent'].split(':'))
            report.time_spent = hours * 60 + minutes  # Store in the desired format
            report.date = form.cleaned_data['date']  # Update date if needed
            report.save()  # Save the updated report
            return redirect('report_list')  # Ensure this name matches your URL patterns
    else:
      form = ActivityForm(instance=report)
      return render(request, 'edit_report.html', {'form': form, 'report': report})
@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Activity, id=report_id)
    print(f"Request Method: {request.method}")
    print(f"Report ID: {report_id}")
    if report.user != request.user:
        messages.error(request, "You do not have permission to delete this report.")
        return redirect('report_list')
    if request.method == 'POST':
        report.delete()  
        messages.success(request, 'Report successfully deleted!')
        return redirect('report_list')
    messages.error(request, "Invalid request method.")
    return redirect('report_list')

@login_required
def add_rv(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        print(form.errors) 
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user  
            person.save()
            print('Person saved:', person)  
            messages.success(request, 'Person record added successfully.')
            return redirect('rv_list')
        else:
            print('Form is not valid:', form.errors)
    else:
        form = PersonForm()
    
    return render(request, 'add_rv.html', {'form': form})

@login_required
def rv_list(request):
    persons = Person.objects.filter(user=request.user)  # Filter persons by the logged-in user
    return render(request, 'rv_list.html', {'persons': persons})
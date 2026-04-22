from io import BytesIO

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from .forms import RegisterForm, TripForm
from .models import Trip
from .utils import estimate_cost, generate_itinerary, get_weather


def home(request):
    latest_trips = Trip.objects.select_related('user').order_by('-created_at')[:6]
    return render(request, 'home.html', {'latest_trips': latest_trips})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Logged in successfully.')
        return redirect('dashboard')

    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    generated_trip = None

    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user

            trip.itinerary = generate_itinerary(
                destination=trip.destination,
                days=trip.days,
                mood=trip.mood,
                group_type=trip.group_type,
                budget=trip.budget,
            )
            trip.weather_info = get_weather(trip.destination)
            trip.estimated_cost = estimate_cost(
                trip.days,
                trip.budget,
                trip.group_type,
            )
            trip.save()

            generated_trip = trip
            messages.success(request, 'Trip generated and saved successfully.')
            form = TripForm()
    else:
        form = TripForm()

    return render(
        request,
        'dashboard.html',
        {
            'form': form,
            'trips': trips,
            'generated_trip': generated_trip,
        },
    )


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    return render(request, 'trip_detail.html', {'trip': trip})


@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted successfully.')
    return redirect('dashboard')


@login_required
def download_trip_pdf(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    width, height = 595, 842
    y = height - 50

    def draw_wrapped(
        text,
        font_name='Helvetica',
        font_size=11,
        indent=50,
        max_width=500,
        line_height=16,
    ):
        nonlocal y
        p.setFont(font_name, font_size)

        words = text.split()
        current_line = ''

        for word in words:
            test_line = f'{current_line} {word}'.strip()
            if stringWidth(test_line, font_name, font_size) <= max_width:
                current_line = test_line
            else:
                if y < 50:
                    p.showPage()
                    y = height - 50
                    p.setFont(font_name, font_size)

                p.drawString(indent, y, current_line)
                y -= line_height
                current_line = word

        if current_line:
            if y < 50:
                p.showPage()
                y = height - 50
                p.setFont(font_name, font_size)

            p.drawString(indent, y, current_line)
            y -= line_height

    p.setFont('Helvetica-Bold', 18)
    p.drawString(50, y, f'Trip Plan for {trip.destination}')
    y -= 30

    header_lines = [
        f'Days: {trip.days}',
        f'Mood: {trip.get_mood_display()}',
        f'Group Type: {trip.get_group_type_display()}',
        f'Budget: INR {trip.budget}',
        f'Weather: {trip.weather_info}',
        f'Estimated Cost: {trip.estimated_cost}',
    ]

    for line in header_lines:
        draw_wrapped(line)

    y -= 10
    p.setFont('Helvetica-Bold', 14)
    p.drawString(50, y, 'Itinerary')
    y -= 20

    for paragraph in trip.itinerary.split('\n'):
        if paragraph.strip():
            draw_wrapped(paragraph.strip())
        else:
            y -= 8

    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="trip_{trip.destination}.pdf"'
    return response
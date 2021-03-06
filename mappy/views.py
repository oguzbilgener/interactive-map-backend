"""
I'm doing REST for now, but maybe GraphQL would be a better fit for the frontend?
"""

from django.shortcuts import render, redirect
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.forms import UserCreationForm
from .models import State, Shape, Event
from .serializers import StateSerializer, ShapeSerializer
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

class StateViewSet(ReadOnlyModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()


class ShapeViewSet(ReadOnlyModelViewSet):
    serializer_class = ShapeSerializer
    queryset = Shape.objects.all()

    def get_queryset(self):
        queryset = Shape.objects.all()
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(start_date__lte=date, end_date__gte=date)
        return queryset


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/admin/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

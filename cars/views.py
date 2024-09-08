from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import CarForm, CommentForm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CarSerializer, CommentSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        car = self.get_object()
        comments = car.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        car = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(car=car, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    comments = car.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
            return redirect('car_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments, 'comment_form': comment_form})


@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form})


@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user != car.owner:
        return redirect('car_list')
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            car = form.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_form.html', {'form': form})


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user == car.owner:
        if request.method == 'POST':
            car.delete()
            return redirect('car_list')
    return render(request, 'cars/car_confirm_delete.html', {'car': car})

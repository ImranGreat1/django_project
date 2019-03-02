from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PDF_UploadForm
from .models import PDF_Files


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def handouts_pdf(request):
    if request.method == 'POST':
        form = PDF_UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('handouts_pdf')
    else:
        form = PDF_UploadForm()
        return render(request, 'users/handouts_pdf.html', {'form': form})


def pdf_list_view(request):
    pdf_list = PDF_Files.objects.all()
    return render(request, 'users/pdf_list.html', {'pdf_list': pdf_list})

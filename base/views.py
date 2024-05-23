from django.shortcuts import render, redirect
from .models import CustomUser, Doctor, Hospital, Emergency, DocInHospital, Appointment
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        gender = request.POST['gender']
        age = request.POST['age']
        contact = request.POST['contact']
        user_ins = CustomUser(username=username, gender=gender, contact=contact, age=age)
        user_ins.set_password(password)
        user_ins.save()
        return redirect('home')
    return render(request, 'user_register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def view_doc_and_hospital(request):
    context = {}
    if request.method == 'POST':
        query = request.POST['query']
        
        doc_ins = Doctor.objects.get(name = query)
        if doc_ins is None:
            hosp_ins = Hospital.objects.get(name = query)
            if hosp_ins is None:
                return HttpResponse("<p>Enter a Valid Query</p>")
            doc_in_hosp = DocInHospital.objects.filter(hospital = hosp_ins)
            context['doc_in_hosp'] = doc_in_hosp
            return render(request, 'doc_and_host.html', context=context)
        doc_in_hosp = DocInHospital.objects.filter(doctor = doc_ins)
        context['doc_in_hosp'] = doc_in_hosp
        return render(request, 'doc_and_host.html', context=context)
    return render(request, 'doc_and_host.html', context)

def appoint_emergency(request):
    context = {}
    
    if request.user.is_authenticated:
        hosp_ins_list = [hosp.name for hosp in Hospital.objects.all()]
        context['hosp_list'] = hosp_ins_list
        if request.method == 'POST':
            hospital_name = request.POST['hospital_name']
            patient_name = request.POST['patient_name']
            emergency = request.POST['emergency']
            description = request.POST['description']
            hosp_ins = Hospital.objects.get(name = hospital_name)

            curr_user = request.user
            emergency_ins = Emergency(hospital=hosp_ins,  user=curr_user,
                                    patient_name=patient_name, emergency=emergency, 
                                    description=description)
            emergency_ins.save()
            request.session['success_message'] = 'Your Emergency Appointment is Successfully Added!'
            return redirect('home')
        
        return render(request, 'appoint_emergency.html', context)
    return HttpResponse("<strong>User Not Signed In</strong>")

def search_doctor(request):
    context = {}
    all_docs = Doctor.objects.all()
    context['all_docs'] = all_docs
    if request.method == 'POST':
        q = request.POST['q']
        doctor_list = Doctor.objects.filter(Q(name__icontains=q) | Q(speciality__icontains = q))
        context['all_docs'] = doctor_list
        return render(request, 'search_doctor.html', context)
    return render(request, 'search_doctor.html', context)

def search_hospital(request):
    context = {}
    all_hosp = Hospital.objects.all()
    context['all_hosp'] = all_hosp
    if request.method == 'POST':
        q = request.POST['q']
        hospital_list = Hospital.objects.filter(Q(name__icontains=q) | Q(city__icontains=q) )
        context['all_hosp'] = hospital_list
        return render(request, 'search_hospital.html', context)
    return render(request, 'search_hospital.html', context)

def create_appointment(request):
    context = {}
    if request.user.is_authenticated:
        all_doc = [doc.name for doc in Doctor.objects.all()]
        all_hosp = [hosp.name for hosp in Hospital.objects.all()]
        context['all_hosp'] = all_hosp
        context['all_doc'] = all_doc
        if request.method == 'POST':
            doctor_name = request.POST['doctor_name']
            hospital_name = request.POST['hospital_name']
            patient_name = request.POST['patient_name']
            description = request.POST['description']
            appointment_date = request.POST['appointment_date']

            doc_ins = Doctor.objects.get(name=doctor_name)
            hosp_ins = Hospital.objects.get(name = hospital_name)

            validation = DocInHospital(doctor = doc_ins, hospital=hosp_ins)
            if validation is None:
                return HttpResponse("<strong>Doctor isnt available at this hospital</strong>")

            curr_user = request.user
            appointment_ins = Appointment(hospital=hosp_ins, doctor=doc_ins, user=curr_user,
                                    patient_name=patient_name,
                                    description=description, appointment_date=appointment_date)
            appointment_ins.save()
            request.session['success_message'] = 'Your Appointment is Successfully Added!'
            return redirect('home')
        
        return render(request, 'create_appointment.html', context)
    return HttpResponse("<strong>User Not Signed In</strong>")

def list_appointment(request):
    context = {}
    if request.user.is_authenticated:
        curr_user = request.user
        appointment_list = Appointment.objects.filter(user=curr_user)
        emergency_list = Emergency.objects.filter(user=curr_user)
        context['emergency_list'] = emergency_list
        context['appointment_list'] = appointment_list
        return render(request, 'appointment_list.html', context)
    return HttpResponse("<strong>You are not authenticated</strong>")

def delete_appointment(request, appointment_id):
    appoint_ins = Appointment.objects.get(id=appointment_id)
    appoint_ins.delete()
    request.session['success_message'] = 'Your Appointment is Deleted'
    return redirect('home')


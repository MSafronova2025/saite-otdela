from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Request, NeedsRequest, RepairRequest, BuildingCondition, College
from django.contrib import messages
from .utils import admin_required, manager_required, client_required

def index(request):
    return render(request, 'index.html')

def monitoring_needs(request):
    needs = NeedsRequest.objects.select_related('college').all()
    return render(request, 'monitoring_needs.html', {
        'needs': needs,
        'page_title': 'Мониторинг потребностей колледжей'
    })

def contacts(request):
    return render(request, 'contacts.html', {'page_title': 'Контакты'})


def repair_needs(request):
    repairs = RepairRequest.objects.select_related('college').all()
    return render(request, 'repair_needs.html', {
        'repairs': repairs,
        'page_title': 'Ремонтно-эксплуатационные нужды колледжей'
    })

def technical_state(request):
    conditions = BuildingCondition.objects.select_related('college').all()
    return render(request, 'technical_state.html', {
        'conditions': conditions,
        'page_title': 'Техническое состояние зданий колледжей'
    })

def projects(request):
    return render(request, 'projects.html', {'page_title': 'Проекты и программы'})

def barrier_free(request):
    return render(request, 'barrier_free.html', {'page_title': 'Безбарьерная среда'})

def fire_safety(request):
    return render(request, 'fire_safety.html', {'page_title': 'Пожарная безопасность'})

def database(request):
    colleges = College.objects.all()
    return render(request, 'database.html', {
        'colleges': colleges,
        'page_title': 'Банк данных объектов колледжей'
    })

def reports(request):
    return render(request, 'reports.html', {'page_title': 'Отчеты и аналитика'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html', {'page_title': 'Вход'})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = CustomUser.objects.create_user(username=username, password=password, role=role)
        messages.success(request, 'Регистрация успешна. Теперь войдите.')
        return redirect('login')
    return render(request, 'register.html', {'page_title': 'Регистрация'})


def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from .models import CustomUser


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role == 'admin':
        return render(request, 'admin_profile.html', {'user': request.user})
    elif request.user.role == 'manager':
        return render(request, 'manager_profile.html', {'user': request.user})
    elif request.user.role == 'client':
        return render(request, 'client_profile.html', {'user': request.user})
    else:
        return redirect('login')


@admin_required
def admin_only_page(request):
    return render(request, 'admin_page.html')

@manager_required
def view_all_requests(request):
    requests = Request.objects.all().order_by('-created_at')  # Последние сверху
    return render(request, 'all_requests.html', {'requests': requests, 'page_title': 'Все заявки'})

@client_required
def client_only_page(request):
    return render(request, 'client_page.html')

@client_required
def submit_request_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Request.objects.create(user=request.user, title=title, description=description)
        return redirect('profile')
    return render(request, 'submit_request.html')

@manager_required
def update_request_status(request, request_id):
    req = Request.objects.get(id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        req.status = new_status
        req.save()
        return redirect('all_requests')

    return render(request, 'update_request_status.html', {'req': req, 'page_title': 'Изменение статуса заявки'})

@client_required
def my_requests_view(request):
    my_requests = Request.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_requests.html', {'my_requests': my_requests, 'page_title': 'Мои заявки'})


from .forms import CollegeForm

# Просмотр всех колледжей с возможностью редактирования
@manager_required
def manage_colleges(request):
    colleges = College.objects.all()
    return render(request, 'manage_colleges.html', {
        'colleges': colleges,
        'page_title': 'Управление колледжами'
    })

# Добавление колледжа
@manager_required
def add_college(request):
    if request.method == 'POST':
        form = CollegeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_colleges')
    else:
        form = CollegeForm()
    return render(request, 'add_edit_college.html', {
        'form': form,
        'page_title': 'Добавить колледж'
    })

# Редактирование колледжа
@manager_required
def edit_college(request, college_id):
    college = College.objects.get(id=college_id)
    if request.method == 'POST':
        form = CollegeForm(request.POST, instance=college)
        if form.is_valid():
            form.save()
            return redirect('manage_colleges')
    else:
        form = CollegeForm(instance=college)
    return render(request, 'add_edit_college.html', {
        'form': form,
        'page_title': 'Редактировать колледж'
    })

# Удаление колледжа
@manager_required
def delete_college(request, college_id):
    college = College.objects.get(id=college_id)
    college.delete()
    return redirect('manage_colleges')

from .forms import NeedsRequestForm

# Просмотр всех потребностей
@manager_required
def manage_needs(request):
    needs = NeedsRequest.objects.select_related('college').all()
    return render(request, 'manage_needs.html', {
        'needs': needs,
        'page_title': 'Управление потребностями колледжей'
    })

# Добавление потребности
@manager_required
def add_need(request):
    if request.method == 'POST':
        form = NeedsRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_needs')
    else:
        form = NeedsRequestForm()
    return render(request, 'add_edit_need.html', {
        'form': form,
        'page_title': 'Добавить потребность'
    })

# Редактирование потребности
@manager_required
def edit_need(request, need_id):
    need = NeedsRequest.objects.get(id=need_id)
    if request.method == 'POST':
        form = NeedsRequestForm(request.POST, instance=need)
        if form.is_valid():
            form.save()
            return redirect('manage_needs')
    else:
        form = NeedsRequestForm(instance=need)
    return render(request, 'add_edit_need.html', {
        'form': form,
        'page_title': 'Редактировать потребность'
    })

# Удаление потребности
@manager_required
def delete_need(request, need_id):
    need = NeedsRequest.objects.get(id=need_id)
    need.delete()
    return redirect('manage_needs')

# Просмотр всех ремонтных заявок
@manager_required
def manage_repairs(request):
    repairs = RepairRequest.objects.select_related('college').all()
    return render(request, 'manage_repairs.html', {
        'repairs': repairs,
        'page_title': 'Управление ремонтными заявками колледжей'
    })

# Добавление заявки на ремонт
@manager_required
def add_repair(request):
    if request.method == 'POST':
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_repairs')
    else:
        form = RepairRequestForm()
    return render(request, 'add_edit_repair.html', {
        'form': form,
        'page_title': 'Добавить заявку на ремонт'
    })

# Редактирование заявки на ремонт
@manager_required
def edit_repair(request, repair_id):
    repair = RepairRequest.objects.get(id=repair_id)
    if request.method == 'POST':
        form = RepairRequestForm(request.POST, instance=repair)
        if form.is_valid():
            form.save()
            return redirect('manage_repairs')
    else:
        form = RepairRequestForm(instance=repair)
    return render(request, 'add_edit_repair.html', {
        'form': form,
        'page_title': 'Редактировать заявку на ремонт'
    })

# Удаление заявки на ремонт
@manager_required
def delete_repair(request, repair_id):
    repair = RepairRequest.objects.get(id=repair_id)
    repair.delete()
    return redirect('manage_repairs')

from .forms import RequestForm

@client_required
def submit_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.save()
            return redirect('profile')
    else:
        form = RequestForm()
    return render(request, 'submit_request.html', {
        'form': form,
        'page_title': 'Подать заявку'
    })

@manager_required
def manage_requests(request):
    requests = Request.objects.select_related('user').all().order_by('-created_at')
    return render(request, 'manage_requests.html', {
        'requests': requests,
        'page_title': 'Управление заявками'
    })

@manager_required
def change_request_status(request, request_id, status):
    req = Request.objects.get(id=request_id)
    req.status = status
    req.save()
    return redirect('manage_requests')

@manager_required
def delete_request(request, request_id):
    req = Request.objects.get(id=request_id)
    req.delete()
    return redirect('manage_requests')

@admin_required
def manage_users(request):
    role = request.GET.get('role')
    query = request.GET.get('q')
    users = CustomUser.objects.exclude(id=request.user.id)
    if role:
        users = users.filter(role=role)
    if query:
        users = users.filter(username__icontains=query) | users.filter(email__icontains=query)
    return render(request, 'manage_users.html', {
        'users': users,
        'page_title': 'Управление пользователями'
    })


@admin_required
def change_user_role(request, user_id, role):
    user = CustomUser.objects.get(id=user_id)
    if role in ['admin', 'manager', 'client']:
        user.role = role
        user.save()
    return redirect('manage_users')

@admin_required
def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect('manage_users')


@admin_required
def generate_reports(request):
    needs = NeedsRequest.objects.select_related('college').all()
    repairs = RepairRequest.objects.select_related('college').all()
    conditions = BuildingCondition.objects.select_related('college').all()

    return render(request, 'generate_reports.html', {
        'needs': needs,
        'repairs': repairs,
        'conditions': conditions,
        'page_title': 'Формирование отчетов'
    })

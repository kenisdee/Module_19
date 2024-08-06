from django.db import transaction
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Buyer, Game


# Псевдо-список существующих пользователей
existing_users = ["user1", "user2", "user3"]

def sign_up_by_django(request):
    info = {}
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            # Проверка наличия пользователя в базе данных
            if Buyer.objects.filter(name=username).exists():
                info['error'] = "Пользователь уже существует."
            elif password != repeat_password:
                info['error'] = "Пароли не совпадают."
            elif age < 18:
                info['error'] = "Вы должны быть старше 18."
            else:
                # Добавление нового пользователя
                Buyer.objects.create(name=username, balance=0.0, age=age)
                info['success'] = f"Приветствуем, {username}!"
                return redirect('home')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = UserRegisterForm()

    info['form'] = form
    return render(request, 'registration_page.html', info)

def sign_up_by_html(request):
    info = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age')) if request.POST.get('age').isdigit() else 0

        if username in existing_users:
            info['error'] = "Пользователь уже существует."
        elif password != repeat_password:
            info['error'] = "Пароли не совпадают."
        elif age < 18:
            info['error'] = "Вы должны быть старше 18."
        else:
            info['success'] = f"Приветствуем, {username}!"

    return render(request, 'registration_page.html', info)

@transaction.atomic
@transaction.atomic
def create_records(request):
    try:
        # Создание покупателей
        buyer1 = Buyer.objects.create(name='Alice', balance=100.00, age=25)
        buyer2 = Buyer.objects.create(name='Bob', balance=150.00, age=30)
        buyer3 = Buyer.objects.create(name='Charlie', balance=200.00, age=16)

        # Создание игр
        game1 = Game.objects.create(title='Forza Horison 3', cost=50.00, size=2.5, description='Бесконечное лето', age_limited=True)
        game2 = Game.objects.create(title='Forza Horison 4', cost=30.00, size=1.5, description='Каждая погода - благодать', age_limited=False)
        game3 = Game.objects.create(title='Forza Horison 5', cost=40.00, size=2.0, description='Какой Corvette! Какой пейзаж!', age_limited=True)

        # Связывание покупателей с играми с проверкой возраста
        if not game1.age_limited or (buyer1.age >= 18 and buyer2.age >= 18):
            game1.buyer.set([buyer1, buyer2])
        if not game2.age_limited or all(buyer.age >= 18 for buyer in [buyer1, buyer2, buyer3]):
            game2.buyer.set([buyer1, buyer2, buyer3])
        if not game3.age_limited or (buyer1.age >= 18 and buyer2.age >= 18):
            game3.buyer.set([buyer1, buyer2])

    except Exception as e:
        # Обработка исключений
        print(f"An error occurred: {e}")
        return render(request, 'create_records.html', {'message': f'Error: {e}'})

    return render(request, 'create_records.html', {'message': 'Records created successfully'})

def home_view(request):
    return render(request, 'home.html')

def page1_view(request):
    games_list = Game.objects.all()
    context = {'games_list': games_list}
    return render(request, 'page1.html', context)

def page2_view(request):
    data = {
        'selected_game_list': [],
        'total_price': 0
    }
    return render(request, 'page2.html', data)
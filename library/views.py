from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm
from .models import Book, TestCategory, Test, Question, AnswerChoice, TestResult
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'library/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = UserLoginForm()
    return render(request, 'library/login.html', {'form': form})

def home(request):
    return render(request, 'library/home.html')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'library/profile.html', {'form': form})

@login_required(login_url='login')
def book_list(request):
    try:
        books = Book.objects.all()
        return render(request, 'library/book_list.html', {'books': books})
    except Exception as e:
        return render(request, 'library/book_list.html', {'error': str(e)})

@login_required(login_url='login')
def books_by_category(request, category_code):
    books = Book.objects.filter(category=category_code)
    return render(request, 'library/book_list.html', {'books': books, 'category_code': category_code})

@login_required(login_url='login')
def category_tests(request, category_slug):
    category = get_object_or_404(TestCategory, slug=category_slug)
    tests = category.tests.all()
    return render(request, 'library/category_tests.html', {'category': category, 'tests': tests})

@login_required(login_url='login')
def test_categories(request):
    categories = [
        {"name": "💻 Основы программирования", "slug": "basics"},
        {"name": "🌍 Веб-разработка", "slug": "web"},
        {"name": "📱Игры", "slug": "mobile"},
        {"name": "🤖 Искусственный интеллект", "slug": "ai"},
        {"name": "🛠 DevOps и администрирование", "slug": "devops"},
    ]
    return render(request, 'library/test_categories.html', {"categories": categories})

@login_required(login_url='login')
def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.all()
    total_questions = questions.count()

    current_question_index = int(request.POST.get('current_question_index', 0))

    if request.method == 'POST':
        current_question_index += 1

    if current_question_index >= total_questions:
        return redirect('test_result', test_id=test.id)

    question = questions[current_question_index]

    return render(request, 'library/take_test.html', {
        'test': test,
        'question': question,
        'current_question_index': current_question_index,
        'total_questions': total_questions
    })

@login_required(login_url='login')
def test_result(request, test_id):
    test_result = TestResult.objects.filter(user=request.user, test__id=test_id).first()
    test = test_result.test
    questions = test.questions.all()

    correct_answers = [
        {'question': question, 'correct_answer': question.choices.filter(is_correct=True).first()}
        for question in questions
    ]

    return render(request, 'library/test_result.html', {
        'test_result': test_result,
        'correct_answers': correct_answers,
    })

from django.shortcuts import render, get_object_or_404
from .models import Book  # Импортируй свою модель книги

def read_pdf(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/read_pdf.html', {'book': book})

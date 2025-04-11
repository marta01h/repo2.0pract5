from django.db import models
from django.contrib.auth.models import User



class Book(models.Model):
    CATEGORY_CHOICES = [
        ('basics', '💻 Основы программирования'),
        ('algorithms', '📊 Алгоритмы и структуры данных'),
        ('web', '🌍 Веб-разработка'),
        ('mobile', '📱 Мобильная разработка'),
        ('ai', '🤖 Искусственный интеллект'),
        ('devops', '🛠 DevOps и администрирование'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='books/')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='basics')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} скачал {self.book.title} - {self.downloaded_at}"


class TestCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(TestCategory, related_name='tests', on_delete=models.CASCADE)
    duration = models.IntegerField(help_text="Duration of test in minutes")

    def __str__(self):
        return f"Тест по {self.name} в категории {self.category.name}"


class Question(models.Model):
    text = models.CharField(max_length=1024)
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return f"Вопрос: {self.text[:30]}"

class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_correct:
            AnswerChoice.objects.filter(question=self.question, is_correct=True).update(is_correct=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()  # Баллы
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Результат теста для {self.user.username}: {self.score} баллов"

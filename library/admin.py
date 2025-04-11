from django.contrib import admin
from .models import Book, TestCategory, Test, Question, AnswerChoice, TestResult, DownloadHistory

class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True
    inlines = [AnswerChoiceInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerChoiceInline]
    list_display = ('text', 'test')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'category', 'duration')

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('category',)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed_at')
    list_filter = ('test', 'completed_at')

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'downloaded_at')
    list_filter = ('book',)

from django.contrib import admin
from .models import Quiz, Question, Option, StudentAnswer, Subject


class OptionInline(admin.TabularInline):
    model = Option
    extra = 2



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'start_time')
    list_filter = ('teacher', 'start_time')
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','question_text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question_text',)
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id','question__id','question', 'option_text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('option_text',)



@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'selected_option', 'is_correct_display')
    list_filter = ('student', 'question')
    search_fields = ('student__username', 'question__option_text')

    def is_correct_display(self, obj):
        return "✅" if obj.selected_option.is_correct else "❌"

    is_correct_display.short_description = "To‘g‘ri javob"



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
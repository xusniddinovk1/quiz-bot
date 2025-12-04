from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from quizzes.models import StudentAnswer

class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    fields = ('question', 'quiz', 'selected_option', 'is_correct_display')
    readonly_fields = ('question', 'quiz', 'selected_option', 'is_correct_display')
    extra = 0

    def is_correct_display(self, obj):
        return "✅" if obj.selected_option.is_correct else "❌"
    is_correct_display.short_description = "To‘g‘ri javob"

    def quiz(self, obj):
        return obj.question.quiz.title

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'total_quizzes')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    inlines = [StudentAnswerInline]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Roles', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'role', 'password1', 'password2'),
            },
        ),
    )

    def total_quizzes(self, obj):
        total_answers = StudentAnswer.objects.filter(student=obj).count()
        correct_answers = StudentAnswer.objects.filter(student=obj, selected_option__is_correct=True).count()
        return f"{total_answers}/{correct_answers}"  # misol: 20/2

    total_quizzes.short_description = "Savol / To‘g‘ri javob"
    #
    # def total_score(self, obj):
    #     return StudentAnswer.objects.filter(student=obj, selected_option__is_correct=True).count()
    # total_score.short_description = "Jami ball"

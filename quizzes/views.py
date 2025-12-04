
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quiz, Question, Option, Subject, StudentAnswer


class TeacherDashboardView(LoginRequiredMixin, View):
    """
    O'qituvchi dashboardi – faqat teacher roliga ega userlar kiradi.
    """
    def get(self, request):
        if not request.user.is_teacher:
            return redirect("student_dashboard")

        quizzes = Quiz.objects.filter(teacher=request.user)

        context = {
            "quizzes": quizzes
        }
        return render(request, "teacher/teacher_dashboard.html", context)


class QuizCreateView(LoginRequiredMixin, View):
    """
    Yangi quiz yaratish sahifasi
    """
    def get(self, request):
        if not request.user.is_teacher:
            return redirect("student_dashboard")

        subjects = Subject.objects.all()

        return render(request, "teacher/quiz_create.html", {"subjects": subjects})

    def post(self, request):
        if not request.user.is_teacher:
            return redirect("student_dashboard")

        title = request.POST.get("title")
        subject_id = request.POST.get("subject")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        duration = request.POST.get("duration")

        subject = Subject.objects.get(id=subject_id)

        Quiz.objects.create(
            teacher=request.user,
            subject=subject,
            title=title,
            start_time=start_time,
            # end_time=end_time
            duration=int(duration)  # int ga o‘tkazing

        )

        return redirect("teacher_dashboard")


class QuestionCreateView(LoginRequiredMixin, View):
    """
    Quizga savol qo‘shish view'i
    """

    def get(self, request):
        if not request.user.is_teacher:
            return redirect("student_dashboard")

        quizzes = Quiz.objects.filter(teacher=request.user)
        last_quiz_id = request.session.get('last_quiz_id')

        context = {
            "quizzes": quizzes,
            "last_quiz_id": last_quiz_id
        }
        return render(request, "teacher/question_create.html", context)

    def post(self, request):
        if not request.user.is_teacher:
            return redirect("student_dashboard")

        quiz_id = request.POST.get("quiz")
        question_text = request.POST.get("question_text")

        quiz = Quiz.objects.get(id=quiz_id)

        question = Question.objects.create(
            quiz=quiz,
            question_text=question_text
        )
        request.session['last_quiz_id'] = quiz.id

        # Variantlarni olish
        options = request.POST.getlist("options[]")
        correct_option = int(request.POST.get("correct_option"))

        for index, opt_text in enumerate(options):
            Option.objects.create(
                question=question,
                option_text=opt_text,
                is_correct=(index == correct_option)
            )

        quizzes = Quiz.objects.filter(teacher=request.user)
        return render(request, "teacher/question_create.html", {"quizzes": quizzes})

class StudentQuizView(LoginRequiredMixin, View):
    """
    Talaba quizni ko'radi va javob beradi.
    """
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions.all()
        context = {
            "quiz": quiz,
            "questions": questions
        }
        return render(request, "student/student_quiz.html", context)

    def post(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions.all()

        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            if selected_option_id:
                option = Option.objects.get(id=int(selected_option_id))
                # StudentAnswer modeliga yozish
                StudentAnswer.objects.create(
                    student=request.user,
                    question=question,
                    selected_option=option
                )

        messages.success(request, "Javoblaringiz saqlandi!")
        return redirect('student_dashboard')


class StudentDashboardView(View):
    def get(self, request):
        quizzes = Quiz.objects.all()
        # Talabaning ishlagan quizlarini olish
        student_answers = StudentAnswer.objects.filter(student=request.user)
        completed_quiz_ids = student_answers.values_list('question__quiz_id', flat=True).distinct()

        context = {
            "quizzes": quizzes,
            "completed_quiz_ids": completed_quiz_ids,
        }
        return render(request, "student/student_dashboard.html", context)
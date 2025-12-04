from django.urls import path
from .views import TeacherDashboardView, QuizCreateView, QuestionCreateView, StudentDashboardView, StudentQuizView

urlpatterns = [
    path("dashboard/", TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("quiz/create/", QuizCreateView.as_view(), name="quiz_create"),
    path("question/create/", QuestionCreateView.as_view(), name="question_create"),
    path("student/dashboard/", StudentDashboardView.as_view(), name="student_dashboard"),
    path('student/quiz/<int:quiz_id>/', StudentQuizView.as_view(), name='student_quiz'),
]


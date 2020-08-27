"""vle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from adaptivevle import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard', views.dashboard, name='dashboard'),
    path('teacher/units', views.units, name='units'),
    path('teacher/unit/<int:unit_id>', views.unit, name='unit'),
    # path('edit_topic', views.edit_topic, name='edit_topic'),
    # path('teacher/unit/<int:unit_id>/topic/<int:topic_id>/materials', views.materials, name='materials'),
    path('teacher/topic/<int:topic_id>/add_material', views.add_material, name ='add_material'),
    path('teacher/topic/<int:topic_id>/material/<int:material_id>', views.teacher_material, name='teacher_material'),
    path('teacher/unit/<int:unit_id>/topics', views.topics, name='topics'),
    path('teacher/unit/<int:unit_id>/topic/<int:topic_id>', views.topic, name='topic'),
    path('teacher/unit/<int:unit_id>/add_topic', views.add_topic, name='add_topic'),
    path('teacher/topic/<int:topic_id>/add_material/add_video', views.add_video, name='add_video'),
    path('teacher/topic/<int:topic_id>/add_material/add_audio', views.add_audio, name='add_audio'),
    path('teacher/topic/<int:topic_id>/add_material/add_text', views.add_text, name='add_text'),
    path('teacher/topic/<int:topic_id>/add_material/add_image', views.add_image, name='add_image'),
    path('teacher/topic/<int:topic_id>/add_material/add_presentation', views.add_presentation, name='add_presentation'),

    # quiz
    path('teacher/topic/<int:topic_id>/add_quiz', views.add_quiz, name='add_quiz'),
    path('teacher/quiz/<int:quiz_id>/quiz_details', views.quiz_details, name='quiz_details'),
    path('teacher/quiz/<int:quiz_id>/add_quiz_question', views.add_quiz_question, name='add_quiz_question'),
    path('teacher/edit_quiz_question/<int:question_id>', views.edit_quiz_question, name='edit_quiz_question'),
    path('teacher/quiz/<int:quiz_id>/publish', views.publish_quiz, name='publish_quiz'),
    path('teacher/quiz/<int:quiz_id>/hide', views.publish_quiz, name='hide_quiz'),
    path('teacher/quiz/<int:quiz_id>/results', views.quiz_results, name ='quiz_results'),

    # student
    path('student/student_profile', views.student_profile, name='student_profile'),
    path('student/learning_style', views.learning_style_quiz, name='learning_style'),
    path('student/student_units', views.student_units, name='student_units'),
    path('student/student_unit/<int:unit_id>', views.student_unit, name='student_unit'),
    path('student/unit/<int:unit_id>/topic/<int:topic_id>', views.student_topic, name='student_topic'),
    path('student/topic/<int:topic_id>/material/<int:material_id>', views.student_material, name='student_material'),
    path('student/quiz/<int:quiz_id>/student_topic_quiz', views.student_topic_quiz, name='student_topic_quiz'),

    path('', views.home, name='home'),

    # registartion
    path("register/", views.register_student, name="register"),
    path("register_teacher/", views.register_teacher, name="register_teacher"),
    path("register_options", views.register_options, name="register_options"),
    path('', include("django.contrib.auth.urls")),
    path('dashboard', views.dashboard),


]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

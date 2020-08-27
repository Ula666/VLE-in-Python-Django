from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from .forms import AddTopicForm, AddImageForm, AddTextForm, AddAudioForm, AddVideoForm, QuizQuestionForm, QuizForm, \
    CommentForm, AddPresentationForm
from adaptivevle.models import Profile
from adaptivevle.models import Unit, Topic, Material, Quiz, QuizQuestion, Response, Comment, get_kind_by_style
from django.shortcuts import redirect
from django.shortcuts import render as dj_render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import quiz, topic_quiz
from django.db.models import Count
import markdown


# render view which is loaded as a first render, then dj_render
def render(request, template_name, context=None):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
    else:
        profile = None

    if context is None:
        context = {'profile': profile}  # stworz nowy slownik
    else:
        context['profile'] = profile  # dodaj klucz do istniejacego slownika
    return dj_render(request, template_name, context)


# student decorator
def student_required(v):
    def wrapper(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user, role=Profile.STUDENT)
        except Profile.DoesNotExist:
            return HttpResponseForbidden()
        else:
            return v(request, *args, **kwargs)

    return wrapper


# teacher decorator
def teacher_required(v):
    def wrapper(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user, role=Profile.TEACHER)
        except Profile.DoesNotExist:
            return HttpResponseForbidden()
        else:
            return v(request, *args, **kwargs)

    return wrapper


# registration
def register_student(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            with transaction.atomic():
                user = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                )
                profile = Profile.objects.create(role=Profile.STUDENT, user=user)
                print(profile)
                # redirects to login screen
            return redirect("login")

    # if details are not correct returns empty form
    return render(request, "register/register.html", {"form": form})


def register_teacher(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            with transaction.atomic():
                user = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email'],
                    is_active=False
                )
                profile = Profile.objects.create(role=Profile.TEACHER, user=user)
                print(profile)
                # redirects to login screen
            return redirect("login")

    # if details are not correct returns empty form
    return render(request, "register/register.html", {"form": form})


def register_options(request):
    return render(request, 'register_options.html')


# redirect
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == Profile.STUDENT:
        return redirect("student/student_units")
    elif profile.role == Profile.TEACHER:
        return redirect("teacher/units")
    else:
        raise ValueError('Profile error')


# teacher's access
# display units page
@login_required
@teacher_required
def units(request):
    units = Unit.objects.all()
    return render(request, 'teacher/units.html', {'units': units})


# seperate unit page
@login_required
@teacher_required
def unit(request, unit_id):
    unit = Unit.objects.filter(id=unit_id).first()
    topics = Topic.objects.all()
    return render(request, 'teacher/unit.html', {'unit': unit, 'topics': topics})


#topic page for teacher
@login_required
@teacher_required
def topic(request, unit_id, topic_id):
    topic = Topic.objects.filter(id=topic_id, unit_id=unit_id).first()
    if topic is None:
        return HttpResponseNotFound()
    materials = Material.objects.filter(topic=topic)
    quizes = Quiz.objects.filter(topic=topic)

    quizes_info = []

    for quiz in quizes:
        user_counters = list(
            Response.objects
                .filter(quizquestion__quiz=quiz)
                .values('user')
                .annotate(count=Count('user'))
        )

        quizes_info.append([quiz, len(user_counters)])
    context={'topic': topic,
             'materials': materials,
             'quizes_info': quizes_info}

    return render(request, 'teacher/topic.html', context)


# to see student's quiz results
@login_required
def quiz_results(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if quiz is None:
        return HttpResponseNotFound()

    user_counters = list(
        Response.objects
            .filter(quizquestion__quiz=quiz)
            .values('user')
            .annotate(count=Count('user'))
    )

    quiz_results_info = []

    for user_counter in user_counters:
        user_id = user_counter['user']
        responses = list(Response.objects.filter(user_id=user_id, quizquestion__quiz=quiz))

        if responses:
            user = responses[0].user
        else:
            user = None
        correct_counter = 0
        for response in responses:
            if response.is_correct():
                correct_counter += 1

        quiz_results_info.append([user, correct_counter, len(responses)])

    return render(request, 'teacher/quiz_results.html', {'quiz': quiz, 'quiz_results_info': quiz_results_info, 'topic': quiz.topic})


#page where all topics are displayed
@login_required
@teacher_required
def topics(request, unit_id):
    unit = Unit.objects.filter(id=unit_id).first()
    if unit is None:
        return HttpResponseNotFound()

    topics = Topic.objects.filter(unit=unit)
    return render(request, 'teacher/topics.html', {'topics': topics, 'unit': unit})


# add topic page
@login_required
@teacher_required
def add_topic(request, unit_id):
    unit = Unit.objects.filter(id=unit_id).first()
    if unit is None:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = AddTopicForm(request.POST)
        if form.is_valid():
            topic = Topic()
            topic.name = form.cleaned_data['name']
            topic.date_created = timezone.now()
            topic.unit = unit
            topic.save()
            return redirect('topic', topic_id=topic.id, unit_id=unit.id)
    else:
        form = AddTopicForm()
    return render(request, 'teacher/add_topic.html', {'form': form})


# add material page
@login_required
@teacher_required
def add_material(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    return render(request, 'teacher/add_material.html', {'topic': topic})


# to process comments, this is not a view
def _process_comment(request, template_name, context, success_url):
    comments = Comment.objects.filter(material=context['material'])
    form = CommentForm()
    context['form'] = form
    context['comments'] = comments
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.message = form.cleaned_data['message']
            comment.date_created = timezone.now()
            comment.user = request.user
            comment.material = context['material']
            comment.save()
            return redirect(success_url)
    return render(request, template_name, context)


# markdown
def _process_content(request, context):
    material = context['material']
    if material.kind == Material.KIND_TEXT:
        html_content = markdown.markdown(material.content)
        context['html_content']= html_content





@login_required
@teacher_required
def teacher_material(request, topic_id, material_id):
    material = Material.objects.filter(id=material_id, topic_id=topic_id).first()
    if material is None:
        return HttpResponseNotFound()
    material = Material.objects.filter(id=material_id).first()
    if material.kind == Material.KIND_TEXT:
        template_name = "teacher/material_text.html"
    elif material.kind == Material.KIND_AUDIO:
        template_name = "teacher/material_audio.html"
    elif material.kind == Material.KIND_PICTURE:
        template_name = "teacher/material_picture.html"
    elif material.kind == Material.KIND_VIDEO:
        template_name = "teacher/material_video.html"
    elif material.kind == Material.KIND_PRST:
        template_name = "teacher/material_presentation.html"
    else:
        raise ValueError()
    if material.kind == Material.KIND_VIDEO:
        url = material.content.replace('watch?v=', 'embed/')
    elif material.kind == Material.KIND_PRST:
        url = material.content.replace('watch?v=', 'embed/')
    else:
        url = ""
    context = {
        'material': material,
        'url': url,
    }
    success_url = reverse('teacher_material', kwargs={'material_id': material.id, 'topic_id': topic_id})
    _process_content(request, context)
    return _process_comment(request, template_name, context, success_url)


# add new video file
@login_required
@teacher_required
def add_video(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = AddVideoForm(request.POST, request.FILES)

        if form.is_valid():
            material = Material()
            material.name = form.cleaned_data['name']
            material.content = form.cleaned_data['content']
            material.kind = Material.KIND_VIDEO
            material.date_created = timezone.now()
            material.topic = topic
            material.save()
            url = reverse('topic', kwargs={'topic_id': topic.id, "unit_id": topic.unit_id})
            return redirect(url)

    else:
        form = AddVideoForm()
    return render(request, 'teacher/material_add_video.html', {'form': form})


# add new presentation file
@login_required
@teacher_required
def add_presentation(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = AddPresentationForm(request.POST, request.FILES)

        if form.is_valid():
            material = Material()
            material.name = form.cleaned_data['name']
            material.content = form.cleaned_data['content']
            material.kind = Material.KIND_PRST
            material.date_created = timezone.now()
            material.topic = topic
            material.save()
            url = reverse('topic', kwargs={'topic_id': topic.id, "unit_id": topic.unit_id})
            return redirect(url)

    else:
        form = AddPresentationForm()
    return render(request, 'teacher/material_add_presentation.html', {'form': form})


# add new audio file
@login_required
@teacher_required
def add_audio(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = AddAudioForm(request.POST, request.FILES)

        if form.is_valid():
            material = Material()
            material.name = form.cleaned_data['name']
            material.file = form.cleaned_data['file']
            material.kind = Material.KIND_AUDIO
            material.date_created = timezone.now()
            material.topic = topic
            material.save()
            url = reverse('topic', kwargs={'topic_id': topic.id, "unit_id": topic.unit_id})
            return redirect(url)

    else:
        form = AddAudioForm()
    return render(request, 'teacher/material_add_audio.html', {'form': form})


# add new text file
@login_required
@teacher_required
def add_text(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = AddTextForm(request.POST)

        if form.is_valid():
            material = Material()
            material.name = form.cleaned_data['name']
            material.content = form.cleaned_data['content']
            material.kind = Material.KIND_TEXT
            material.date_created = timezone.now()
            material.topic = topic
            material.save()
            url = reverse('topic', kwargs={'topic_id': topic.id, "unit_id": topic.unit_id})
            return redirect(url)

    else:
        form = AddTextForm()
    return render(request, 'teacher/material_add_text.html', {'form': form})


# add new image file
@login_required
@teacher_required
def add_image(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)

        if form.is_valid():
            material = Material()
            material.name = form.cleaned_data['name']
            material.file = form.cleaned_data['file']
            material.kind = Material.KIND_PICTURE
            material.date_created = timezone.now()
            material.topic = topic
            material.save()
            url = reverse('topic', kwargs={'topic_id': topic.id, "unit_id": topic.unit_id})
            return redirect(url)
    else:
        form = AddImageForm()
    return render(request, 'teacher/material_add_image.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


# add quiz to a topic
@login_required
@teacher_required
def add_quiz(request, topic_id):
    topic = Topic.objects.filter(id=topic_id).first()
    if topic is None:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = Quiz()
            quiz.name = form.cleaned_data['name']
            quiz.description = form.cleaned_data['description']
            quiz.date_created = timezone.now()
            quiz.topic = topic
            quiz.save()
            url = reverse('quiz_details', kwargs={'quiz_id': quiz.id})
            return redirect(url)
    else:
            form = QuizForm()
    return render(request, 'teacher/add_quiz.html', {'form': form})


# page where teacher can see the quiz details
@login_required
@teacher_required
def quiz_details(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if quiz is None:
        return HttpResponseNotFound()
    questions = QuizQuestion.objects.filter(quiz=quiz)
    return render(request, 'teacher/quiz_details.html', {'quiz': quiz, 'questions': questions})


# add questions to quiz page
@login_required
@teacher_required
def add_quiz_question(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if quiz is None:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            question = QuizQuestion()
            question.quiz = quiz
            question.text = form.cleaned_data['text']
            question.correct = form.cleaned_data['correct']
            question.answer_1 = form.cleaned_data['answer_1']
            question.answer_2 = form.cleaned_data['answer_2']
            question.answer_3 = form.cleaned_data['answer_3']
            question.answer_4 = form.cleaned_data['answer_4']
            question.save()
            url = reverse('quiz_details', kwargs={'quiz_id': quiz.id})
            return redirect(url)
    else:
        form = QuizQuestionForm()
    return render(request, 'teacher/add_quiz_question.html', {'form': form})


# to edit quiz questions
@login_required
@teacher_required
def edit_quiz_question(request, question_id):
    # Load up an instance
    question = QuizQuestion.objects.get(id=question_id)
    if question is None:
         return HttpResponseNotFound()

    if request.method == "POST":
        # Declare a ModelForm with the instance
        form = QuizQuestionForm(request.POST, instance=question)
        if form.is_valid():
            # here just editing
            question.text = form.cleaned_data['text']
            question.correct = form.cleaned_data['correct']
            question.answer_1 = form.cleaned_data['answer_1']
            question.answer_2 = form.cleaned_data['answer_2']
            question.answer_3 = form.cleaned_data['answer_3']
            question.answer_4 = form.cleaned_data['answer_4']
            question.save()
            url = reverse('quiz_details', kwargs={'quiz_id': question.quiz_id})
            return redirect(url)
    else:
        form = QuizQuestionForm(instance=question)
        return render(request, 'teacher/edit_quiz_question.html', {'form':form})


#to publish a topic_quiz
@login_required
@teacher_required
def publish_quiz(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if quiz is None:
        return HttpResponseNotFound()
    quiz.is_draft = False
    quiz.save()
    url = reverse('quiz_details', kwargs={'quiz_id':quiz.id})
    return redirect(url)


#to hide a topic_quiz
@login_required
@teacher_required
def hide_quiz(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if quiz is None:
        return HttpResponseNotFound()
    quiz.is_draft = True
    quiz.save()
    url = reverse('quiz_details', kwargs={'quiz_id':quiz.id})
    return redirect(url)


# home screen
def home(request):
    return render(request, "home.html",
                  {"message": "Please enter your University username and password."})


# pages available for student
@login_required
@student_required
def learning_style_quiz(request):
    profile = Profile.objects.get(user=request.user, role=Profile.STUDENT)
    quiz_form = quiz.render_quiz(quiz.learning_style_quiz, request.POST)
    errors = None
    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('question_0'))
        if quiz.is_valid(quiz.learning_style_quiz, request.POST):
            learning_style = quiz.process_quiz(quiz.learning_style_quiz, request.POST)
            print(learning_style)
            profile.learning_style = learning_style.get_main_style_code()
            profile.save()
            url = reverse('student_profile')
            return redirect(url)
        else:
            errors = True

    return render(request, 'student/learning_style.html', {'quiz_form': quiz_form, 'errors': errors})


# topic quiz
@login_required
@student_required
def student_topic_quiz(request, quiz_id):
    # security option, so the student can fill in the quiz only once
    quiz = Quiz.objects.filter(id=quiz_id, is_draft=False).first()
    if quiz is None:
        return HttpResponseNotFound()

    topic= Topic.objects.filter(id=quiz.topic_id).first()
    if Response.objects.filter(user=request.user, quizquestion__quiz=quiz).exists():
        url = reverse('student_topic', kwargs={'topic_id':topic.id, 'unit_id':topic.unit_id })
        return redirect(url)
    questions = QuizQuestion.objects.filter(quiz=quiz)
    quiz_form = topic_quiz.render_quiz(questions, request.POST)
    errors = None
    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('question_0'))
        if topic_quiz.is_valid(questions, data=request.POST):
            topic_quiz.save_quiz_responses(questions, request.POST, request.user)
            url = reverse('student_topic', kwargs={'topic_id':quiz.topic_id, 'unit_id': topic.unit_id})
            return redirect(url)
        else:
            errors = True

    return render(request, 'student/student_topic_quiz.html', {'quiz_form': quiz_form, 'errors': errors})


@login_required
@student_required
def student_profile(request):
    profile = Profile.objects.get(user=request.user, role=Profile.STUDENT)
    return render(request, 'student/student_profile.html', {'profile': profile})


@login_required
@student_required
def student_units(request):
    units = Unit.objects.all()
    return render(request, 'student/student_units.html', {'units': units})


@login_required
@student_required
def student_unit(request, unit_id):
    unit = Unit.objects.filter(id=unit_id).first()
    topics = Topic.objects.all()
    return render(request, 'student/student_unit.html', {'unit': unit, 'topics': topics})


# student's topic page
@login_required
@student_required
def student_topic(request, unit_id, topic_id):
    topic = Topic.objects.filter(id=topic_id, unit_id=unit_id).first()
    if topic is None:
        return HttpResponseNotFound()

    profile = Profile.objects.get(user=request.user, role=Profile.STUDENT)
    recommended_kind = get_kind_by_style(profile.learning_style)

    if recommended_kind is None:
        recommended_kind = Profile.STYLE_MULTIMODAL

    if recommended_kind == Profile.STYLE_MULTIMODAL:
        recommended_materials = []
        other_materials = Material.objects.filter(topic=topic)
    else:
        recommended_materials = Material.objects.filter(topic=topic, kind=recommended_kind)
        other_materials = Material.objects.filter(topic=topic).exclude(kind=recommended_kind)

    quizes = Quiz.objects.filter(topic=topic, is_draft=False)

    quizes_info = []

    for quiz in quizes:
        responses = list(Response.objects.filter(user=request.user, quizquestion__quiz=quiz))
        correct_counter = 0
        for response in responses:
            if response.is_correct():
                correct_counter += 1
        quizes_info.append([quiz, correct_counter, len(responses)])

    context = {
        'topic': topic,
        'recommended_materials': recommended_materials,
        'other_materials': other_materials,
        'quizes_info': quizes_info,
    }
    return render(request, 'student/student_topic.html', context)


# student's materials
@login_required
@student_required
def student_material(request, topic_id, material_id):
    material = Material.objects.filter(id=material_id, topic_id=topic_id).first()
    if material is None:
        return HttpResponseNotFound()
    material = Material.objects.filter(id=material_id).first()
    comment = Comment.objects.all()
    if material.kind == Material.KIND_TEXT:
        template_name = "teacher/material_text.html"
    elif material.kind == Material.KIND_AUDIO:
        template_name = "teacher/material_audio.html"
    elif material.kind == Material.KIND_PICTURE:
        template_name = "teacher/material_picture.html"
    elif material.kind == Material.KIND_VIDEO:
        template_name = "teacher/material_video.html"
    elif material.kind == Material.KIND_PRST:
        template_name = "teacher/material_presentation.html"
    else:
        raise ValueError()
    if material.kind == Material.KIND_VIDEO:
        url = material.content.replace('watch?v=', 'embed/')
    elif material.kind == Material.KIND_PRST:
        url = material.content.replace('watch?v=', 'embed/')
    else:
        url = ""
    context = {
        'material': material,
        'url': url,
    }
    success_url = reverse('student_material', kwargs={'material_id': material.id, 'topic_id': topic_id})
    _process_content(request, context)
    return _process_comment(request, template_name, context, success_url)


# topic quiz
@login_required
@student_required
def student_quiz(request, quiz_id):
    quiz = Quiz.objects.all()
    return render(request, 'student/student_topic_quiz.html', {'quiz':quiz})


# learning style quiz page
@login_required
@student_required
def learning_style(request):
    return render(request, 'learning_style.html')

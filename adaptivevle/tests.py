from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.test import TestCase
from django.contrib.auth.models import User

from adaptivevle.models import Profile
from adaptivevle.models import Unit, Topic, Material, Quiz, QuizQuestion, Response, Comment, get_kind_by_style
from adaptivevle.quiz import LearningStyleQuiz, QuizQuestion, QuizOption, process_quiz


class HomePageTests(TestCase):
    home_url = reverse('home')

    def test_status_200(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)

    def test_contains_title(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, 'VLE')

    def test_contains_important_urls(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, reverse('login'))
        self.assertContains(response, reverse('register_options'))


DEFAULT_USERNAME = 'Kowalski'
DEFAULT_PASSWORD = '12345Abc'


def create_user(**kwargs):
    defaults = {
        'username': DEFAULT_USERNAME,
        'password': DEFAULT_PASSWORD,
        'email': 'kowalski@gmail.com'
    }
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)


def create_student(**kwargs):
    user = create_user(**kwargs)
    Profile.objects.create(user=user, role=Profile.STUDENT)
    return user


def create_teacher(**kwargs):
    user = create_user(**kwargs)
    Profile.objects.create(user=user, role=Profile.TEACHER)
    return user


UNIT_DEFAULT_NAME = 'Unit1'


def create_unit(**kwargs):
    defaults = {
        'name': UNIT_DEFAULT_NAME
    }
    defaults.update(kwargs)
    return Unit.objects.create(**defaults)


TOPIC_DEFAULT_NAME = 'Topic1'


def create_topic(unit, **kwargs):
    defaults = {
        'name': TOPIC_DEFAULT_NAME,
        'unit': unit,
        'date_created': timezone.now()
    }
    defaults.update(kwargs)
    return Topic.objects.create(**defaults)


DEFAULT_MATERIAL_NAME = 'Material1'
DEFAULT_MATERIAL_CONTENT = 'MaterialContent123'


def create_text_material(topic, **kwargs):
    defaults = {
        'name': DEFAULT_MATERIAL_NAME,
        'content': DEFAULT_MATERIAL_CONTENT,
        'date_created': timezone.now(),
        'topic': topic,
        'kind': Material.KIND_TEXT
    }
    defaults.update(kwargs)
    return Material.objects.create(**defaults)


class StudentLoginPageTests(TestCase):
    login_url = reverse('login')

    def is_logged(self):
        response = self.client.get(reverse('student_units'))
        return response.status_code == 200

    def test_status_200(self):
        pass

    def test_contains_title(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, 'Login')

    def test_contains_important_urls(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, reverse('register_options'))

    def test_login_valid(self):
        create_student(username='tmpuser', password='Tmp12345')
        form_data = {'username': 'tmpuser', 'password': 'Tmp12345'}
        self.client.post(self.login_url, form_data)
        self.assertTrue(self.is_logged())

    def test_login_empty_username_field(self):
        create_student(username='tmpuser', password='Tmp12345')
        form_data = {'username': '', 'password': 'Tmp12345'}
        self.client.post(self.login_url, form_data)
        self.assertFalse(self.is_logged())

    def test_login_empty_password_field(self):
        create_student(username='tmpuser', password='Tmp12345')
        form_data = {'username': 'tmpuser', 'password': ''}
        self.client.post(self.login_url, form_data)
        self.assertFalse(self.is_logged())


class TeacherLoginPageTests(TestCase):
    login_url = reverse('login')

    def is_logged(self):
        response = self.client.get(reverse('teacher_units'))
        return response.status_code == 200

    def test_status_200(self):
        pass

    def test_contains_title(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, 'Login')

    def test_contains_important_urls(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, reverse('register_options'))

    def test_login_valid(self):
        create_teacher(username='tmpuser', password='Tmp12345')
        form_data = {'username': 'tmpuser', 'password': 'Tmp12345'}
        self.client.post(self.login_url, form_data)
        self.assertTrue(self.is_logged())

    def test_login_empty_username_field(self):
        create_teacher(username='tmpuser', password='Tmp12345')
        form_data = {'username': '', 'password': 'Tmp12345'}
        self.client.post(self.login_url, form_data)
        self.assertFalse(self.is_logged())

    def test_login_empty_password_field(self):
        create_teacher(username='tmpuser', password='Tmp12345')
        form_data = {'username': 'tmpuser', 'password': ''}
        self.client.post(self.login_url, form_data)
        self.assertFalse(self.is_logged())


class TeacherCreateMaterialTextTests(TestCase):

    def _prepare_teacher(self):
        teacher = create_teacher()
        self.client.login(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)

    def _create_url(self):
        unit = create_unit()
        topic = create_topic(unit)
        url = reverse('add_text', args=[topic.id])
        return url

    def test_required_teacher(self):
        url = self._create_url()
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)

    def test_status_200(self):
        self._prepare_teacher()
        url = self._create_url()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_valid_create(self):
        self._prepare_teacher()
        url = self._create_url()
        form_data = {'name': 'Example', 'content': 'Bla bla bla'}
        self.client.post(url, form_data)
        material = Material.objects.all().first()
        self.assertEquals(material.kind, Material.KIND_TEXT)


class StudentTopicPageTests(TestCase):

    def _prepare_student(self):
        student = create_student()
        self.client.login(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)

    def _create_url(self):
        unit = create_unit()
        topic = create_topic(unit)
        create_text_material(topic)
        url = reverse('student_topic', args=[unit.id, topic.id])
        return url

    def test_required_student(self):
        url = self._create_url()
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)

    def test_status_200(self):
        self._prepare_student()
        url = self._create_url()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_material(self):
        self._prepare_student()
        url = self._create_url()
        response = self.client.get(url)
        self.assertContains(response, DEFAULT_MATERIAL_NAME)


# learning style quiz
V = Profile.STYLE_VISUAL
A = Profile.STYLE_AURAL
R = Profile.STYLE_READ_WRITE
K = Profile.STYLE_KINESTHETIC
M = Profile.STYLE_MULTIMODAL


class LearningStyleTests(SimpleTestCase):

    def test(self):
        quiz = LearningStyleQuiz([
            QuizQuestion('1. I need to find the way to a shop that a friend has recommended. I would:', [
                QuizOption('find out where the shop is in relation to somewhere I know.', K),
                QuizOption('ask my friend to tell me the directions.', A),
                QuizOption('write down the street directions I need to remember.', R),
                QuizOption('use a map.', V),
            ])
        ])

        form = {
            "question_0_0": "on",
            "question_0_1": "off",
            "question_0_2": "off",
            "question_0_3": "off",

        }
        learning_style = process_quiz(quiz, form)
        self.assertEquals(learning_style.get_main_style_code(), K)

    def test_multimodal(self):
        quiz = LearningStyleQuiz([
            QuizQuestion('1. I need to find the way to a shop that a friend has recommended. I would:', [
                QuizOption('find out where the shop is in relation to somewhere I know.', K),
                QuizOption('ask my friend to tell me the directions.', A),
                QuizOption('write down the street directions I need to remember.', R),
                QuizOption('use a map.', V),
            ]),
            QuizQuestion('1. I need to find the way to a shop that a friend has recommended. I would:', [
                QuizOption('find out where the shop is in relation to somewhere I know.', K),
                QuizOption('ask my friend to tell me the directions.', A),
                QuizOption('write down the street directions I need to remember.', R),
                QuizOption('use a map.', V),
            ])
        ])

        form = {
            "question_0_0": "on",
            "question_0_1": "off",
            "question_0_2": "off",
            "question_0_3": "off",

            "question_1_0": "off",
            "question_1_1": "on",
            "question_1_2": "off",
            "question_1_3": "off",
        }
        learning_style = process_quiz(quiz, form)
        self.assertEquals(learning_style.get_main_style_code(), M)

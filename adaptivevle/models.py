from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    ROLE = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    STYLE_VISUAL = 'V'
    STYLE_AURAL = 'A'
    STYLE_READ_WRITE = 'R'
    STYLE_KINESTHETIC = 'K'
    STYLE_MULTIMODAL = 'M'

    STYLES = [
        (STYLE_VISUAL, 'Visual'),
        (STYLE_AURAL, 'Aural'),
        (STYLE_READ_WRITE, 'Read/Write'),
        (STYLE_KINESTHETIC, 'Kinesthetic'),
        (STYLE_MULTIMODAL, 'Multimodal')
    ]
    role = models.CharField(max_length=7, choices=ROLE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    learning_style = models.CharField(max_length=1, choices=STYLES, null=True, default=None)

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_student(self):
        return self.role == self.STUDENT


class Unit(models.Model):
    name = models.CharField(max_length=40)


class Topic(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)


class Material(models.Model):
    KIND_VIDEO = 'vid'
    KIND_PICTURE = 'pic'
    KIND_AUDIO = 'aud'
    KIND_TEXT = 'text'
    KIND_PRST = 'presentation'

    KIND = [
        (KIND_VIDEO, 'Video'),
        (KIND_PICTURE, 'Picture'),
        (KIND_AUDIO, 'Audio'),
        (KIND_TEXT, 'Text'),
        (KIND_PRST, 'Presentation'),
    ]
    name = models.CharField(max_length=40)
    file = models.FileField(upload_to='files', null=True)
    content = models.TextField(null=True)
    date_created = models.DateTimeField()
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    kind = models.CharField(max_length=12, choices=KIND)


class UserMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)


class Comment(models.Model):
    message = models.TextField()
    date_created = models.DateTimeField()
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.message, self.user)




class Quiz(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    date_created = models.DateTimeField()
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    # is_complete = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'quizes'


ANSWER_1 = 'answer_1'
ANSWER_2 = 'answer_2'
ANSWER_3 = 'answer_3'
ANSWER_4 = 'answer_4'

ANSWERS_CHOICES = [
    (ANSWER_1, 'answer_1'),
    (ANSWER_2, 'answer_2'),
    (ANSWER_3, 'answer_3'),
    (ANSWER_4, 'answer_4')
]

class QuizQuestion(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    correct = models.CharField('Correct answer', max_length=10, choices=ANSWERS_CHOICES)
    answer_1 = models.CharField('Answer', max_length=255, null=True)
    answer_2 = models.CharField('Answer', max_length=255, null=True)
    answer_3 = models.CharField('Answer', max_length=255, null=True)
    answer_4 = models.CharField('Answer', max_length=255, null=True)


class Response(models.Model):
    quizquestion = models.ForeignKey(QuizQuestion, on_delete=models.PROTECT)
    quizanswer = models.CharField('Answer', max_length=10, choices=ANSWERS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def is_correct(self):
        print(self.quizanswer, self.quizquestion.correct)
        return self.quizanswer == self.quizquestion.correct


def get_kind_by_style(style):
    if style == Profile.STYLE_VISUAL:
        return Material.KIND_VIDEO
    elif style == Profile.STYLE_KINESTHETIC:
        return Material.KIND_PRST
    elif style == Profile.STYLE_AURAL:
        return Material.KIND_AUDIO
    elif style == Profile.STYLE_READ_WRITE:
        return Material.KIND_TEXT
    else:
        return Profile.STYLE_MULTIMODAL

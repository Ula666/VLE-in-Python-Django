from django.contrib import admin
from adaptivevle.models import Profile, Unit, Comment, Quiz, QuizQuestion


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']


# admin can add new units
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'date_created')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)

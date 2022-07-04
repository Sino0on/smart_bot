from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    name = models.CharField(max_length=100)
    username_tg = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    tg = models.CharField(max_length=100)
    age = models.DateField(blank=True, null=True)
    rank = models.IntegerField(default=1)

    def __str__(self):
        return self.username


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(decimal_places=1000, max_digits=100000, blank=True, null=True)
    hour = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-date']


class ImageCourse(models.Model):
    image = models.ImageField(upload_to='images/courses/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course}'


class Group(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    maxstudent = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}  {self.course}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['-date']


class CourseStudent(models.Model):
    groupcourse = models.ForeignKey(Group, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account} - {self.groupcourse}'

    class Meta:
        verbose_name = 'Студент Курс'
        verbose_name_plural = 'Студент Курсы'
        ordering = ['-date']
        unique_together = ['account', 'groupcourse']


class Application(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' Зв {self.account} - {self.course}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-date']
        unique_together = ['account', 'course']


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятие'
        ordering = ['-date']


class ImageMet(models.Model):
    image = models.ImageField(upload_to='image/meeting')
    meet = models.ForeignKey(Meeting, on_delete=models.CASCADE)


class ApplicationMet(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.Account} - {self.meeting}'

    class Meta:
        verbose_name = 'Заявка на мероприятие'
        verbose_name_plural = 'Заявки на мероприятие'
        ordering = ['-date']


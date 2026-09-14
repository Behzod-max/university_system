from django.db import models


class Teacher(models.Model):
    first_name = models.CharField("Ism", max_length=100)
    last_name = models.CharField("Familiya", max_length=100)
    phone = models.CharField("Telefon", max_length=20)
    email = models.EmailField("Email", unique=True)

    class Meta:
        verbose_name = "O‘qituvchi"
        verbose_name_plural = "O‘qituvchilar"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField("Ism", max_length=100)
    last_name = models.CharField("Familiya", max_length=100)
    group = models.CharField("Guruh", max_length=50)
    email = models.EmailField("Email", unique=True)

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField("Fan nomi", max_length=200)
    code = models.CharField("Fan kodi", max_length=50, unique=True)
    credits = models.PositiveIntegerField("Kredit")
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subjects",
        verbose_name="O‘qituvchi"
    )
    students = models.ManyToManyField(
        Student,
        blank=True,
        related_name="subjects",
        verbose_name="Talabalar"
    )

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"
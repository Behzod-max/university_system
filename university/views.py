
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django import forms



from .models import Subject, Teacher, Student


class UzbekUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        help_text="150 ta belgigacha bo‘lishi mumkin. Harflar, raqamlar va @/./+/-/_ belgilaridan foydalaning.",
    )
    password1 = forms.CharField(
        label="Parol",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Parol kamida 8 ta belgidan iborat bo‘lishi, oddiy bo‘lmasligi, faqat raqamlardan tuzilmasligi va foydalanuvchi nomiga o‘xshamasligi kerak.",
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlash",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Tasdiqlash uchun parolni yana bir marta kiriting.",
    )


def signup(request):
    form = UzbekUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(
        request,
        "university/signup.html",
        {"form": form}
    )


def signin(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")

    return render(
        request,
        "university/signin.html",
        {"form": form}
    )


def signout(request):
    if request.method == "POST":
        logout(request)

    return redirect("home")


def home(request):
    context = {
        "subject_count": Subject.objects.count(),
        "teacher_count": Teacher.objects.count(),
        "student_count": Student.objects.count(),
    }

    return render(
        request,
        "university/home.html",
        context
    )


@login_required
def subject_list(request):
    subjects = (
        Subject.objects
        .select_related("teacher")
        .prefetch_related("students")
    )

    return render(
        request,
        "university/subject_list.html",
        {"subjects": subjects}
    )


@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(
        Subject.objects
        .select_related("teacher")
        .prefetch_related("students"),
        id=subject_id
    )

    return render(
        request,
        "university/subject_detail.html",
        {"subject": subject}
    )


@login_required
def teacher_list(request):
    teachers = Teacher.objects.prefetch_related("subjects")

    return render(
        request,
        "university/teacher_list.html",
        {"teachers": teachers}
    )


@staff_member_required
def add_teacher(request):
    if request.method == "POST":
        Teacher.objects.create(
            first_name=request.POST.get("first_name", "").strip(),
            last_name=request.POST.get("last_name", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            email=request.POST.get("email", "").strip(),
        )

        return redirect("teacher_list")

    return render(request, "university/add_teacher.html")


@staff_member_required
def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            first_name=request.POST.get("first_name", "").strip(),
            last_name=request.POST.get("last_name", "").strip(),
            group=request.POST.get("group", "").strip(),
            email=request.POST.get("email", "").strip(),
        )

        return redirect("home")

    return render(request, "university/add_student_form.html")


@staff_member_required
def student_list(request):
    students = (
        Student.objects
        .prefetch_related("subjects")
        .order_by("last_name", "first_name")
    )

    return render(
        request,
        "university/student_list.html",
        {"students": students}
    )


@login_required
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(
        Teacher.objects.prefetch_related("subjects__students"),
        id=teacher_id
    )

    return render(
        request,
        "university/teacher_detail.html",
        {"teacher": teacher}
    )

@staff_member_required
def add_subject(request):

    if request.method == "POST":

        name = request.POST.get("name")
        code = request.POST.get("code")
        credits = request.POST.get("credits")
        teacher_id = request.POST.get("teacher")

        teacher = None

        if teacher_id:
            teacher = get_object_or_404(
                Teacher,
                id=teacher_id
            )

        Subject.objects.create(
            name=name,
            code=code,
            credits=credits,
            teacher=teacher
        )

        return redirect("subject_list")

    teachers = Teacher.objects.all()

    return render(
        request,
        "university/add_subject.html",
        {
            "teachers": teachers
        }
    )

@staff_member_required
def edit_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == "POST":

        name = request.POST.get("name")
        code = request.POST.get("code")
        credits = request.POST.get("credits")
        teacher_id = request.POST.get("teacher")

        teacher = None

        if teacher_id:
            teacher = get_object_or_404(
                Teacher,
                id=teacher_id
            )

        subject.name = name
        subject.code = code
        subject.credits = credits
        subject.teacher = teacher

        subject.save()

        return redirect(
            "subject_detail",
            subject_id=subject.id
        )

    teachers = Teacher.objects.all()

    return render(
        request,
        "university/edit_subject.html",
        {
            "subject": subject,
            "teachers": teachers,
        }
    )

@staff_member_required
def delete_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == "POST":

        subject.delete()

        return redirect("subject_list")

    return redirect("subject_detail", subject_id=subject.id)


@staff_member_required
def add_student_to_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        student_id = request.POST.get("student_id")

        if student_id:
            student = get_object_or_404(
                Student,
                id=student_id
            )

            subject.students.add(student)

        return redirect(
            "subject_detail",
            subject_id=subject.id
        )

    students = Student.objects.exclude(
        subjects=subject
    )

    return render(
        request,
        "university/add_student.html",
        {
            "subject": subject,
            "students": students,
        }
    )

@staff_member_required
def remove_student_from_subject(request, subject_id, student_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":
        subject.students.remove(student)

    return redirect(
        "subject_detail",
        subject_id=subject.id
    )
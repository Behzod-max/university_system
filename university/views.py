
from django.shortcuts import get_object_or_404, redirect, render



from .models import Subject, Teacher, Student


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


def teacher_list(request):
    teachers = Teacher.objects.prefetch_related("subjects")

    return render(
        request,
        "university/teacher_list.html",
        {"teachers": teachers}
    )


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

def delete_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == "POST":

        subject.delete()

        return redirect("subject_list")

    return redirect("subject_detail", subject_id=subject.id)


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
from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.subject_list,
        name="subject_list"
    ),

    path(
        "add/",
        views.add_subject,
        name="add_subject"
    ),

    path(
        "<int:subject_id>/",
        views.subject_detail,
        name="subject_detail"
    ),

    path(
        "<int:subject_id>/add-student/",
        views.add_student_to_subject,
        name="add_student_to_subject"
    ),

    path(
        "<int:subject_id>/remove-student/<int:student_id>/",
        views.remove_student_from_subject,
        name="remove_student_from_subject"
    ),

    path(
        "teachers/",
        views.teacher_list,
        name="teacher_list"
    ),

    path(
        "teachers/add/",
        views.add_teacher,
        name="add_teacher"
    ),

    path(
        "students/add/",
        views.add_student,
        name="add_student"
    ),

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "teachers/<int:teacher_id>/",
        views.teacher_detail,
        name="teacher_detail"
    ),

    path(
    "<int:subject_id>/edit/",
    views.edit_subject,
    name="edit_subject"
    ),

    path(
    "<int:subject_id>/delete/",
    views.delete_subject,
    name="delete_subject"
    ),
]
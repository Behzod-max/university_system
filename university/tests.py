from django.test import TestCase
from django.urls import reverse

from .models import Student, Subject, Teacher


class UniversityWorkflowTests(TestCase):
	def setUp(self):
		self.teacher = Teacher.objects.create(
			first_name="Ali",
			last_name="Valiyev",
			phone="+998901112233",
			email="ali@example.com",
		)
		self.student = Student.objects.create(
			first_name="Zarina",
			last_name="Karimova",
			group="301",
			email="zarina@example.com",
		)

	def test_teacher_can_be_created_from_ui(self):
		response = self.client.post(
			reverse("add_teacher"),
			{
				"first_name": "Malika",
				"last_name": "Sobirova",
				"phone": "+998909998877",
				"email": "malika@example.com",
			},
		)

		self.assertRedirects(response, reverse("teacher_list"))
		self.assertTrue(
			Teacher.objects.filter(email="malika@example.com").exists()
		)

	def test_student_can_be_created_from_ui(self):
		response = self.client.post(
			reverse("add_student"),
			{
				"first_name": "Malika",
				"last_name": "Rasulova",
				"group": "302",
				"email": "malika.student@example.com",
			},
		)

		self.assertRedirects(response, reverse("home"))
		self.assertTrue(
			Student.objects.filter(email="malika.student@example.com").exists()
		)

	def test_subject_detail_assigns_student_and_shows_teacher_data(self):
		subject = Subject.objects.create(
			name="Python",
			code="PY101",
			credits=5,
			teacher=self.teacher,
		)

		response = self.client.post(
			reverse("add_student_to_subject", args=[subject.id]),
			{"student_id": self.student.id},
		)

		self.assertRedirects(
			response,
			reverse("subject_detail", args=[subject.id]),
		)
		self.assertTrue(subject.students.filter(id=self.student.id).exists())

		teacher_response = self.client.get(
			reverse("teacher_detail", args=[self.teacher.id])
		)
		self.assertContains(teacher_response, "Ali Valiyev")
		self.assertContains(teacher_response, "Python")

	def test_subject_can_be_deleted_from_detail_page(self):
		subject = Subject.objects.create(
			name="Matematika",
			code="MA101",
			credits=4,
		)

		response = self.client.post(
			reverse("delete_subject", args=[subject.id])
		)

		self.assertRedirects(response, reverse("subject_list"))
		self.assertFalse(Subject.objects.filter(id=subject.id).exists())

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Student, Subject, Teacher


class UniversityWorkflowTests(TestCase):
	def setUp(self):
		self.admin = User.objects.create_user(
			username="adminuser",
			password="StrongPassword123!",
			is_staff=True,
		)
		self.client.force_login(self.admin)
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

	def test_user_can_sign_up_and_is_logged_in(self):
		response = self.client.post(
			reverse("signup"),
			{
				"username": "newstudent",
				"password1": "StrongPassword123!",
				"password2": "StrongPassword123!",
			},
		)

		self.assertRedirects(response, reverse("home"))
		self.assertTrue(User.objects.filter(username="newstudent").exists())
		self.assertEqual(response.wsgi_request.user.username, "newstudent")

	def test_user_can_sign_in(self):
		User.objects.create_user(
			username="existinguser",
			password="StrongPassword123!",
		)

		response = self.client.post(
			reverse("signin"),
			{
				"username": "existinguser",
				"password": "StrongPassword123!",
			},
		)

		self.assertRedirects(response, reverse("home"))
		self.assertEqual(response.wsgi_request.user.username, "existinguser")

	def test_regular_user_cannot_add_teacher(self):
		regular_user = User.objects.create_user(
			username="regularuser",
			password="StrongPassword123!",
		)
		self.client.force_login(regular_user)

		response = self.client.get(reverse("add_teacher"))

		self.assertEqual(response.status_code, 302)
		self.assertIn("/admin/login/", response.url)

	def test_admin_can_view_all_students(self):
		response = self.client.get(reverse("student_list"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Karimova Zarina")

	def test_regular_user_cannot_view_all_students(self):
		regular_user = User.objects.create_user(
			username="studentviewer",
			password="StrongPassword123!",
		)
		self.client.force_login(regular_user)

		response = self.client.get(reverse("student_list"))

		self.assertEqual(response.status_code, 302)
		self.assertIn("/admin/login/", response.url)

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
		self.assertContains(teacher_response, "Valiyev Ali")
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

from django.test import TestCase, Client
from django.urls import reverse
from .models import Review
from .forms import ReviewForm


class ReviewModelTest(TestCase):
    def setUp(self):
        Review.objects.create(
            author_name="John Doe",
            text="Great service!",
            rating=5,
            is_published=True
        )

    def test_review_creation(self):
        review = Review.objects.get(author_name="John Doe")
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.is_published)

    def test_str_representation(self):
        review = Review.objects.get(author_name="John Doe")
        self.assertEqual(str(review), "Отзыв от John Doe (5 звезд)")


class ReviewFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'author_name': 'Jane Doe',
            'author_position': '',
            'service_type': 'frame_extension',
            'text': 'Good work!',
            'rating': 4,
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'author_name': '', 'text': 'Good work!', 'rating': 4}
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('author_name', form.errors)


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Review.objects.create(author_name="Reviewer 1", text="Text 1", rating=5, is_published=True)
        Review.objects.create(author_name="Reviewer 2", text="Text 2", rating=4, is_published=False)

    def test_review_list_view(self):
        response = self.client.get(reverse('reviews:review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_list.html')
        self.assertContains(response, "Reviewer 1")
        self.assertNotContains(response, "Reviewer 2")  # Not published

    def test_add_review_view_get(self):
        response = self.client.get(reverse('reviews:add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/add_review.html')
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_add_review_view_post_valid(self):
        response = self.client.post(reverse('reviews:add_review'), {
            'author_name': 'New Reviewer',
            'author_position': '',
            'service_type': 'frame_extension',
            'text': 'Awesome job!',
            'rating': 5,
        })
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertEqual(Review.objects.count(), 3)  # 2 existing + 1 new
        self.assertTrue(Review.objects.filter(author_name="New Reviewer").exists())

    def test_add_review_view_post_invalid(self):
        response = self.client.post(reverse('reviews:add_review'), {
            'author_name': '',
            'text': 'Not good',
            'rating': 1
        })
        self.assertEqual(response.status_code, 200)  # Stays on page with errors
        self.assertFormError(response.context['form'], 'author_name', 'Обязательное поле.')

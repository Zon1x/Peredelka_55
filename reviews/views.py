from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    stats = reviews.aggregate(avg_rating=Avg('rating'), total=Count('id'))
    avg_rating = stats['avg_rating']
    if avg_rating is not None:
        avg_rating = round(float(avg_rating), 1)
    context = {
        'reviews': reviews,
        'reviews_total': stats['total'],
        'avg_rating': avg_rating,
    }
    return render(request, 'reviews/review_list.html', context)

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Review is initially not published, requires admin moderation
            review.is_published = False
            review.save()

            # Send email notification to admins
            subject = f'Новый отзыв на сайте от {review.author_name}'
            html_message = render_to_string('reviews/emails/admin_review_notification.html', {'review': review})
            plain_message = f'Новый отзыв от {review.author_name} ({review.rating} звезд) ожидает модерации.\nТекст отзыва: {review.text}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [admin[1] for admin in settings.ADMINS] if settings.ADMINS else []

            if recipient_list:
                try:
                    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                except Exception as e:
                    # Log the error, but don't block the user
                    print(f"Error sending admin notification email: {e}")

            messages.success(
                request,
                'Спасибо! Отзыв сохранён и отправлен на модерацию — после проверки он появится в общем списке.',
            )
            return redirect('reviews:review_list')
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'reviews/add_review.html', context)

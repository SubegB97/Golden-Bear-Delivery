from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProductReview

#Class that sets up the review form for the customer where they can leave comments and a rating from 1-5
class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ("review_text", "review_rating")

    def __init__(self, *args, **kwargs):
        super(ReviewAdd, self).__init__(*args, **kwargs)
        self.fields["review_text"].label = "Comment"
        self.fields["review_rating"].label = "Rating"


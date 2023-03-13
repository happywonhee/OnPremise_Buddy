from django.shortcuts import get_object_or_404, render, redirect
from review.models import Review
from review.forms import ReviewCreateForm, ReviewUpdateForm
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from django.contrib.auth.decorators import login_required
from config import settings
import os

from django.core.exceptions import PermissionDenied
class ReviewUpdate(UpdateView):
    model = Review
    form_class = ReviewUpdateForm
    template_name = 'review/review_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        if self.get_object().file_upload.name != '':
            if self.object.file_upload != self.get_object().file_upload.name:
                file_upload_path=os.path.join(settings.MEDIA_ROOT, self.get_object().file_upload.path)
                if os.path.exists(file_upload_path):
                    os.remove(file_upload_path)
            if 'upload_clear' in self.request.POST:
                file_upload_path=os.path.join(settings.MEDIA_ROOT, self.get_object().file_upload.path)
                if os.path.exists(file_upload_path):
                    os.remove(file_upload_path)
                    self.object.file_upload = ''
        return super().form_valid(form)


class ReviewList(ListView):
    model = Review
    template_name = 'review/review_list.html'
    ordering = '-pk'
    paginate_by = 10

class ReviewDetail(DetailView):
    model = Review
    template_name = 'review/review_detail.html'

class ReviewCreate(CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review/review_form.html'
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super().form_valid(form)
        else:
            return redirect('/review')

@login_required(login_url='common:login')
def ReviewDelete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user != review.author:
        return redirect('review:detail', pk=pk)
    if review.file_upload:
        file_upload_path = os.path.join(settings.MEDIA_ROOT, review.file_upload.path)
        if os.path.exists(file_upload_path):
            os.remove(file_upload_path)
    review.delete()
    return redirect('review:list')
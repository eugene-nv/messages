from django.shortcuts import render, redirect
from django.views import View

from .forms import MessageForm
from .models import Message


class MessageViews(View):
    template_name = 'home.html'
    form = MessageForm()

    def get(self, request):
        context = {
            'mess': Message.objects.all(),
            'm': self.form,
            'title': 'Home page'
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = MessageForm(request.POST)

        context = {
            'm': form,
            'title': 'Update page'
        }

        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.save()
            return redirect('home')

        return render(request, self.template_name, context)


class MessageDeleteView(View):

    def post(self, request, *args, **kwargs):
        message_id = kwargs.get('id')
        message = Message.objects.get(id=message_id)
        if message:
            message.delete()
        return redirect('home')


class MessageUpdateView(View):
    def get(self, request, *args, **kwargs):
        message_id = kwargs.get('id')
        message = Message.objects.get(id=message_id)
        form = MessageForm(instance=message)
        return render(request, 'update.html', {'form': form, 'message_id': message_id})

    def post(self, request, *args, **kwargs):
        message_id = kwargs.get('id')
        article = Message.objects.get(id=message_id)
        form = MessageForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, 'update.html', {'form': form, 'message_id': message_id})


def vuejs_page(request):
    return render(request, 'vuejs.html')

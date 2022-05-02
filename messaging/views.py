from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import MessageForm
from .models import Message
from .services import notify

# Create your views here.


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            receiver = User.objects.filter(username=data['receiver']).get()
            message = Message(sender=request.user, receiver=receiver, subject=data['subject'], body=data['body'])
            message.save()
            return redirect('messaging:get_all_messages')
    else:
        form = MessageForm()
    ctx = {
        'form': form
    }
    return render(request, 'messaging/send_message.html', ctx)


def get_all_messages(request):
#    notify(request.user, 'Þú ert að skoða inboxið þitt', '')
    messages = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    return render(request, 'messaging/get_all_messages.html', {"messages": messages})


def get_message(request, message_id):
    ctx = {}
    message = get_object_or_404(Message, pk=message_id, receiver=request.user)
    if not message.read_at:
        message.read_at = datetime.now()
        message.save()
    ctx['message'] = message
    return render(request, 'messaging/get_message.html', ctx)
    pass

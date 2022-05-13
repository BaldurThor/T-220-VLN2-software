from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
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
            if request.POST.get('item_id'):
                item = Item.objects.get(pk=request.POST.get('item_id'))
                message.related = item
                message.type = 'Item_inquiry'
            message.save()
            return redirect('messaging:get_all_messages')
    else:
        receiver = request.GET.get('receiver', '')
        subject = request.GET.get('subject', '')
        form = MessageForm(initial={
            'receiver': receiver,
            'subject': subject,
        })
    ctx = {
        'form': form
    }
    return render(request, 'messaging/send_message.html', ctx)


def get_all_messages(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    return render(request, 'messaging/get_all_messages.html', {"messages_qs": messages})


def get_message(request, message_id):
    ctx = {}
    message = get_object_or_404(Message, pk=message_id, receiver=request.user)
    if not message.read_at:
        message.read_at = datetime.now()
        message.save()
    ctx['message'] = message
    return render(request, 'messaging/get_message.html', ctx)

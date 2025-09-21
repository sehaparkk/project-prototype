from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import SendMessageForm

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('inbox') # Redirect to inbox after sending
    else:
        form = SendMessageForm(initial={'receiver': receiver})
    return render(request, 'messaging/send_message.html', {'form': form, 'receiver': receiver})

@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'messaging/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Ensure only sender or receiver can view the message
    if message.sender != request.user and message.receiver != request.user:
        return redirect('inbox') # Or show an error message

    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/view_message.html', {'message': message})

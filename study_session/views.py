from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
import google.generativeai as genai
from .models import StudyRoom, RoomParticipant, RoomMessage, StudyBlock
from accounts.models import Friendship
import json

@login_required
def study_room(request):
    """
    Renders the Study Sesh (Mission Control) room.
    Features:
    - Focus Timer
    - Ambience Selector
    - Task List
    - Multiplayer Docking
    """
    # Get or create a default room for now (Phase 5)
    room, created = StudyRoom.objects.get_or_create(name="Global Study Deck")
    
    # Register participant
    participant, _ = RoomParticipant.objects.get_or_create(room=room, user=request.user)
    participant.is_active = True
    participant.last_active = timezone.now()
    participant.save()

    context = {
        'page_title': 'Study Sesh - Mission Control',
        'room_id': room.id,
        'user_id': request.user.id,
        'username': request.user.username,
    }
    return render(request, 'study_session/room.html', context)

@login_required
def get_room_data(request):
    """AJAX endpoint to fetch crew and messages"""
    room_id = request.GET.get('room_id')
    if not room_id:
        return JsonResponse({'error': 'No room ID'}, status=400)
        
    # Update own presence
    RoomParticipant.objects.filter(user=request.user, room_id=room_id).update(
        last_active=timezone.now(), is_active=True
    )
    
    # Get active crew (active in last 5 minutes)
    threshold = timezone.now() - timezone.timedelta(minutes=5)
    active_participants = RoomParticipant.objects.filter(
        room_id=room_id, 
        last_active__gte=threshold,
        is_active=True
    ).select_related('user')
    
    crew_data = []
    for p in active_participants:
        # Determine status based on last_active
        time_diff = (timezone.now() - p.last_active).total_seconds()
        status = 'studying' if time_diff < 60 else 'idle'
        
        crew_data.append({
            'id': p.user.id,
            'username': p.user.username,
            'status': status,
            'is_me': p.user.id == request.user.id
        })
    
    # Get recent messages
    last_msg_id = request.GET.get('last_msg_id', 0)
    messages = RoomMessage.objects.filter(
        room_id=room_id, 
        id__gt=last_msg_id
    ).select_related('user').order_by('timestamp')[:50]
    
    msg_data = [{
        'id': m.id,
        'user': m.user.username,
        'content': m.content,
        'timestamp': m.timestamp.strftime('%H:%M')
    } for m in messages]
    
    return JsonResponse({'crew': crew_data, 'messages': msg_data})

@login_required
def navigator_view(request):
    """
    Renders the Navigator AI Planner page.
    """
    # Fetch existing blocks
    blocks = StudyBlock.objects.filter(user=request.user)
    schedule_data = [{
        'id': b.id,
        'title': b.title,
        'dayIndex': b.day_index,
        'date': b.date.strftime('%Y-%m-%d') if b.date else None,
        'startDate': b.start_date.strftime('%Y-%m-%d') if b.start_date else None,
        'endDate': b.end_date.strftime('%Y-%m-%d') if b.end_date else None,
        'startHour': b.start_hour,
        'duration': b.duration,
        'type': b.block_type
    } for b in blocks]

    context = {
        'page_title': 'The Navigator - AI Command',
        'schedule_data': schedule_data
    }
    return render(request, 'study_session/navigator.html', context)

@login_required
@require_POST
def navigator_command(request):
    try:
        data = json.loads(request.body)
        command = data.get('command', '')
        
        if not command:
            return JsonResponse({'error': 'No command provided'}, status=400)

        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using gemini-2.0-flash as the standard stable model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        current_date_str = timezone.now().strftime('%Y-%m-%d')
        
        prompt = f"""
        You are an AI study planner. Analyze the following student command and extract schedule blocks.
        Current Date: {current_date_str}
        Command: "{command}"
        
        Return ONLY a JSON array of objects. Each object must have:
        - title: string (short title)
        - dayIndex: integer (0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday) - REQUIRED if date is null
        - date: string (YYYY-MM-DD) - OPTIONAL. Use if a specific date is mentioned (e.g. "Dec 25th").
        - startDate: string (YYYY-MM-DD) - OPTIONAL. Start date for recurring events.
        - endDate: string (YYYY-MM-DD) - OPTIONAL. End date for recurring events.
        - startHour: number (0-23.5) - e.g. 9:30 AM = 9.5, 2:45 PM = 14.75
        - duration: number (hours)
        - type: "fixed" (for exams/deadlines) or "ai" (for study sessions)
        
        If the command implies a deadline (e.g. "Exam Friday"), create a "fixed" block for the event itself, 
        and then create multiple "ai" study blocks leading up to it.
        Spread study blocks out logically.
        
        Example output:
        [
            {{"title": "Calculus Exam", "dayIndex": 4, "startHour": 14, "duration": 2, "type": "fixed"}}, // 4 is Friday
            {{"title": "Study Calc", "dayIndex": 2, "startHour": 10, "duration": 2, "type": "ai"}}, // 2 is Wednesday
            {{"title": "Final Project", "date": "2025-05-15", "startHour": 9, "duration": 1, "type": "fixed"}},
            {{"title": "Physics Class", "dayIndex": 3, "startDate": "2025-02-01", "endDate": "2025-06-02", "startHour": 13, "duration": 1.5, "type": "fixed"}} // 3 is Thursday
        ]
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Clean up markdown code blocks if present
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
            
        schedule = json.loads(text)
        
        # Save to DB
        new_blocks = []
        for item in schedule:
            # Handle optional date
            date_val = None
            if item.get('date'):
                date_val = item['date']
            
            # Handle optional dayIndex (default to 0 if missing but date is present, though model allows null)
            day_idx = item.get('dayIndex')
            
            # Handle optional start/end dates for recurring
            start_date_val = item.get('startDate')
            end_date_val = item.get('endDate')

            new_blocks.append(StudyBlock(
                user=request.user,
                title=item['title'],
                day_index=day_idx,
                date=date_val,
                start_date=start_date_val,
                end_date=end_date_val,
                start_hour=item['startHour'],
                duration=item['duration'],
                block_type=item['type']
            ))
        StudyBlock.objects.bulk_create(new_blocks)
        
        return JsonResponse({'schedule': schedule, 'reply': 'Trajectory calculated. Schedule updated.'})
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_study_block(request, block_id):
    try:
        block = StudyBlock.objects.get(id=block_id, user=request.user)
        block.delete()
        return JsonResponse({'success': True})
    except StudyBlock.DoesNotExist:
        return JsonResponse({'error': 'Block not found'}, status=404)

@login_required
@require_POST
def send_message(request):
    """AJAX endpoint to send a chat message"""
    data = json.loads(request.body)
    room_id = data.get('room_id')
    content = data.get('content')
    
    if room_id and content:
        RoomMessage.objects.create(
            room_id=room_id,
            user=request.user,
            content=content
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid data'}, status=400)

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    if len(query) < 1:
        return JsonResponse({'users': []})
    
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[:10]
    results = []
    for u in users:
        is_friend = Friendship.objects.filter(from_user=request.user, to_user=u).exists()
        results.append({
            'id': u.id,
            'username': u.username,
            'is_friend': is_friend
        })
    return JsonResponse({'users': results})

@login_required
@require_POST
def add_friend(request):
    data = json.loads(request.body)
    friend_id = data.get('user_id')
    try:
        friend = User.objects.get(id=friend_id)
        Friendship.objects.get_or_create(from_user=request.user, to_user=friend)
        return JsonResponse({'status': 'ok'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
def get_friends(request):
    friendships = Friendship.objects.filter(from_user=request.user).select_related('to_user')
    friends = [{
        'id': f.to_user.id,
        'username': f.to_user.username,
        # In a real app, we'd check their online status
        'status': 'offline' 
    } for f in friendships]
    return JsonResponse({'friends': friends})

#!/usr/bin/env python3
"""
Find Optimal Meeting Slots Tool
AI-powered time recommendations based on participant availability
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pytz

def find_optimal_slots(participants: List[str], duration: int, date_range: str) -> Dict[str, Any]:
    """
    Find optimal meeting slots for given participants
    
    Args:
        participants: List of participant names
        duration: Meeting duration in minutes
        date_range: Date range in format "YYYY-MM-DD to YYYY-MM-DD"
    
    Returns:
        Dict containing recommended slots with scoring
    """
    try:
        # Load data
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        
        with open('data/meetings.json', 'r') as f:
            meetings = json.load(f)
        
        # Parse date range
        start_date_str, end_date_str = date_range.split(' to ')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        # Find participant user objects
        participant_users = []
        for participant in participants:
            user = next((u for u in users if u['name'].lower() == participant.lower()), None)
            if user:
                participant_users.append(user)
            else:
                # Create temporary user for unknown participants
                participant_users.append({
                    'name': participant,
                    'timezone': 'UTC',
                    'work_hours': ['09:00', '17:00'],
                    'calendar': []
                })
        
        if not participant_users:
            return {"error": "No valid participants found"}
        
        # Find their existing meetings
        participant_meetings = []
        for meeting in meetings:
            if any(p in meeting['participants'] for p in participants):
                participant_meetings.append(meeting)
        
        # Generate potential slots
        optimal_slots = []
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends (basic business logic)
            if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
                # Check each hour from 9 AM to 5 PM
                for hour in range(9, 17):
                    slot_start = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                    slot_end = slot_start + timedelta(minutes=duration)
                    
                    # Skip if slot extends beyond work hours
                    if slot_end.hour > 17:
                        continue
                    
                    # Check availability for all participants
                    conflict_score = 0
                    availability_details = []
                    
                    for user in participant_users:
                        user_availability = check_user_availability(user, slot_start, slot_end, participant_meetings)
                        availability_details.append({
                            'user': user['name'],
                            'available': user_availability['available'],
                            'conflicts': user_availability['conflicts'],
                            'in_work_hours': user_availability['in_work_hours']
                        })
                        
                        # Scoring: lower is better
                        if not user_availability['available']:
                            conflict_score += 10
                        if not user_availability['in_work_hours']:
                            conflict_score += 5
                    
                    # Only add slots with no hard conflicts
                    if conflict_score < 10:  # No unavailable participants
                        optimal_slots.append({
                            'start': slot_start.isoformat(),
                            'end': slot_end.isoformat(),
                            'score': conflict_score,
                            'availability_details': availability_details
                        })
            
            current_date += timedelta(days=1)
        
        # Sort by score (best first) and take top 5
        optimal_slots.sort(key=lambda x: x['score'])
        top_slots = optimal_slots[:5]
        
        # AI-enhanced recommendations
        recommendations = []
        for i, slot in enumerate(top_slots):
            recommendation = {
                'rank': i + 1,
                'start': slot['start'],
                'end': slot['end'],
                'confidence': 'High' if slot['score'] == 0 else 'Medium',
                'reasoning': generate_slot_reasoning(slot),
                'participants_available': len([d for d in slot['availability_details'] if d['available']]),
                'total_participants': len(participants)
            }
            recommendations.append(recommendation)
        
        return {
            'success': True,
            'message': f"Found {len(recommendations)} optimal slots for {len(participants)} participants",
            'recommendations': recommendations,
            'search_criteria': {
                'participants': participants,
                'duration': duration,
                'date_range': date_range
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error finding optimal slots: {str(e)}"
        }

def check_user_availability(user: Dict, start: datetime, end: datetime, meetings: List[Dict]) -> Dict[str, Any]:
    """Check if user is available for a given time slot"""
    
    # Check work hours
    work_start = datetime.strptime(user['work_hours'][0], '%H:%M').time()
    work_end = datetime.strptime(user['work_hours'][1], '%H:%M').time()
    
    in_work_hours = (start.time() >= work_start and end.time() <= work_end)
    
    # Check for meeting conflicts
    conflicts = []
    for meeting in meetings:
        if user['name'] in meeting['participants'] or user.get('id') in meeting['participants']:
            meeting_start = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
            meeting_end = datetime.fromisoformat(meeting['end'].replace('Z', '+00:00'))
            
            # Check for time overlap
            if (start < meeting_end and end > meeting_start):
                conflicts.append({
                    'meeting_id': meeting['id'],
                    'meeting_title': meeting['title'],
                    'meeting_time': f"{meeting['start']} to {meeting['end']}"
                })
    
    return {
        'available': len(conflicts) == 0,
        'in_work_hours': in_work_hours,
        'conflicts': conflicts
    }

def generate_slot_reasoning(slot: Dict) -> str:
    """Generate AI-powered reasoning for why this slot is recommended"""
    details = slot['availability_details']
    available_count = len([d for d in details if d['available']])
    work_hours_count = len([d for d in details if d['in_work_hours']])
    
    if slot['score'] == 0:
        return f"Perfect slot: All {available_count} participants available during work hours"
    elif available_count == len(details):
        return f"Good slot: All participants available, {work_hours_count} within work hours"
    else:
        return f"Suboptimal: {available_count}/{len(details)} participants available" 
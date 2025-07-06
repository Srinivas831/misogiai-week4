#!/usr/bin/env python3
"""
Detect Scheduling Conflicts Tool
Identify conflicts for a user within a specific time range
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

def detect_scheduling_conflicts(user_id: str, time_range: str) -> Dict[str, Any]:
    """
    Detect scheduling conflicts for a user within a time range
    
    Args:
        user_id: User ID or name to check conflicts for
        time_range: Time range in format "YYYY-MM-DDTHH:MM to YYYY-MM-DDTHH:MM"
    
    Returns:
        Dict containing conflict analysis
    """
    try:
        # Load data
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        
        with open('data/meetings.json', 'r') as f:
            meetings = json.load(f)
        
        # Find the user
        user = None
        for u in users:
            if u['id'] == user_id or u['name'].lower() == user_id.lower():
                user = u
                break
        
        if not user:
            return {
                'success': False,
                'error': f"User '{user_id}' not found"
            }
        
        # Parse time range
        start_time_str, end_time_str = time_range.split(' to ')
        check_start = datetime.fromisoformat(start_time_str)
        check_end = datetime.fromisoformat(end_time_str)
        
        # Find user's meetings in the time range
        user_meetings = []
        for meeting in meetings:
            if user['id'] in meeting['participants'] or user['name'] in meeting['participants']:
                meeting_start = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
                meeting_end = datetime.fromisoformat(meeting['end'].replace('Z', '+00:00'))
                
                # Check if meeting overlaps with the time range
                if (meeting_start < check_end and meeting_end > check_start):
                    user_meetings.append({
                        'meeting_id': meeting['id'],
                        'title': meeting['title'],
                        'start': meeting['start'],
                        'end': meeting['end'],
                        'participants': meeting['participants'],
                        'overlap_start': max(check_start, meeting_start).isoformat(),
                        'overlap_end': min(check_end, meeting_end).isoformat()
                    })
        
        # Analyze conflicts
        conflicts = []
        overlapping_meetings = []
        
        # Check for overlapping meetings
        for i, meeting1 in enumerate(user_meetings):
            for j, meeting2 in enumerate(user_meetings[i+1:], i+1):
                m1_start = datetime.fromisoformat(meeting1['start'].replace('Z', '+00:00'))
                m1_end = datetime.fromisoformat(meeting1['end'].replace('Z', '+00:00'))
                m2_start = datetime.fromisoformat(meeting2['start'].replace('Z', '+00:00'))
                m2_end = datetime.fromisoformat(meeting2['end'].replace('Z', '+00:00'))
                
                # Check for overlap
                if (m1_start < m2_end and m1_end > m2_start):
                    overlap_start = max(m1_start, m2_start)
                    overlap_end = min(m1_end, m2_end)
                    overlap_duration = (overlap_end - overlap_start).total_seconds() / 60
                    
                    conflict = {
                        'type': 'overlapping_meetings',
                        'severity': 'high',
                        'meeting1': {
                            'id': meeting1['meeting_id'],
                            'title': meeting1['title'],
                            'time': f"{meeting1['start']} to {meeting1['end']}"
                        },
                        'meeting2': {
                            'id': meeting2['meeting_id'],
                            'title': meeting2['title'],
                            'time': f"{meeting2['start']} to {meeting2['end']}"
                        },
                        'overlap_duration_minutes': overlap_duration,
                        'overlap_time': f"{overlap_start.isoformat()} to {overlap_end.isoformat()}"
                    }
                    conflicts.append(conflict)
        
        # Check work hours conflicts
        work_start = datetime.strptime(user['work_hours'][0], '%H:%M').time()
        work_end = datetime.strptime(user['work_hours'][1], '%H:%M').time()
        
        for meeting in user_meetings:
            meeting_start = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
            meeting_end = datetime.fromisoformat(meeting['end'].replace('Z', '+00:00'))
            
            # Check if meeting is outside work hours
            if (meeting_start.time() < work_start or meeting_end.time() > work_end):
                conflicts.append({
                    'type': 'outside_work_hours',
                    'severity': 'medium',
                    'meeting': {
                        'id': meeting['meeting_id'],
                        'title': meeting['title'],
                        'time': f"{meeting['start']} to {meeting['end']}"
                    },
                    'work_hours': f"{user['work_hours'][0]} to {user['work_hours'][1]}",
                    'issue': 'Meeting scheduled outside work hours'
                })
        
        # Generate AI insights
        insights = generate_conflict_insights(user, conflicts, user_meetings, check_start, check_end)
        
        return {
            'success': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'timezone': user['timezone'],
                'work_hours': user['work_hours']
            },
            'time_range': {
                'start': check_start.isoformat(),
                'end': check_end.isoformat(),
                'duration_hours': (check_end - check_start).total_seconds() / 3600
            },
            'meetings_in_range': len(user_meetings),
            'conflicts_found': len(conflicts),
            'conflicts': conflicts,
            'meetings': user_meetings,
            'insights': insights
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error detecting conflicts: {str(e)}"
        }

def generate_conflict_insights(user: Dict, conflicts: List[Dict], meetings: List[Dict], start: datetime, end: datetime) -> Dict[str, Any]:
    """Generate AI-powered insights about the conflicts"""
    
    total_meeting_time = 0
    for meeting in meetings:
        m_start = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
        m_end = datetime.fromisoformat(meeting['end'].replace('Z', '+00:00'))
        duration = (m_end - m_start).total_seconds() / 60
        total_meeting_time += duration
    
    total_period_minutes = (end - start).total_seconds() / 60
    meeting_load_percentage = (total_meeting_time / total_period_minutes) * 100 if total_period_minutes > 0 else 0
    
    high_severity_conflicts = len([c for c in conflicts if c.get('severity') == 'high'])
    medium_severity_conflicts = len([c for c in conflicts if c.get('severity') == 'medium'])
    
    # Generate recommendations
    recommendations = []
    
    if high_severity_conflicts > 0:
        recommendations.append("⚠️ Critical: Resolve overlapping meetings immediately")
    
    if medium_severity_conflicts > 0:
        recommendations.append("⚡ Consider rescheduling meetings outside work hours")
    
    if meeting_load_percentage > 80:
        recommendations.append("📊 High meeting load detected - consider reducing meetings")
    elif meeting_load_percentage > 60:
        recommendations.append("📊 Moderate meeting load - monitor workload")
    
    if len(conflicts) == 0:
        recommendations.append("✅ No conflicts detected - schedule looks good!")
    
    return {
        'meeting_load_percentage': round(meeting_load_percentage, 1),
        'total_meeting_time_minutes': total_meeting_time,
        'conflict_severity': {
            'high': high_severity_conflicts,
            'medium': medium_severity_conflicts
        },
        'recommendations': recommendations,
        'status': 'critical' if high_severity_conflicts > 0 else 'warning' if medium_severity_conflicts > 0 else 'good'
    } 
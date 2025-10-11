"""
User Engagement System for Ribit 2.0
Randomly engages users with interesting questions based on their interests
"""

import random
import time
import logging
from typing import Dict, List, Optional, Set
from collections import defaultdict

logger = logging.getLogger(__name__)

class UserEngagementSystem:
    """Proactive user engagement with personalized questions"""
    
    def __init__(self):
        self.user_activity = defaultdict(list)  # Track user activity
        self.user_interests = defaultdict(set)  # Track user interests
        self.last_engagement = {}  # Track when we last pinged each user
        self.engagement_cooldown = 3600  # 1 hour between pings
        
    def track_user_activity(self, user_id: str, room_id: str, message: str):
        """Track user activity and extract interests"""
        self.user_activity[user_id].append({
            'timestamp': time.time(),
            'room_id': room_id,
            'message_length': len(message)
        })
        
        # Extract interests from message
        interests = self._extract_interests(message)
        self.user_interests[user_id].update(interests)
        
        # Keep only last 50 activities
        if len(self.user_activity[user_id]) > 50:
            self.user_activity[user_id] = self.user_activity[user_id][-50:]
    
    def _extract_interests(self, message: str) -> Set[str]:
        """Extract user interests from their messages"""
        interests = set()
        message_lower = message.lower()
        
        # Programming languages
        prog_langs = ['python', 'javascript', 'java', 'c++', 'rust', 'go', 'ruby', 'php']
        for lang in prog_langs:
            if lang in message_lower:
                interests.add(f"programming:{lang}")
        
        # Technologies
        technologies = ['ai', 'machine learning', 'web development', 'database', 'docker', 
                       'kubernetes', 'react', 'vue', 'angular', 'node']
        for tech in technologies:
            if tech in message_lower:
                interests.add(f"technology:{tech}")
        
        # Topics
        topics = ['philosophy', 'history', 'science', 'mathematics', 'physics', 
                 'biology', 'psychology', 'art', 'music', 'gaming']
        for topic in topics:
            if topic in message_lower:
                interests.add(f"topic:{topic}")
        
        # Hobbies/Activities
        hobbies = ['reading', 'writing', 'coding', 'gaming', 'music', 'art', 
                  'sports', 'cooking', 'travel']
        for hobby in hobbies:
            if hobby in message_lower:
                interests.add(f"hobby:{hobby}")
        
        return interests
    
    def get_recently_active_users(self, room_id: str, time_window: int = 7200) -> List[str]:
        """Get users who were recently active in a room"""
        cutoff_time = time.time() - time_window
        active_users = []
        
        for user_id, activities in self.user_activity.items():
            # Check if user was active in this room recently
            recent_in_room = [
                a for a in activities
                if a['room_id'] == room_id and a['timestamp'] > cutoff_time
            ]
            if recent_in_room:
                active_users.append(user_id)
        
        return active_users
    
    def can_engage_user(self, user_id: str) -> bool:
        """Check if we can engage this user (not too soon after last engagement)"""
        if user_id not in self.last_engagement:
            return True
        
        time_since_last = time.time() - self.last_engagement[user_id]
        return time_since_last > self.engagement_cooldown
    
    def select_random_user(self, room_id: str, exclude_users: Optional[List[str]] = None) -> Optional[str]:
        """Select a random recently active user to engage"""
        active_users = self.get_recently_active_users(room_id)
        
        # Filter out excluded users and users on cooldown
        eligible_users = [
            user for user in active_users
            if (not exclude_users or user not in exclude_users)
            and self.can_engage_user(user)
        ]
        
        if not eligible_users:
            return None
        
        return random.choice(eligible_users)
    
    def generate_personalized_question(self, user_id: str) -> str:
        """Generate a personalized question based on user's interests"""
        interests = list(self.user_interests.get(user_id, set()))
        
        if not interests:
            # Generic questions if no interests known
            return random.choice(self._get_generic_questions())
        
        # Pick a random interest
        interest = random.choice(interests)
        interest_type, interest_value = interest.split(':', 1) if ':' in interest else ('general', interest)
        
        # Generate question based on interest type
        if interest_type == 'programming':
            return self._get_programming_question(interest_value)
        elif interest_type == 'technology':
            return self._get_technology_question(interest_value)
        elif interest_type == 'topic':
            return self._get_topic_question(interest_value)
        elif interest_type == 'hobby':
            return self._get_hobby_question(interest_value)
        else:
            return random.choice(self._get_generic_questions())
    
    def _get_programming_question(self, language: str) -> str:
        """Get programming-related question"""
        questions = [
            f"What's your favorite feature in {language}?",
            f"Have you tried any new {language} frameworks lately?",
            f"What's the most challenging {language} project you've worked on?",
            f"Do you prefer {language} for backend or frontend development?",
            f"What's one thing you wish {language} had?",
            f"How did you first learn {language}?",
        ]
        return random.choice(questions)
    
    def _get_technology_question(self, tech: str) -> str:
        """Get technology-related question"""
        questions = [
            f"What do you think about the future of {tech}?",
            f"Have you used {tech} in any recent projects?",
            f"What's the biggest challenge with {tech} in your opinion?",
            f"Do you think {tech} is overhyped or underhyped?",
            f"What resources would you recommend for learning {tech}?",
        ]
        return random.choice(questions)
    
    def _get_topic_question(self, topic: str) -> str:
        """Get topic-related question"""
        questions = [
            f"What aspect of {topic} interests you most?",
            f"Have you read any good books about {topic} lately?",
            f"What's a common misconception about {topic}?",
            f"How did you get interested in {topic}?",
            f"What's the most fascinating thing you've learned about {topic}?",
        ]
        return random.choice(questions)
    
    def _get_hobby_question(self, hobby: str) -> str:
        """Get hobby-related question"""
        questions = [
            f"How long have you been into {hobby}?",
            f"What got you started with {hobby}?",
            f"Do you have any {hobby} recommendations?",
            f"What's your favorite thing about {hobby}?",
            f"Have you discovered anything new in {hobby} recently?",
        ]
        return random.choice(questions)
    
    def _get_generic_questions(self) -> List[str]:
        """Get generic interesting questions"""
        return [
            "What's something interesting you learned recently?",
            "If you could master any skill instantly, what would it be?",
            "What's a technology you're excited about?",
            "What's your favorite way to learn new things?",
            "What project are you working on these days?",
            "What's a problem you'd love to solve?",
            "What's your take on AI and the future?",
            "What's something you're curious about?",
            "If you could time travel, which era would you visit?",
            "What's a book or article that changed your perspective?",
            "What's your favorite productivity hack?",
            "What's something you wish more people knew about?",
        ]
    
    def mark_engaged(self, user_id: str):
        """Mark that we've engaged this user"""
        self.last_engagement[user_id] = time.time()
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Get user engagement profile"""
        activities = self.user_activity.get(user_id, [])
        interests = list(self.user_interests.get(user_id, set()))
        
        if not activities:
            return {'profile_available': False}
        
        # Calculate activity statistics
        total_messages = len(activities)
        recent_activity = [a for a in activities if time.time() - a['timestamp'] < 86400]  # Last 24h
        avg_message_length = sum(a['message_length'] for a in activities) / len(activities)
        
        return {
            'profile_available': True,
            'total_messages': total_messages,
            'recent_messages_24h': len(recent_activity),
            'avg_message_length': avg_message_length,
            'interests': interests,
            'activity_level': 'high' if len(recent_activity) > 10 else 'moderate' if len(recent_activity) > 3 else 'low',
            'last_active': max(a['timestamp'] for a in activities) if activities else None,
        }
    
    def should_engage_room(self, room_id: str, min_users: int = 2, time_window: int = 3600) -> bool:
        """Determine if we should proactively engage users in this room"""
        active_users = self.get_recently_active_users(room_id, time_window)
        
        # Need minimum number of active users
        if len(active_users) < min_users:
            return False
        
        # Check if any users are eligible for engagement
        eligible = [user for user in active_users if self.can_engage_user(user)]
        
        return len(eligible) > 0
    
    def get_engagement_statistics(self) -> Dict:
        """Get engagement statistics"""
        return {
            'total_users_tracked': len(self.user_activity),
            'users_with_interests': len(self.user_interests),
            'total_interests_tracked': sum(len(interests) for interests in self.user_interests.values()),
            'users_engaged': len(self.last_engagement),
        }


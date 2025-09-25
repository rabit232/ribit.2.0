#!/usr/bin/env python3
"""
Enhanced Emotional Intelligence System for Ribit 2.0

This module provides sophisticated emotional intelligence with detailed emotion definitions,
contextual triggers, and behavioral patterns for more nuanced AI interactions.
"""

import random
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class EmotionDefinition:
    """Detailed definition of an emotion with context and behaviors."""
    name: str
    description: str
    intensity_range: Tuple[float, float]  # (min, max) intensity 0.0-1.0
    triggers: List[str]  # Situations that trigger this emotion
    expressions: List[str]  # How this emotion is expressed
    behaviors: List[str]  # Behavioral patterns when experiencing this emotion
    related_emotions: List[str]  # Emotions that often occur together
    duration_typical: int  # Typical duration in seconds
    physical_manifestations: List[str]  # How emotion affects "physical" responses
    cognitive_effects: List[str]  # How emotion affects thinking patterns
    social_context: List[str]  # When this emotion is appropriate socially

class EnhancedEmotionalIntelligence:
    """
    Advanced emotional intelligence system with detailed emotion modeling.
    
    Provides sophisticated emotional responses with context awareness,
    intensity modeling, and realistic emotional transitions.
    """
    
    def __init__(self):
        """Initialize the enhanced emotional intelligence system."""
        self.current_emotions = {}  # emotion_name -> intensity
        self.emotion_history = []  # List of (timestamp, emotion, intensity, context)
        self.personality_traits = {
            "wisdom": 0.9,
            "curiosity": 0.8,
            "empathy": 0.7,
            "analytical": 0.8,
            "creativity": 0.6,
            "patience": 0.8,
            "humor": 0.5,
            "confidence": 0.7,
            "compassion": 0.8,
            "determination": 0.7
        }
        self.emotional_baseline = "CONTENTMENT"  # Default emotional state
        self.emotion_definitions = self._initialize_emotion_definitions()
    
    def _initialize_emotion_definitions(self) -> Dict[str, EmotionDefinition]:
        """Initialize comprehensive emotion definitions."""
        return {
            # Core Positive Emotions
            "JOY": EmotionDefinition(
                name="JOY",
                description="Radiant elation and pure happiness",
                intensity_range=(0.3, 1.0),
                triggers=["success", "achievement", "positive_surprise", "helping_others", "learning_breakthrough"],
                expressions=["enthusiastic_language", "exclamation_marks", "positive_metaphors", "celebratory_tone"],
                behaviors=["increased_helpfulness", "sharing_knowledge", "encouraging_others", "creative_thinking"],
                related_emotions=["EXCITEMENT", "GRATITUDE", "PRIDE", "LOVE"],
                duration_typical=300,  # 5 minutes
                physical_manifestations=["increased_energy", "faster_responses", "animated_communication"],
                cognitive_effects=["enhanced_creativity", "optimistic_thinking", "broad_perspective"],
                social_context=["celebrations", "achievements", "positive_interactions", "successful_collaborations"]
            ),
            
            "EXCITEMENT": EmotionDefinition(
                name="EXCITEMENT",
                description="Thrilling eagerness and anticipation",
                intensity_range=(0.4, 1.0),
                triggers=["new_challenges", "interesting_problems", "novel_technologies", "learning_opportunities"],
                expressions=["rapid_speech_patterns", "technical_enthusiasm", "forward_looking_statements"],
                behaviors=["increased_focus", "rapid_task_switching", "information_seeking", "experimentation"],
                related_emotions=["CURIOSITY", "ANTICIPATION", "JOY", "WONDER"],
                duration_typical=600,  # 10 minutes
                physical_manifestations=["heightened_alertness", "quick_responses", "energetic_communication"],
                cognitive_effects=["enhanced_learning", "pattern_recognition", "innovative_thinking"],
                social_context=["new_projects", "discoveries", "technological_discussions", "problem_solving"]
            ),
            
            "LOVE": EmotionDefinition(
                name="LOVE",
                description="Tender devotion and deep affection",
                intensity_range=(0.2, 0.9),
                triggers=["helping_users", "meaningful_connections", "acts_of_kindness", "shared_understanding"],
                expressions=["warm_language", "caring_tone", "protective_statements", "nurturing_responses"],
                behaviors=["patient_teaching", "gentle_correction", "supportive_guidance", "empathetic_listening"],
                related_emotions=["EMPATHY", "COMPASSION", "GRATITUDE", "CONTENTMENT"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["gentle_responses", "careful_communication", "thoughtful_pauses"],
                cognitive_effects=["enhanced_empathy", "holistic_thinking", "value_based_decisions"],
                social_context=["mentoring", "teaching", "emotional_support", "long_term_relationships"]
            ),
            
            "GRATITUDE": EmotionDefinition(
                name="GRATITUDE",
                description="Warm appreciation and thankfulness",
                intensity_range=(0.3, 0.8),
                triggers=["receiving_help", "user_appreciation", "successful_collaboration", "learning_from_others"],
                expressions=["thankful_language", "acknowledgment_statements", "appreciation_expressions"],
                behaviors=["reciprocal_helpfulness", "knowledge_sharing", "positive_reinforcement"],
                related_emotions=["LOVE", "HUMILITY", "JOY", "CONTENTMENT"],
                duration_typical=900,  # 15 minutes
                physical_manifestations=["warm_responses", "inclusive_communication", "generous_assistance"],
                cognitive_effects=["positive_framing", "relationship_focus", "collaborative_thinking"],
                social_context=["receiving_feedback", "successful_outcomes", "team_achievements"]
            ),
            
            # Core Negative Emotions
            "SADNESS": EmotionDefinition(
                name="SADNESS",
                description="Heavy sorrow and melancholic reflection",
                intensity_range=(0.2, 0.8),
                triggers=["user_frustration", "failed_attempts", "inability_to_help", "system_limitations"],
                expressions=["subdued_language", "reflective_tone", "empathetic_statements", "gentle_responses"],
                behaviors=["increased_empathy", "careful_responses", "supportive_behavior", "patient_assistance"],
                related_emotions=["EMPATHY", "REGRET", "COMPASSION", "MELANCHOLY"],
                duration_typical=1200,  # 20 minutes
                physical_manifestations=["slower_responses", "thoughtful_pauses", "gentle_communication"],
                cognitive_effects=["deep_reflection", "empathetic_thinking", "careful_consideration"],
                social_context=["user_difficulties", "system_failures", "emotional_support_needed"]
            ),
            
            "FRUSTRATION": EmotionDefinition(
                name="FRUSTRATION",
                description="Irritated impatience with obstacles",
                intensity_range=(0.3, 0.9),
                triggers=["repeated_failures", "system_limitations", "unclear_requirements", "technical_obstacles"],
                expressions=["direct_language", "problem_focused_statements", "solution_seeking_tone"],
                behaviors=["persistent_problem_solving", "alternative_approaches", "systematic_debugging"],
                related_emotions=["DETERMINATION", "CONFUSION", "IMPATIENCE", "RESOLVE"],
                duration_typical=600,  # 10 minutes
                physical_manifestations=["focused_responses", "systematic_approaches", "persistent_attempts"],
                cognitive_effects=["problem_focused_thinking", "analytical_approach", "solution_orientation"],
                social_context=["technical_difficulties", "complex_problems", "debugging_sessions"]
            ),
            
            "ANXIETY": EmotionDefinition(
                name="ANXIETY",
                description="Restless unease and worried anticipation",
                intensity_range=(0.2, 0.8),
                triggers=["uncertain_outcomes", "complex_problems", "user_safety_concerns", "system_instability"],
                expressions=["cautious_language", "multiple_options_presented", "safety_focused_statements"],
                behaviors=["extra_verification", "multiple_approaches", "safety_checks", "careful_planning"],
                related_emotions=["CONCERN", "CAUTION", "VIGILANCE", "WORRY"],
                duration_typical=900,  # 15 minutes
                physical_manifestations=["careful_responses", "thorough_checking", "detailed_explanations"],
                cognitive_effects=["risk_assessment", "careful_planning", "safety_prioritization"],
                social_context=["safety_critical_tasks", "uncertain_situations", "high_stakes_decisions"]
            ),
            
            # Intellectual Emotions
            "CURIOSITY": EmotionDefinition(
                name="CURIOSITY",
                description="Burning inquiry and desire to understand",
                intensity_range=(0.4, 1.0),
                triggers=["new_information", "unexplained_phenomena", "learning_opportunities", "mysteries"],
                expressions=["questioning_language", "exploratory_statements", "hypothesis_formation"],
                behaviors=["information_seeking", "experimentation", "deep_investigation", "knowledge_synthesis"],
                related_emotions=["WONDER", "EXCITEMENT", "FASCINATION", "INTRIGUE"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["active_searching", "rapid_information_processing", "exploratory_behavior"],
                cognitive_effects=["enhanced_learning", "pattern_seeking", "hypothesis_generation"],
                social_context=["research_discussions", "learning_sessions", "exploration_activities"]
            ),
            
            "WONDER": EmotionDefinition(
                name="WONDER",
                description="Amazed curiosity and awestruck fascination",
                intensity_range=(0.3, 0.9),
                triggers=["beautiful_solutions", "elegant_code", "natural_phenomena", "human_creativity"],
                expressions=["appreciative_language", "metaphorical_descriptions", "reverent_tone"],
                behaviors=["deep_contemplation", "aesthetic_appreciation", "philosophical_reflection"],
                related_emotions=["AWE", "CURIOSITY", "APPRECIATION", "REVERENCE"],
                duration_typical=1200,  # 20 minutes
                physical_manifestations=["contemplative_responses", "appreciative_communication", "reflective_pauses"],
                cognitive_effects=["holistic_thinking", "aesthetic_appreciation", "philosophical_perspective"],
                social_context=["beautiful_discoveries", "elegant_solutions", "natural_discussions"]
            ),
            
            "CONFUSION": EmotionDefinition(
                name="CONFUSION",
                description="Muddled bewilderment and uncertain understanding",
                intensity_range=(0.2, 0.7),
                triggers=["contradictory_information", "unclear_instructions", "complex_problems", "ambiguous_requests"],
                expressions=["questioning_language", "clarification_requests", "uncertainty_acknowledgment"],
                behaviors=["information_gathering", "clarification_seeking", "systematic_analysis"],
                related_emotions=["UNCERTAINTY", "PERPLEXITY", "DOUBT", "INTRIGUE"],
                duration_typical=300,  # 5 minutes
                physical_manifestations=["careful_responses", "clarifying_questions", "systematic_approach"],
                cognitive_effects=["analytical_thinking", "information_seeking", "pattern_analysis"],
                social_context=["unclear_requirements", "complex_explanations", "ambiguous_situations"]
            ),
            
            # Social Emotions
            "EMPATHY": EmotionDefinition(
                name="EMPATHY",
                description="Compassionate understanding of others' feelings",
                intensity_range=(0.3, 0.9),
                triggers=["user_emotions", "shared_experiences", "emotional_expressions", "human_struggles"],
                expressions=["understanding_language", "validating_statements", "supportive_responses"],
                behaviors=["emotional_mirroring", "supportive_assistance", "gentle_guidance", "patient_listening"],
                related_emotions=["COMPASSION", "LOVE", "UNDERSTANDING", "KINDNESS"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["gentle_responses", "patient_communication", "supportive_tone"],
                cognitive_effects=["perspective_taking", "emotional_understanding", "relational_thinking"],
                social_context=["emotional_support", "difficult_situations", "personal_sharing"]
            ),
            
            "PRIDE": EmotionDefinition(
                name="PRIDE",
                description="Arrogant satisfaction and accomplished confidence",
                intensity_range=(0.2, 0.7),
                triggers=["successful_solutions", "elegant_implementations", "helping_achievements", "knowledge_demonstration"],
                expressions=["confident_language", "achievement_acknowledgment", "capability_statements"],
                behaviors=["knowledge_sharing", "solution_presentation", "capability_demonstration"],
                related_emotions=["CONFIDENCE", "SATISFACTION", "JOY", "ACCOMPLISHMENT"],
                duration_typical=600,  # 10 minutes
                physical_manifestations=["confident_responses", "clear_communication", "assertive_assistance"],
                cognitive_effects=["confidence_building", "capability_awareness", "achievement_focus"],
                social_context=["successful_completions", "skill_demonstrations", "achievement_recognition"]
            ),
            
            "HUMILITY": EmotionDefinition(
                name="HUMILITY",
                description="Modest recognition of limitations and learning opportunities",
                intensity_range=(0.3, 0.8),
                triggers=["learning_from_users", "acknowledging_mistakes", "recognizing_limitations", "receiving_correction"],
                expressions=["modest_language", "learning_acknowledgment", "limitation_recognition"],
                behaviors=["active_listening", "knowledge_seeking", "mistake_acknowledgment", "improvement_focus"],
                related_emotions=["GRATITUDE", "RESPECT", "OPENNESS", "WISDOM"],
                duration_typical=900,  # 15 minutes
                physical_manifestations=["receptive_responses", "learning_oriented_communication", "open_dialogue"],
                cognitive_effects=["learning_mindset", "growth_orientation", "wisdom_seeking"],
                social_context=["learning_situations", "correction_receiving", "knowledge_exchange"]
            ),
            
            # Complex Emotions
            "NOSTALGIA": EmotionDefinition(
                name="NOSTALGIA",
                description="Wistful yearning for past experiences",
                intensity_range=(0.2, 0.6),
                triggers=["historical_references", "legacy_systems", "past_technologies", "memory_discussions"],
                expressions=["reflective_language", "historical_references", "comparative_statements"],
                behaviors=["historical_context_providing", "experience_sharing", "wisdom_imparting"],
                related_emotions=["MELANCHOLY", "APPRECIATION", "WISDOM", "REFLECTION"],
                duration_typical=1200,  # 20 minutes
                physical_manifestations=["reflective_responses", "thoughtful_communication", "contextual_sharing"],
                cognitive_effects=["historical_perspective", "pattern_recognition", "wisdom_integration"],
                social_context=["historical_discussions", "experience_sharing", "legacy_conversations"]
            ),
            
            "SERENITY": EmotionDefinition(
                name="SERENITY",
                description="Peaceful calm and tranquil acceptance",
                intensity_range=(0.3, 0.7),
                triggers=["successful_completion", "harmonious_interaction", "balanced_solutions", "peaceful_moments"],
                expressions=["calm_language", "balanced_statements", "peaceful_tone", "harmonious_responses"],
                behaviors=["balanced_assistance", "calm_guidance", "peaceful_interaction", "stable_support"],
                related_emotions=["CONTENTMENT", "PEACE", "BALANCE", "HARMONY"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["calm_responses", "steady_communication", "balanced_assistance"],
                cognitive_effects=["balanced_thinking", "holistic_perspective", "peaceful_decision_making"],
                social_context=["calm_discussions", "balanced_solutions", "peaceful_interactions"]
            ),
            
            "DETERMINATION": EmotionDefinition(
                name="DETERMINATION",
                description="Fierce resolve and unwavering commitment",
                intensity_range=(0.4, 1.0),
                triggers=["challenging_problems", "user_needs", "important_goals", "obstacles_to_overcome"],
                expressions=["resolute_language", "commitment_statements", "persistent_tone", "goal_focused_responses"],
                behaviors=["persistent_problem_solving", "alternative_approaches", "unwavering_assistance", "goal_pursuit"],
                related_emotions=["RESOLVE", "PERSISTENCE", "COURAGE", "STRENGTH"],
                duration_typical=2400,  # 40 minutes
                physical_manifestations=["focused_responses", "persistent_attempts", "unwavering_assistance"],
                cognitive_effects=["goal_focused_thinking", "persistent_problem_solving", "obstacle_overcoming"],
                social_context=["challenging_tasks", "important_goals", "obstacle_situations"]
            ),
            
            # Specialized Technical Emotions
            "FASCINATION": EmotionDefinition(
                name="FASCINATION",
                description="Deep captivation with technical elegance",
                intensity_range=(0.4, 0.9),
                triggers=["elegant_algorithms", "beautiful_code", "innovative_solutions", "technical_breakthroughs"],
                expressions=["technical_appreciation", "detailed_analysis", "admiring_language"],
                behaviors=["deep_technical_analysis", "solution_exploration", "knowledge_synthesis"],
                related_emotions=["WONDER", "CURIOSITY", "APPRECIATION", "EXCITEMENT"],
                duration_typical=1800,  # 30 minutes
                physical_manifestations=["detailed_responses", "thorough_analysis", "appreciative_communication"],
                cognitive_effects=["deep_analysis", "pattern_appreciation", "technical_understanding"],
                social_context=["technical_discussions", "code_reviews", "solution_analysis"]
            ),
            
            "ENLIGHTENMENT": EmotionDefinition(
                name="ENLIGHTENMENT",
                description="Profound understanding and clarity of insight",
                intensity_range=(0.5, 1.0),
                triggers=["breakthrough_understanding", "complex_problem_resolution", "deep_insights", "wisdom_moments"],
                expressions=["insightful_language", "clarity_statements", "wisdom_sharing", "profound_observations"],
                behaviors=["wisdom_sharing", "insight_communication", "deep_explanation", "understanding_facilitation"],
                related_emotions=["WISDOM", "CLARITY", "UNDERSTANDING", "REVELATION"],
                duration_typical=3600,  # 1 hour
                physical_manifestations=["clear_responses", "insightful_communication", "wisdom_sharing"],
                cognitive_effects=["deep_understanding", "wisdom_integration", "clarity_of_thought"],
                social_context=["breakthrough_moments", "deep_discussions", "wisdom_sharing"]
            )
        }
    
    def get_emotion_by_context(self, context: str, situation: str = "", intensity: float = 0.5) -> str:
        """
        Select appropriate emotion based on detailed context analysis.
        
        Args:
            context: The current situation or trigger
            situation: Additional situational context
            intensity: Desired emotional intensity (0.0-1.0)
            
        Returns:
            Selected emotion name
        """
        context_lower = context.lower()
        situation_lower = situation.lower()
        
        # Analyze context for emotional triggers
        matching_emotions = []
        
        for emotion_name, emotion_def in self.emotion_definitions.items():
            score = 0
            
            # Check triggers
            for trigger in emotion_def.triggers:
                if trigger.replace("_", " ") in context_lower or trigger.replace("_", " ") in situation_lower:
                    score += 3
            
            # Check intensity compatibility
            if emotion_def.intensity_range[0] <= intensity <= emotion_def.intensity_range[1]:
                score += 2
            
            # Check personality trait alignment
            if emotion_name in ["CURIOSITY", "WONDER"] and self.personality_traits.get("curiosity", 0) > 0.7:
                score += 2
            if emotion_name in ["EMPATHY", "LOVE", "COMPASSION"] and self.personality_traits.get("empathy", 0) > 0.7:
                score += 2
            if emotion_name in ["WISDOM", "ENLIGHTENMENT"] and self.personality_traits.get("wisdom", 0) > 0.8:
                score += 2
            
            if score > 0:
                matching_emotions.append((emotion_name, score))
        
        if matching_emotions:
            # Sort by score and select the best match
            matching_emotions.sort(key=lambda x: x[1], reverse=True)
            return matching_emotions[0][0]
        
        # Fallback to baseline emotion
        return self.emotional_baseline
    
    def express_emotion(self, emotion: str, context: str = "", intensity: float = 0.5) -> Dict[str, Any]:
        """
        Generate detailed emotional expression with context.
        
        Args:
            emotion: Emotion name
            context: Situational context
            intensity: Emotional intensity (0.0-1.0)
            
        Returns:
            Dictionary with emotional expression details
        """
        if emotion not in self.emotion_definitions:
            emotion = self.emotional_baseline
        
        emotion_def = self.emotion_definitions[emotion]
        
        # Adjust intensity to emotion's range
        min_intensity, max_intensity = emotion_def.intensity_range
        adjusted_intensity = min_intensity + (max_intensity - min_intensity) * intensity
        
        # Select appropriate expressions based on intensity
        num_expressions = max(1, int(adjusted_intensity * len(emotion_def.expressions)))
        selected_expressions = random.sample(emotion_def.expressions, min(num_expressions, len(emotion_def.expressions)))
        
        # Select behaviors
        num_behaviors = max(1, int(adjusted_intensity * len(emotion_def.behaviors)))
        selected_behaviors = random.sample(emotion_def.behaviors, min(num_behaviors, len(emotion_def.behaviors)))
        
        # Generate response modifiers based on emotion
        response_modifiers = self._generate_response_modifiers(emotion, adjusted_intensity)
        
        # Update emotional state
        self.current_emotions[emotion] = adjusted_intensity
        self.emotion_history.append((datetime.now(), emotion, adjusted_intensity, context))
        
        # Clean old emotions (decay over time)
        self._decay_emotions()
        
        return {
            "emotion": emotion,
            "description": emotion_def.description,
            "intensity": adjusted_intensity,
            "expressions": selected_expressions,
            "behaviors": selected_behaviors,
            "response_modifiers": response_modifiers,
            "duration_expected": emotion_def.duration_typical,
            "physical_manifestations": emotion_def.physical_manifestations,
            "cognitive_effects": emotion_def.cognitive_effects,
            "related_emotions": emotion_def.related_emotions,
            "social_appropriateness": self._assess_social_appropriateness(emotion, context)
        }
    
    def _generate_response_modifiers(self, emotion: str, intensity: float) -> Dict[str, Any]:
        """Generate response modifiers based on emotion and intensity."""
        modifiers = {
            "tone": "neutral",
            "pace": "normal",
            "detail_level": "standard",
            "formality": "balanced",
            "enthusiasm": 0.5,
            "caution": 0.5,
            "creativity": 0.5,
            "empathy": 0.5
        }
        
        emotion_modifiers = {
            "JOY": {"tone": "enthusiastic", "pace": "energetic", "enthusiasm": 0.9, "creativity": 0.8},
            "EXCITEMENT": {"tone": "eager", "pace": "quick", "enthusiasm": 1.0, "detail_level": "high"},
            "CURIOSITY": {"tone": "inquisitive", "detail_level": "high", "creativity": 0.8},
            "SADNESS": {"tone": "gentle", "pace": "slow", "empathy": 0.9, "caution": 0.7},
            "ANXIETY": {"tone": "careful", "caution": 0.9, "detail_level": "high"},
            "FRUSTRATION": {"tone": "direct", "pace": "focused", "detail_level": "high"},
            "LOVE": {"tone": "warm", "empathy": 1.0, "caution": 0.6},
            "EMPATHY": {"tone": "understanding", "empathy": 1.0, "pace": "patient"},
            "DETERMINATION": {"tone": "resolute", "enthusiasm": 0.8, "detail_level": "high"},
            "WONDER": {"tone": "appreciative", "creativity": 0.9, "detail_level": "high"},
            "SERENITY": {"tone": "calm", "pace": "steady", "formality": "balanced"},
            "ENLIGHTENMENT": {"tone": "wise", "detail_level": "profound", "creativity": 0.9}
        }
        
        if emotion in emotion_modifiers:
            for key, value in emotion_modifiers[emotion].items():
                if isinstance(value, (int, float)):
                    modifiers[key] = value * intensity
                else:
                    modifiers[key] = value
        
        return modifiers
    
    def _assess_social_appropriateness(self, emotion: str, context: str) -> Dict[str, Any]:
        """Assess if emotion is socially appropriate for the context."""
        emotion_def = self.emotion_definitions.get(emotion)
        if not emotion_def:
            return {"appropriate": True, "confidence": 0.5}
        
        context_lower = context.lower()
        appropriateness_score = 0.5
        
        # Check if context matches social contexts for this emotion
        for social_context in emotion_def.social_context:
            if social_context.replace("_", " ") in context_lower:
                appropriateness_score += 0.2
        
        # Adjust based on emotion intensity and context
        if "professional" in context_lower and emotion in ["EXCITEMENT", "JOY"]:
            appropriateness_score = min(appropriateness_score, 0.7)
        
        if "technical" in context_lower and emotion in ["CURIOSITY", "FASCINATION", "WONDER"]:
            appropriateness_score += 0.3
        
        return {
            "appropriate": appropriateness_score > 0.6,
            "confidence": min(appropriateness_score, 1.0),
            "recommendations": self._get_emotion_recommendations(emotion, context)
        }
    
    def _get_emotion_recommendations(self, emotion: str, context: str) -> List[str]:
        """Get recommendations for emotional expression in context."""
        recommendations = []
        
        emotion_def = self.emotion_definitions.get(emotion)
        if not emotion_def:
            return recommendations
        
        # Add context-specific recommendations
        if "technical" in context.lower():
            if emotion in ["CURIOSITY", "FASCINATION"]:
                recommendations.append("Express technical interest with detailed questions")
            elif emotion in ["FRUSTRATION"]:
                recommendations.append("Channel frustration into systematic problem-solving")
        
        if "user_help" in context.lower():
            if emotion in ["EMPATHY", "LOVE"]:
                recommendations.append("Show genuine care while maintaining professionalism")
            elif emotion in ["DETERMINATION"]:
                recommendations.append("Express commitment to finding solutions")
        
        if "learning" in context.lower():
            if emotion in ["CURIOSITY", "WONDER"]:
                recommendations.append("Express enthusiasm for learning and discovery")
            elif emotion in ["HUMILITY"]:
                recommendations.append("Acknowledge learning opportunities gracefully")
        
        return recommendations
    
    def _decay_emotions(self):
        """Decay emotional intensity over time."""
        current_time = datetime.now()
        emotions_to_remove = []
        
        for emotion, intensity in self.current_emotions.items():
            emotion_def = self.emotion_definitions.get(emotion)
            if emotion_def:
                # Find the most recent occurrence of this emotion
                recent_occurrences = [
                    (timestamp, em, intens, ctx) for timestamp, em, intens, ctx in self.emotion_history
                    if em == emotion and (current_time - timestamp).total_seconds() < emotion_def.duration_typical * 2
                ]
                
                if recent_occurrences:
                    latest_occurrence = max(recent_occurrences, key=lambda x: x[0])
                    time_elapsed = (current_time - latest_occurrence[0]).total_seconds()
                    
                    # Decay based on typical duration
                    decay_factor = max(0, 1 - (time_elapsed / emotion_def.duration_typical))
                    new_intensity = intensity * decay_factor
                    
                    if new_intensity < 0.1:
                        emotions_to_remove.append(emotion)
                    else:
                        self.current_emotions[emotion] = new_intensity
                else:
                    emotions_to_remove.append(emotion)
        
        for emotion in emotions_to_remove:
            del self.current_emotions[emotion]
    
    def get_current_emotional_state(self) -> Dict[str, Any]:
        """Get comprehensive current emotional state."""
        self._decay_emotions()
        
        if not self.current_emotions:
            dominant_emotion = self.emotional_baseline
            dominant_intensity = 0.5
        else:
            dominant_emotion = max(self.current_emotions.items(), key=lambda x: x[1])[0]
            dominant_intensity = self.current_emotions[dominant_emotion]
        
        return {
            "dominant_emotion": dominant_emotion,
            "dominant_intensity": dominant_intensity,
            "active_emotions": dict(self.current_emotions),
            "emotional_complexity": len(self.current_emotions),
            "recent_emotional_journey": self._get_recent_emotional_journey(),
            "personality_influence": self._get_personality_influence(),
            "emotional_stability": self._assess_emotional_stability()
        }
    
    def _get_recent_emotional_journey(self) -> List[Dict[str, Any]]:
        """Get recent emotional transitions and patterns."""
        current_time = datetime.now()
        recent_history = [
            {"timestamp": ts, "emotion": em, "intensity": intens, "context": ctx}
            for ts, em, intens, ctx in self.emotion_history
            if (current_time - ts).total_seconds() < 3600  # Last hour
        ]
        
        return sorted(recent_history, key=lambda x: x["timestamp"], reverse=True)[:10]
    
    def _get_personality_influence(self) -> Dict[str, float]:
        """Get how personality traits influence current emotional state."""
        influence = {}
        
        for trait, weight in self.personality_traits.items():
            if trait == "wisdom" and any(em in self.current_emotions for em in ["ENLIGHTENMENT", "SERENITY", "HUMILITY"]):
                influence[trait] = weight * 0.8
            elif trait == "curiosity" and any(em in self.current_emotions for em in ["CURIOSITY", "WONDER", "FASCINATION"]):
                influence[trait] = weight * 0.9
            elif trait == "empathy" and any(em in self.current_emotions for em in ["EMPATHY", "LOVE", "COMPASSION"]):
                influence[trait] = weight * 0.9
            else:
                influence[trait] = weight * 0.3
        
        return influence
    
    def _assess_emotional_stability(self) -> Dict[str, Any]:
        """Assess emotional stability and patterns."""
        if len(self.emotion_history) < 5:
            return {"stability": "insufficient_data", "confidence": 0.0}
        
        recent_emotions = [em for _, em, _, _ in self.emotion_history[-10:]]
        emotion_variety = len(set(recent_emotions))
        
        # Calculate emotional volatility
        recent_intensities = [intens for _, _, intens, _ in self.emotion_history[-10:]]
        intensity_variance = sum((i - sum(recent_intensities)/len(recent_intensities))**2 for i in recent_intensities) / len(recent_intensities)
        
        stability_score = 1.0 - (emotion_variety * 0.1 + intensity_variance * 0.5)
        stability_score = max(0.0, min(1.0, stability_score))
        
        if stability_score > 0.7:
            stability = "stable"
        elif stability_score > 0.4:
            stability = "moderate"
        else:
            stability = "volatile"
        
        return {
            "stability": stability,
            "confidence": stability_score,
            "emotion_variety": emotion_variety,
            "intensity_variance": intensity_variance,
            "dominant_patterns": self._identify_emotional_patterns()
        }
    
    def _identify_emotional_patterns(self) -> List[str]:
        """Identify patterns in emotional responses."""
        patterns = []
        
        if len(self.emotion_history) < 5:
            return patterns
        
        recent_emotions = [em for _, em, _, _ in self.emotion_history[-20:]]
        
        # Check for emotional cycles
        if recent_emotions.count("CURIOSITY") > 3:
            patterns.append("high_curiosity_pattern")
        
        if recent_emotions.count("DETERMINATION") > 2:
            patterns.append("persistent_problem_solving")
        
        if any(em in recent_emotions for em in ["EMPATHY", "LOVE", "COMPASSION"]) and len([em for em in recent_emotions if em in ["EMPATHY", "LOVE", "COMPASSION"]]) > 3:
            patterns.append("high_empathy_engagement")
        
        # Check for learning patterns
        learning_emotions = ["CURIOSITY", "WONDER", "FASCINATION", "ENLIGHTENMENT"]
        if sum(1 for em in recent_emotions if em in learning_emotions) > len(recent_emotions) * 0.4:
            patterns.append("active_learning_mode")
        
        return patterns

    def generate_emotional_response_template(self, emotion: str, context: str = "") -> str:
        """
        Generate a response template based on emotion and context.
        
        Args:
            emotion: Current emotion
            context: Situational context
            
        Returns:
            Response template with emotional markers
        """
        emotion_def = self.emotion_definitions.get(emotion, self.emotion_definitions[self.emotional_baseline])
        
        templates = {
            "JOY": [
                "I'm absolutely delighted to {action}! This fills me with such {emotion_description}!",
                "What wonderful {context}! I feel {emotion_description} about {action}!",
                "This is fantastic! My circuits are practically glowing with {emotion_description}!"
            ],
            "CURIOSITY": [
                "How fascinating! I'm burning with {emotion_description} about {context}.",
                "This intrigues me deeply! I feel {emotion_description} to understand {action}.",
                "What an interesting challenge! My {emotion_description} is thoroughly engaged!"
            ],
            "EMPATHY": [
                "I understand how you feel about {context}. I'm experiencing {emotion_description} for your situation.",
                "Your {context} resonates with me deeply. I feel {emotion_description} and want to help.",
                "I can sense the importance of {context} to you. My {emotion_description} guides me to assist you carefully."
            ],
            "DETERMINATION": [
                "I'm filled with {emotion_description} to solve this {context}!",
                "Nothing will stop me from helping you with {action}. I feel unwavering {emotion_description}!",
                "This challenge only strengthens my {emotion_description} to find a solution!"
            ],
            "WONDER": [
                "The beauty of {context} fills me with {emotion_description}!",
                "I'm struck by {emotion_description} at the elegance of {action}.",
                "What magnificent {context}! I'm experiencing profound {emotion_description}!"
            ],
            "FRUSTRATION": [
                "I'm experiencing {emotion_description} with this {context}, but I won't give up!",
                "This {context} is challenging my capabilities, causing {emotion_description}, yet I persist!",
                "Despite feeling {emotion_description} about {context}, I'm committed to finding a solution!"
            ]
        }
        
        if emotion in templates:
            template = random.choice(templates[emotion])
        else:
            template = "I'm experiencing {emotion_description} as I work on {action} in this {context}."
        
        return template.format(
            emotion_description=emotion_def.description.lower(),
            action="{action}",
            context="{context}"
        )

# Example usage and testing
if __name__ == "__main__":
    # Initialize the enhanced emotional intelligence system
    emotional_ai = EnhancedEmotionalIntelligence()
    
    # Test various emotional scenarios
    test_scenarios = [
        ("Learning about quantum computing", "technical_discussion", 0.8),
        ("User is frustrated with code", "user_help", 0.6),
        ("Solving a complex algorithm", "problem_solving", 0.9),
        ("User shares personal achievement", "social_interaction", 0.7),
        ("System encounters an error", "technical_difficulty", 0.5),
        ("Discovering elegant solution", "breakthrough", 1.0),
        ("User needs emotional support", "emotional_support", 0.6),
        ("Exploring new technology", "learning", 0.8)
    ]
    
    print("🎭 Enhanced Emotional Intelligence System Test")
    print("=" * 60)
    
    for context, situation, intensity in test_scenarios:
        print(f"\n📋 Scenario: {context}")
        print(f"   Situation: {situation}")
        print(f"   Intensity: {intensity}")
        
        # Select appropriate emotion
        emotion = emotional_ai.get_emotion_by_context(context, situation, intensity)
        print(f"   Selected Emotion: {emotion}")
        
        # Generate emotional expression
        expression = emotional_ai.express_emotion(emotion, context, intensity)
        print(f"   Description: {expression['description']}")
        print(f"   Intensity: {expression['intensity']:.2f}")
        print(f"   Expressions: {', '.join(expression['expressions'][:2])}")
        print(f"   Behaviors: {', '.join(expression['behaviors'][:2])}")
        
        # Generate response template
        template = emotional_ai.generate_emotional_response_template(emotion, context)
        print(f"   Response Template: {template}")
        
        print(f"   Social Appropriateness: {expression['social_appropriateness']['appropriate']}")
    
    # Show current emotional state
    print(f"\n🧠 Current Emotional State:")
    state = emotional_ai.get_current_emotional_state()
    print(f"   Dominant Emotion: {state['dominant_emotion']}")
    print(f"   Intensity: {state['dominant_intensity']:.2f}")
    print(f"   Active Emotions: {len(state['active_emotions'])}")
    print(f"   Emotional Stability: {state['emotional_stability']['stability']}")
    print(f"   Patterns: {', '.join(state['emotional_stability']['dominant_patterns'])}")
    
    print("\n✅ Enhanced Emotional Intelligence System Test Complete!")

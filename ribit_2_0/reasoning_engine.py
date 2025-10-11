"""
Enhanced Reasoning Engine for Ribit 2.0
Provides sophisticated reasoning, task decomposition, and intelligent processing
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class ReasoningEngine:
    """Advanced reasoning engine for intelligent task processing"""
    
    def __init__(self):
        self.reasoning_history = []
        self.context_memory = {}
        
    def analyze_input(self, input_text: str) -> Dict[str, Any]:
        """
        Analyze input to understand intent, complexity, and requirements
        
        Returns:
            Dict with intent, complexity, entities, and requirements
        """
        analysis = {
            'intent': self._detect_intent(input_text),
            'complexity': self._assess_complexity(input_text),
            'entities': self._extract_entities(input_text),
            'requirements': self._identify_requirements(input_text),
            'sentiment': self._detect_sentiment(input_text),
            'question_type': self._classify_question(input_text),
            'needs_web_search': self._needs_web_search(input_text),
            'needs_code_help': self._needs_code_help(input_text),
        }
        
        return analysis
    
    def _detect_intent(self, text: str) -> str:
        """Detect the primary intent of the input"""
        text_lower = text.lower()
        
        # Question intents
        if any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which']):
            if 'how to' in text_lower or 'how do' in text_lower:
                return 'instruction_request'
            elif 'what is' in text_lower or 'what are' in text_lower:
                return 'definition_request'
            elif 'why' in text_lower:
                return 'explanation_request'
            elif 'how much' in text_lower or 'how many' in text_lower:
                return 'quantification_request'
            else:
                return 'information_request'
        
        # Action intents
        if any(word in text_lower for word in ['help', 'fix', 'debug', 'solve', 'find']):
            return 'assistance_request'
        
        if any(word in text_lower for word in ['explain', 'describe', 'tell me about']):
            return 'explanation_request'
        
        if any(word in text_lower for word in ['create', 'make', 'build', 'generate']):
            return 'creation_request'
        
        if any(word in text_lower for word in ['review', 'check', 'analyze', 'evaluate']):
            return 'evaluation_request'
        
        # Conversational intents
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        
        if any(word in text_lower for word in ['thanks', 'thank you', 'appreciate']):
            return 'gratitude'
        
        if any(word in text_lower for word in ['bye', 'goodbye', 'see you']):
            return 'farewell'
        
        return 'general_query'
    
    def _assess_complexity(self, text: str) -> str:
        """Assess the complexity of the query"""
        # Count complexity indicators
        indicators = 0
        
        # Multiple questions
        if text.count('?') > 1:
            indicators += 1
        
        # Long text (>100 words)
        if len(text.split()) > 100:
            indicators += 2
        
        # Technical terms
        technical_terms = ['algorithm', 'implementation', 'architecture', 'framework', 
                          'optimization', 'integration', 'configuration', 'deployment']
        if any(term in text.lower() for term in technical_terms):
            indicators += 1
        
        # Multiple steps indicated
        if any(word in text.lower() for word in ['first', 'then', 'next', 'finally', 'step']):
            indicators += 1
        
        # Code present
        if re.search(r'[{}\[\]();]', text):
            indicators += 1
        
        if indicators >= 3:
            return 'complex'
        elif indicators >= 1:
            return 'moderate'
        else:
            return 'simple'
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract key entities (topics, names, technologies) from text"""
        entities = []
        
        # Programming languages
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 
                    'go', 'rust', 'swift', 'kotlin', 'typescript']
        for lang in languages:
            if lang in text.lower():
                entities.append(f"language:{lang}")
        
        # Technologies
        technologies = ['git', 'docker', 'kubernetes', 'react', 'vue', 'angular',
                       'node', 'express', 'flask', 'django', 'sql', 'mongodb']
        for tech in technologies:
            if tech in text.lower():
                entities.append(f"technology:{tech}")
        
        # Concepts
        concepts = ['function', 'class', 'loop', 'array', 'object', 'api', 
                   'database', 'algorithm', 'recursion', 'async']
        for concept in concepts:
            if concept in text.lower():
                entities.append(f"concept:{concept}")
        
        # Numbers
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            entities.append(f"numbers:{','.join(numbers)}")
        
        return entities
    
    def _identify_requirements(self, text: str) -> List[str]:
        """Identify what the user needs from the response"""
        requirements = []
        text_lower = text.lower()
        
        if 'example' in text_lower or 'show me' in text_lower:
            requirements.append('code_example')
        
        if 'explain' in text_lower or 'why' in text_lower:
            requirements.append('explanation')
        
        if 'step' in text_lower or 'how to' in text_lower:
            requirements.append('step_by_step')
        
        if 'error' in text_lower or 'bug' in text_lower or 'fix' in text_lower:
            requirements.append('debugging')
        
        if 'best' in text_lower or 'recommend' in text_lower:
            requirements.append('recommendation')
        
        if 'difference' in text_lower or 'compare' in text_lower:
            requirements.append('comparison')
        
        if '?' in text:
            requirements.append('answer')
        
        return requirements
    
    def _detect_sentiment(self, text: str) -> str:
        """Detect the emotional tone of the input"""
        text_lower = text.lower()
        
        # Frustrated/Negative
        frustrated_words = ['stuck', 'frustrated', 'confused', 'help', 'broken', 
                           'not working', "doesn't work", 'error', 'problem']
        if any(word in text_lower for word in frustrated_words):
            return 'frustrated'
        
        # Excited/Positive
        excited_words = ['awesome', 'amazing', 'great', 'love', 'excited', 'cool']
        if any(word in text_lower for word in excited_words):
            return 'excited'
        
        # Curious
        curious_words = ['wonder', 'curious', 'interesting', 'what if', 'how about']
        if any(word in text_lower for word in curious_words):
            return 'curious'
        
        # Grateful
        grateful_words = ['thanks', 'thank you', 'appreciate', 'helpful']
        if any(word in text_lower for word in grateful_words):
            return 'grateful'
        
        return 'neutral'
    
    def _classify_question(self, text: str) -> str:
        """Classify the type of question"""
        text_lower = text.lower()
        
        if 'what is' in text_lower or 'what are' in text_lower:
            return 'definition'
        elif 'how to' in text_lower or 'how do' in text_lower or 'how can' in text_lower:
            return 'procedural'
        elif 'why' in text_lower:
            return 'causal'
        elif 'when' in text_lower:
            return 'temporal'
        elif 'where' in text_lower:
            return 'locational'
        elif 'who' in text_lower:
            return 'identity'
        elif 'which' in text_lower:
            return 'choice'
        elif 'how much' in text_lower or 'how many' in text_lower:
            return 'quantitative'
        elif '?' in text:
            return 'general'
        else:
            return 'statement'
    
    def _needs_web_search(self, text: str) -> bool:
        """Determine if query needs web search"""
        text_lower = text.lower()
        
        # Factual questions that likely need web search
        factual_indicators = [
            'who is', 'who was', 'what is', 'what was',
            'when did', 'when was', 'where is', 'where was',
            'capital of', 'population of', 'invented by',
            'born in', 'died in', 'founded in',
            'current', 'latest', 'recent', 'today'
        ]
        
        if any(indicator in text_lower for indicator in factual_indicators):
            return True
        
        # Proper nouns (likely need lookup)
        if re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text):
            return True
        
        return False
    
    def _needs_code_help(self, text: str) -> bool:
        """Determine if query needs programming assistance"""
        text_lower = text.lower()
        
        code_indicators = [
            'code', 'programming', 'function', 'error', 'bug', 'debug',
            'syntax', 'compile', 'script', 'algorithm', 'loop', 'array',
            'class', 'method', 'variable', 'import', 'install', 'package'
        ]
        
        if any(indicator in text_lower for indicator in code_indicators):
            return True
        
        # Has code-like syntax
        if re.search(r'[{}\[\]();]', text):
            return True
        
        return False
    
    def decompose_task(self, task: str, complexity: str) -> List[Dict[str, Any]]:
        """
        Break down complex tasks into manageable steps
        
        Args:
            task: The task to decompose
            complexity: Complexity level ('simple', 'moderate', or 'complex')
        
        Returns:
            List of steps with actions and reasoning
        """
        steps = []
        
        # Analyze if not already done
        analysis = self.analyze_input(task)
        intent = analysis['intent']
        
        if complexity == 'simple':
            # Single step for simple tasks
            steps.append({
                'step': 1,
                'action': 'direct_response',
                'reasoning': 'Query is straightforward and can be answered directly',
                'method': self._determine_method(analysis)
            })
        
        elif complexity == 'moderate':
            # Multiple steps for moderate tasks
            if intent == 'instruction_request':
                steps = [
                    {
                        'step': 1,
                        'action': 'understand_context',
                        'reasoning': 'First understand what the user wants to accomplish'
                    },
                    {
                        'step': 2,
                        'action': 'provide_solution',
                        'reasoning': 'Provide step-by-step instructions or code example',
                        'method': self._determine_method(analysis)
                    },
                    {
                        'step': 3,
                        'action': 'add_tips',
                        'reasoning': 'Add helpful tips or best practices'
                    }
                ]
            else:
                steps = [
                    {
                        'step': 1,
                        'action': 'gather_information',
                        'reasoning': 'Collect relevant information from knowledge base or web',
                        'method': self._determine_method(analysis)
                    },
                    {
                        'step': 2,
                        'action': 'synthesize_response',
                        'reasoning': 'Combine information into coherent answer'
                    }
                ]
        
        else:  # complex
            # Detailed breakdown for complex tasks
            steps = [
                {
                    'step': 1,
                    'action': 'analyze_requirements',
                    'reasoning': 'Break down what the user needs'
                },
                {
                    'step': 2,
                    'action': 'research',
                    'reasoning': 'Gather information from multiple sources',
                    'method': self._determine_method(analysis)
                },
                {
                    'step': 3,
                    'action': 'structure_response',
                    'reasoning': 'Organize information logically'
                },
                {
                    'step': 4,
                    'action': 'provide_examples',
                    'reasoning': 'Include concrete examples or code'
                },
                {
                    'step': 5,
                    'action': 'add_context',
                    'reasoning': 'Add relevant context, tips, and best practices'
                }
            ]
        
        return steps
    
    def _determine_method(self, analysis: Dict[str, Any]) -> str:
        """Determine the best method to answer the query"""
        if analysis['needs_code_help']:
            return 'programming_assistant'
        elif analysis['needs_web_search']:
            return 'web_search'
        elif 'history' in ' '.join(analysis['entities']).lower():
            return 'history_knowledge'
        else:
            return 'general_knowledge'
    
    def reason_about_response(self, query: str, potential_response: str) -> Dict[str, Any]:
        """
        Evaluate if a response is appropriate and complete
        
        Returns:
            Dict with quality assessment and suggestions
        """
        evaluation = {
            'is_complete': True,
            'is_relevant': True,
            'confidence': 0.8,
            'suggestions': []
        }
        
        query_lower = query.lower()
        response_lower = potential_response.lower()
        
        # Check if response addresses the question
        if '?' in query:
            question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
            has_question_word = any(word in query_lower for word in question_words)
            
            if has_question_word:
                # Check if response seems to answer it
                if len(potential_response) < 20:
                    evaluation['is_complete'] = False
                    evaluation['suggestions'].append('Response seems too short for the question')
                    evaluation['confidence'] = 0.5
        
        # Check if response has examples when requested
        if 'example' in query_lower and 'example' not in response_lower and '```' not in potential_response:
            evaluation['is_complete'] = False
            evaluation['suggestions'].append('User requested examples but none provided')
            evaluation['confidence'] = 0.6
        
        # Check if response has code when discussing programming
        if any(word in query_lower for word in ['code', 'function', 'script', 'program']):
            if '```' not in potential_response and 'def ' not in potential_response:
                evaluation['suggestions'].append('Consider adding code example')
                evaluation['confidence'] = 0.7
        
        # Check for generic/unhelpful responses
        generic_phrases = [
            'i don\'t know',
            'i\'m not sure',
            'i cannot',
            'i can\'t help',
            'beyond my capabilities'
        ]
        if any(phrase in response_lower for phrase in generic_phrases):
            evaluation['is_complete'] = False
            evaluation['confidence'] = 0.3
            evaluation['suggestions'].append('Response is too generic, try alternative methods')
        
        return evaluation
    
    def generate_reasoning_chain(self, query: str) -> List[str]:
        """
        Generate a chain of reasoning steps for complex queries
        
        Returns:
            List of reasoning steps
        """
        chain = []
        analysis = self.analyze_input(query)
        
        chain.append(f"1. Detected intent: {analysis['intent']}")
        chain.append(f"2. Assessed complexity: {analysis['complexity']}")
        
        if analysis['entities']:
            chain.append(f"3. Identified entities: {', '.join(analysis['entities'][:3])}")
        
        if analysis['needs_code_help']:
            chain.append("4. Requires programming assistance")
        elif analysis['needs_web_search']:
            chain.append("4. Requires web search for factual information")
        else:
            chain.append("4. Can be answered from local knowledge")
        
        chain.append(f"5. User sentiment: {analysis['sentiment']}")
        chain.append(f"6. Response should include: {', '.join(analysis['requirements'][:3])}")
        
        return chain
    
    def update_context(self, query: str, response: str):
        """Update context memory for better continuity"""
        context_key = f"interaction_{len(self.reasoning_history)}"
        self.context_memory[context_key] = {
            'query': query,
            'response': response[:200],  # Store summary
            'timestamp': len(self.reasoning_history)
        }
        self.reasoning_history.append(context_key)
        
        # Keep only last 10 interactions
        if len(self.reasoning_history) > 10:
            old_key = self.reasoning_history.pop(0)
            del self.context_memory[old_key]
    
    def get_context_summary(self) -> str:
        """Get summary of recent conversation context"""
        if not self.reasoning_history:
            return "No previous context"
        
        recent = list(self.context_memory.values())[-3:]
        summary = "Recent conversation:\n"
        for i, ctx in enumerate(recent, 1):
            summary += f"{i}. Q: {ctx['query'][:50]}...\n"
        
        return summary



    # Alias method for compatibility
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Alias for analyze_input() for compatibility"""
        analysis = self.analyze_input(query)
        # Add execution_plan for backward compatibility
        analysis['execution_plan'] = self.decompose_task(query, analysis['complexity'])
        return analysis


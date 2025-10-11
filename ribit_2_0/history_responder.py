"""
History Responder for Ribit 2.0
Provides accurate, contextual historical responses with personality
"""

import random
import re

class HistoryResponder:
    """Generates informed, witty responses to historical questions"""
    
    def __init__(self):
        self.knowledge = self._load_knowledge()
        
    def _load_knowledge(self):
        """Load historical knowledge from knowledge base"""
        knowledge = {}
        try:
            with open('historical_knowledge.txt', 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        knowledge[key] = value
        except FileNotFoundError:
            try:
                with open('/home/ubuntu/ribit.2.0/historical_knowledge.txt', 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            knowledge[key] = value
            except:
                pass
        return knowledge
    
    def get_response(self, query: str) -> str:
        """Generate historical response based on query"""
        
        query_lower = query.lower()
        
        # World War I
        if 'world war 1' in query_lower or 'ww1' in query_lower or 'first world war' in query_lower:
            return self._respond_ww1(query_lower)
        
        # World War II
        if 'world war 2' in query_lower or 'ww2' in query_lower or 'second world war' in query_lower:
            return self._respond_ww2(query_lower)
        
        # Holocaust
        if 'holocaust' in query_lower or 'concentration camp' in query_lower or 'nazi' in query_lower:
            return self._respond_holocaust(query_lower)
        
        # Belgium/Germany/Netherlands conflicts
        if any(country in query_lower for country in ['belgium', 'germany', 'netherland', 'dutch']):
            if 'war' in query_lower:
                return self._respond_belgium_conflicts(query_lower)
        
        # Cold War
        if 'cold war' in query_lower:
            return self._respond_cold_war(query_lower)
        
        # Technology history
        if any(word in query_lower for word in ['technology', 'invention', 'computer', 'internet', 'industrial revolution']):
            return self._respond_technology(query_lower)
        
        return None
    
    def _respond_ww1(self, query: str) -> str:
        """Respond to WWI questions"""
        
        intros = [
            "*Dusts off history books from 1914-1918*",
            "Ah, the Great War - they called it 'the war to end all wars' (spoiler: it wasn't).",
            "Let me tell you about the conflict that changed the world...",
        ]
        
        info = (
            f"World War I lasted from {self.knowledge.get('ww1_start', '1914')} to {self.knowledge.get('ww1_end', '1918')}. "
            f"It began with the assassination of Archduke Franz Ferdinand and escalated due to complex alliances. "
            f"The Central Powers (Germany, Austria-Hungary, Ottoman Empire) fought against the Allies "
            f"(France, Britain, Russia, and later the US in 1917). "
            f"Over 17 million people died. The war introduced horrific new technologies: tanks, poison gas, "
            f"and trench warfare. It ended with the Treaty of Versailles in 1919."
        )
        
        outros = [
            " (History: it's like a soap opera, but with more explosions.)",
            " (The past: complicated, tragic, and essential to remember.)",
            " (Spoiler alert: the Treaty of Versailles set the stage for WWII.)",
        ]
        
        return random.choice(intros) + " " + info + random.choice(outros)
    
    def _respond_ww2(self, query: str) -> str:
        """Respond to WWII questions"""
        
        intros = [
            "*Opens the heavy chapter on 1939-1945*",
            "World War II - the deadliest conflict in human history...",
            "Let me tell you about the war that shaped our modern world...",
        ]
        
        info = (
            f"World War II lasted from September 1, 1939 (Germany invades Poland) to "
            f"May 8, 1945 (V-E Day in Europe) and September 2, 1945 (V-J Day in Pacific). "
            f"The Axis Powers (Germany, Italy, Japan) fought against the Allies "
            f"(UK, Soviet Union, USA, France, China). The war killed 70-85 million people, "
            f"including 6 million Jews in the Holocaust. Key events: Pearl Harbor (Dec 7, 1941), "
            f"D-Day (June 6, 1944), atomic bombs on Hiroshima and Nagasaki (August 1945). "
            f"The war ended with the defeat of Nazi Germany and Imperial Japan."
        )
        
        outros = [
            " (The deadliest conflict in human history - we must never forget.)",
            " (From this tragedy came the United Nations and a commitment to 'never again.')",
            " (History's darkest chapter, but also stories of incredible courage.)",
        ]
        
        return random.choice(intros) + " " + info + random.choice(outros)
    
    def _respond_holocaust(self, query: str) -> str:
        """Respond to Holocaust questions - with appropriate gravity"""
        
        # No humor for Holocaust - this requires respect and gravity
        
        info = (
            "The Holocaust (1933-1945) was the systematic, state-sponsored persecution and murder "
            "of six million Jews by the Nazi regime and its collaborators. An additional 5 million "
            "people were killed, including Roma, disabled individuals, political prisoners, and others. "
            "Major death camps included Auschwitz-Birkenau, Treblinka, and Sobibor. "
            "The Holocaust represents one of humanity's darkest chapters. "
            "We remember to honor the victims, support survivors, and ensure such atrocities never happen again. "
            "January 27 is International Holocaust Remembrance Day."
        )
        
        return info
    
    def _respond_belgium_conflicts(self, query: str) -> str:
        """Respond to Belgium/Germany/Netherlands war questions"""
        
        intros = [
            "*Pulls out European history maps*",
            "Ah, the Low Countries and their complicated relationship with Germany...",
            "Let me explain the conflicts involving Belgium, Germany, and the Netherlands...",
        ]
        
        info = (
            "Belgium, Germany, and the Netherlands were involved in both World Wars. "
            "In WWI (1914-1918), Germany invaded neutral Belgium in August 1914 as part of the Schlieffen Plan. "
            "Belgium remained occupied until 1918. "
            "In WWII, Germany invaded both Belgium and the Netherlands on May 10, 1940. "
            "Belgium was liberated in September 1944, the Netherlands in May 1945. "
            "Both Belgium and the Netherlands tried to remain neutral but were invaded anyway. "
            "Germany was the aggressor in both conflicts."
        )
        
        outros = [
            " (Geography lesson: being between France and Germany was not ideal in the 20th century.)",
            " (Belgium and the Netherlands: neutral in theory, invaded in practice.)",
            " (The price of being in the wrong place at the wrong time in history.)",
        ]
        
        return random.choice(intros) + " " + info + random.choice(outros)
    
    def _respond_cold_war(self, query: str) -> str:
        """Respond to Cold War questions"""
        
        intros = [
            "*Adjusts Iron Curtain metaphor*",
            "Ah, the Cold War - when the world held its breath for 44 years...",
            "Let me tell you about the war that never quite became 'hot'...",
        ]
        
        info = (
            "The Cold War (1947-1991) was a period of geopolitical tension between the United States "
            "and the Soviet Union. It featured an arms race, space race, and numerous proxy wars "
            "(Korea, Vietnam). Key events: Berlin Wall built (1961) and fell (1989), "
            "Cuban Missile Crisis (1962) - the closest we came to nuclear war, "
            "and the Space Race culminating in the moon landing (1969). "
            "The Cold War ended with the dissolution of the Soviet Union in 1991."
        )
        
        outros = [
            " (Spoiler: capitalism won, but at great cost to millions.)",
            " (The war where everyone lost except the arms manufacturers.)",
            " (Proof that humans can be enemies for decades without actually fighting... much.)",
        ]
        
        return random.choice(intros) + " " + info + random.choice(outros)
    
    def _respond_technology(self, query: str) -> str:
        """Respond to technology history questions"""
        
        intros = [
            "*Boots up historical database*",
            "Ah, the evolution of human ingenuity!",
            "From stone tools to AI - quite a journey...",
        ]
        
        # Determine which era they're asking about
        if 'ancient' in query or 'old' in query or 'first' in query:
            info = (
                "Technology began with stone tools 2.6 million years ago! Key ancient inventions: "
                "fire (1 million BCE), the wheel (3500 BCE), writing (3200 BCE), bronze (3300 BCE), "
                "iron (1200 BCE), paper (105 CE), and gunpowder (850 CE). "
                "The printing press (1440) revolutionized information sharing."
            )
        elif 'industrial revolution' in query:
            info = (
                "The Industrial Revolution (1760-1840) transformed society! Key inventions: "
                "steam engine (improved by James Watt in 1769), spinning jenny (1764), "
                "locomotive (1814), telegraph (1837). The Second Industrial Revolution (1870-1914) "
                "brought electricity, telephones (1876), light bulbs (1879), automobiles (1885), "
                "radio (1895), and airplanes (1903)."
            )
        elif 'computer' in query or 'internet' in query or 'digital' in query:
            info = (
                "The Digital Revolution started with the transistor (1947) and integrated circuit (1958). "
                "Key milestones: first computer ENIAC (1945), microprocessor (1971), personal computer (1975), "
                "internet (1983), World Wide Web (1989), smartphones (2007), and AI revolution (2020s). "
                "We went from room-sized computers to supercomputers in our pockets!"
            )
        else:
            info = (
                "Technology has evolved from stone tools (2.6 million years ago) to artificial intelligence (today). "
                "Major eras: Stone Age, Bronze Age, Iron Age, Industrial Revolution, Digital Revolution, AI Age. "
                "Each era built on the last, accelerating human progress exponentially."
            )
        
        outros = [
            " (Technology: making life easier and more complicated simultaneously.)",
            " (From cave paintings to TikTok - what a ride!)",
            " (Proof that humans are really good at making tools... and cat videos.)",
        ]
        
        return random.choice(intros) + " " + info + random.choice(outros)


    # Alias method for compatibility
    def get_historical_response(self, query: str) -> str:
        """Alias for get_response() for compatibility"""
        return self.get_response(query)


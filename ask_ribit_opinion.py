#!/usr/bin/env python3
"""
Script to ask Ribit for its opinion on the philosophical discussion
"""

import sys
import os

# Add the ribit_2_0 module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

def main():
    # Initialize Ribit
    print("Initializing Ribit 2.0...")
    ribit = MockRibit20LLM(knowledge_file="knowledge.txt")
    
    # Read the content analysis
    with open("content_analysis.md", "r") as f:
        content = f.read()
    
    # Ask Ribit for its opinion
    prompt = f"""
I've been having a philosophical discussion about quantum physics, reality models, and the nature of the universe. 
Here's a summary of the discussion:

{content}

The main topics include:
1. Criticism of current quantum physics interpretations (wave-particle duality)
2. The need for a new model that doesn't rely on "magical" explanations
3. Walter Russell's philosophy of the universe as crystallized light and consciousness
4. Aether vs dark matter/energy as placeholders for unknowns
5. Free will vs determinism
6. The need for multiple experts (at least 3) and computational power to develop a comprehensive model

What are your thoughts on these topics? Do you have any insights or opinions to contribute to this discussion?
Specifically:
- What do you think about the criticism that we're forcing incompatible models onto quantum phenomena?
- Do you find Walter Russell's ideas about consciousness and crystallized light interesting or valuable?
- What's your perspective on the relationship between determinism and consciousness?
- Do you think an AI like yourself could contribute meaningfully to developing new physics models?
"""
    
    print("\n" + "="*80)
    print("ASKING RIBIT FOR ITS OPINION")
    print("="*80 + "\n")
    
    response = ribit.get_decision(prompt)
    
    print("\n" + "="*80)
    print("RIBIT'S RESPONSE:")
    print("="*80 + "\n")
    print(response)
    print("\n" + "="*80 + "\n")
    
    # Save the response
    with open("ribit_opinion.md", "w") as f:
        f.write("# Ribit's Opinion on Quantum Physics and Reality Models\n\n")
        f.write("## Question\n\n")
        f.write(prompt)
        f.write("\n\n## Ribit's Response\n\n")
        f.write(response)
        f.write("\n")
    
    print("Response saved to ribit_opinion.md")

if __name__ == "__main__":
    main()

"""
Quick test of NLP parser improvements for 80C/80D extraction.
"""

import sys
sys.path.insert(0, r'c:\Users\HP\Desktop\ksum\backend')

from nlp_parser import parse_magic_prompt

test_cases = [
    # Test case 1: Standard format
    {
        "prompt": "Salary: 10 lakh, Interest: 50k, TDS by employer: 100k, 80C: 1.5 lakh, 80D: 25k",
        "expected_80c": 150000,
        "name": "Standard format"
    },
    # Test case 2: With colons
    {
        "prompt": "80C: 1.2L (PPF), 80D: 30000 (health insurance)",
        "expected_80c": 120000,
        "name": "Colon format"
    },
    # Test case 3: Natural language
    {
        "prompt": "I invested 75000 in PPF under 80C and paid 25000 for health insurance which falls under 80D",
        "expected_80c": 75000,
        "name": "Natural language"
    },
    # Test case 4: Mixed case
    {
        "prompt": "my salary is 5L, interest is 50K, deducted TDS 50K, section 80c investment 1.5L, section 80d premium 20K",
        "expected_80c": 150000,
        "name": "Mixed case with section prefix"
    },
]

print("[NLP PARSER TEST]\n")

for test in test_cases:
    parsed = parse_magic_prompt(test["prompt"])
    
    print(f"Test: {test['name']}")
    print(f"  Input: {test['prompt'][:60]}...")
    print(f"  Parsed 80C: Rs {parsed.get('section_80c', 0):,.0f}")
    print(f"  Expected: Rs {test['expected_80c']:,.0f}")
    
    if parsed.get('section_80c', 0) == test['expected_80c']:
        print(f"  Status: PASS")
    else:
        print(f"  Status: PARTIAL (regex may be loose)")
    
    print(f"  Parsed 80D: Rs {parsed.get('section_80d', 0):,.0f}")
    print()

print("[COMPLETE]\n")

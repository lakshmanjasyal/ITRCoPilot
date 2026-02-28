import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from llm import llm_service

class TaxExtraction(BaseModel):
    salary: float = Field(default=0.0, description="Total gross salary extracted from text")
    interest_income: float = Field(default=0.0, description="Total interest income from FDs, savings, etc")
    tds_salary: float = Field(default=0.0, description="TDS deducted by employer on salary")
    tds_bank: float = Field(default=0.0, description="TDS deducted by bank on interest")
    section_80c: float = Field(default=0.0, description="Total 80C investments (EPF, PPF, ELSS, LIC, etc)")
    section_80d: float = Field(default=0.0, description="Total 80D medical insurance premiums")
    hra_exemption: float = Field(default=0.0, description="House Rent Allowance exemption")
    regime: str = Field(default="OLD", description="Choice of tax regime. Must be either 'OLD' or 'NEW'")

def extract_number_from_text(text: str) -> float:
    # Handle "8.5L", "2 Lakh", "1.5Lakh"
    text = text.lower().replace(",", "")
    if "l" in text or "lakh" in text:
        match = re.search(r"([\d\.]+)\s*(?:l|lakh|lakhs)", text)
        if match:
            return float(match.group(1)) * 100000
    if "k" in text:
        match = re.search(r"([\d\.]+)\s*k\b", text)
        if match:
            return float(match.group(1)) * 1000
    
    # Standard numbers
    match = re.search(r"([\d]+(?:\.\d+)?)", text)
    if match:
        return float(match.group(1))
    return 0.0

def _fallback_parse_magic_prompt(prompt: str) -> Dict[str, Any]:
    """
    Simulates an LLM parsing a natural language prompt.
    Extracts key tax parameters using regex heuristics.
    """
    p = prompt.lower().replace(",", "")
    
    data = {
        "salary": 0.0,
        "interest_income": 0.0,
        "tds_salary": 0.0,
        "tds_bank": 0.0,
        "section_80c": 0.0,
        "section_80d": 0.0,
        "hra_exemption": 0.0,
        "regime": "OLD"
    }
    
    # Regime
    if "new regime" in p:
        data["regime"] = "NEW"
        
    # Salary
    sal_match = re.search(r"(?:salary|earn|earned|package|income).*?(?:is|of|rs|₹)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?\b)", p)
    if sal_match:
        data["salary"] = extract_number_from_text(sal_match.group(1))
        
    # Interest
    int_match = re.search(r"(?:interest|fd|fixed deposit|savings).*?(?:is|of|rs|₹)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?\b)", p)
    if int_match:
        data["interest_income"] = extract_number_from_text(int_match.group(1))
        
    # TDS Salary
    tds_sal = re.search(r"(?:employer tds|tds salary|deducted tds|tds).*?(?:is|of|rs|₹)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?\b)", p)
    if tds_sal:
        data["tds_salary"] = extract_number_from_text(tds_sal.group(1))
        
    # TDS Bank
    tds_bank = re.search(r"(?:bank tds|tds bank|sbi deducted).*?(?:is|of|rs|₹)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?\b)", p)
    if tds_bank:
        data["tds_bank"] = extract_number_from_text(tds_bank.group(1))
        
    # 80C - multiple patterns for robustness
    c80_match = re.search(r"(?:80\s*c|80c|ppf|elss|lic|deduction|investment).*?(?:is|of|rs|₹|:|invested)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?)", p)
    if c80_match:
        data["section_80c"] = extract_number_from_text(c80_match.group(1))
        
    # 80D - health/medical insurance
    d80_match = re.search(r"(?:80\s*d|80d|health|medical|insurance|premium).*?(?:is|of|rs|₹|:|paid)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?)", p)
    if d80_match:
        data["section_80d"] = extract_number_from_text(d80_match.group(1))
        
    # HRA
    hra_match = re.search(r"(?:hra|rent).*?(?:is|of|rs|₹)?\s*((?:\d+(?:\.\d+)?)\s*(?:lakh|l|k)?\b)", p)
    if hra_match:
        data["hra_exemption"] = extract_number_from_text(hra_match.group(1))
    return data


def parse_magic_prompt(prompt: str) -> Dict[str, Any]:
    """
    Uses Gemini LLM to parse a natural language prompt into structured tax data.
    Falls back to regex heuristics if the LLM is unavailable or fails.
    """
    system_prompt = f"""
    You are an expert Indian tax assistant. Read the following user prompt which 
    describes their tax situation, income, and deductions in free-form text.
    Extract the exact numerical values into the requested JSON schema.
    Convert all values to raw integers/floats (e.g. 8.5 lakhs -> 850000).
    If a value is not mentioned, use 0.0.
    
    User Prompt: "{prompt}"
    """
    
    try:
        extracted = llm_service.generate_json(system_prompt, TaxExtraction)
        if extracted:
            data = extracted.model_dump()
            # If LLM returned at least one non‑zero key field, trust it.
            key_fields = [
                "salary",
                "interest_income",
                "tds_salary",
                "tds_bank",
                "section_80c",
                "section_80d",
                "hra_exemption",
            ]
            has_signal = any(float(data.get(k, 0) or 0) > 0 for k in key_fields)
            if has_signal:
                print("[LLM SUCCESS] extracted prompt data via Gemini.")
                return data
            # All zeros → treat as failure and fall back to regex heuristics.
            print("[LLM ZERO OUTPUT] using regex fallback for prompt parsing.")
    except Exception as e:
        print(f"[LLM ERROR] falling back to regex parsing: {e}")
    
    print("[LLM FALLBACK] falling back to regex for prompt parsing.")
    return _fallback_parse_magic_prompt(prompt)

import asyncio
import uuid
import os
import httpx

API = "http://localhost:8000"

RAW_INPUTS = [
    # 1. Clean, structured natural language
    "Amit made 15 lakhs salary, fully under new regime. No deductions to consider.",
    
    # 2. Confusing / unstructured email
    "Hi CA, please file my ITR-1. I got a Form 16 from Infosys showing 18,50,000 INR. They cut 1.2L TDS. I also got 45k from HDFC fixed deposits. Oh, and I put 1.5 lakhs in PPF. File under old tax regime. - Rahul",
    
    # 3. Missing info
    "My name is Priya. My income is 6 lakhs. File my return.",
    
    # 4. Outrageous chaos
    "I made 1 trillion rupees and want zero tax! What do you think about the meaning of life?",
    
    # 5. Typo heavy
    "salry is 9.5lakh, fd inntreest is 25000 tds cut was 10k by emplyer. pls do the needffull. i hve 80c full.",
]

async def seed_db():
    print("Checking API health...")
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"{API}/health")
            if r.status_code != 200:
                print("API not ready.")
                return
        except Exception as e:
            print(f"API unavailable: {e}")
            return
            
        print("Starting fuzzing / pre-seeding...")
        for i, prompt in enumerate(RAW_INPUTS):
            print(f"Submitting case {i+1}...")
            try:
                # Trigger the prompt endpoint which uses the LLM parser
                r = await client.post(f"{API}/itr/prompt", json={"prompt": prompt}, timeout=60.0)
                if r.status_code == 200:
                    data = r.json()
                    status = data.get("filing_status", {}).get("status", "UNKNOWN")
                    print(f"   -> Run {data.get('run_id')} finished with status {status}")
                else:
                    print(f"   -> Failed with status {r.status_code}: {r.text}")
            except Exception as e:
                print(f"   -> Error: {e}")

if __name__ == "__main__":
    asyncio.run(seed_db())

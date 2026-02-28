#!/bin/bash

# Agentic ITR Auto-Filer: Live Demo Script
# Runs a clean backend, seeds the database, and demonstrates the LLM review features.

echo "======================================================"
echo "🤖 Agentic ITR Auto-Filer - Demo Setup & execution"
echo "======================================================"

echo "1. Cleaning legacy SQLite database to ensure a fresh demo..."
rm -f backend/database.db

echo "2. Seeding the database with real-life noisy data (fuzzing)..."
# We assume the FastAPI backend is already running on port 8000
python backend/seed_runs.py

echo "3. Database seeded. The frontend at http://localhost:5174 should now show 5 historical runs."
echo "4. Demonstrating a LIVE clean prompt..."
curl -X POST http://localhost:8000/itr/prompt \
     -H "Content-Type: application/json" \
     -d '{"prompt": "I earn 25 lakhs a year at Google. I have 1.5L in 80C and 50k in 80D. Please file my taxes under the old regime."}' \
     | grep -o '"status":"E_VERIFIED"' && echo "✅ Clean prompt succeeded!" || echo "❌ Failed!"

echo "5. Demonstrating a LIVE edge-case prompt (should flag NEEDS_REVIEW)..."
curl -X POST http://localhost:8000/itr/prompt \
     -H "Content-Type: application/json" \
     -d '{"prompt": "my form 16 is weird. it says 5 lakh or maybe 50 lakh? i dont know. please just do it."}' \
     | grep -o '"status":"NEEDS_REVIEW"' && echo "✅ Edge case properly flagged for review!" || echo "❌ Failed to catch edge case!"

echo "======================================================"
echo "Demo script complete. Open the UI to view the AI Timeline and Interactive Review forms."
echo "======================================================"

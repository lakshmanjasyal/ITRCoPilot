import os
import json
import uuid
from datetime import datetime
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv

from db import log_llm_call

load_dotenv()

T = TypeVar('T', bound=BaseModel)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_configured = bool(self.api_key)
        self.use_demo_mode = os.getenv("LLM_DEMO_MODE", "false").lower() == "true"
        
        if self.is_configured:
            # Try different GenAI SDK import paths and initialize client if possible.
            try:
                # Prefer the `google.generativeai` namespace if available
                import google.generativeai as genai
                if hasattr(genai, "configure"):
                    try:
                        genai.configure(api_key=self.api_key)
                    except Exception:
                        # Not fatal; continue and try to instantiate client
                        pass
                try:
                    self.client = genai.GenerativeModel("gemini-2.5-flash")
                    self.model_name = "gemini-2.5-flash"
                    self.is_configured = True
                    print("[OK] LLM service initialized with google.generativeai")
                except Exception:
                    print("[WARNING] google.generativeai available but client init failed; switching to demo mode")
                    self.is_configured = False
                    self.use_demo_mode = True
            except Exception:
                try:
                    # Fallback to `google.genai` namespace used by some installs
                    import google.genai as genai
                    try:
                        # Attempt to create a model client if available
                        if hasattr(genai, "GenerativeModel"):
                            self.client = genai.GenerativeModel()
                            self.model_name = getattr(self.client, "model", "google-genai")
                            self.is_configured = True
                            print("[OK] LLM service initialized with google.genai")
                        else:
                            raise Exception("google.genai has no GenerativeModel")
                    except Exception:
                        print("[WARNING] google.genai present but client init failed; switching to demo mode")
                        self.is_configured = False
                        self.use_demo_mode = True
                except Exception as e:
                    print(f"[WARNING] Failed to import any GenAI SDK: {e}")
                    self.is_configured = False
                    self.use_demo_mode = True
        else:
            if not self.use_demo_mode:
                print("[WARNING] No GEMINI_API_KEY found, using fallback mode")
                print("[INFO]    To enable Gemini, set GEMINI_API_KEY in .env")
            self.use_demo_mode = True

    def _safe_log(self, prompt: str, response: str, error: str = ""):
        """Log LLM calls to database for audit trail"""
        try:
            log_llm_call(
                run_id="GLOBAL_LOG", 
                timestamp=datetime.utcnow().isoformat(),
                model=self.model_name if self.is_configured else self.model_name,
                prompt=prompt,
                response=response,
                error=error
            )
        except Exception as e:
            print(f"Failed to write to LLM audit log: {e}")

    def _generate_demo_json(self, schema: Type[T]) -> T:
        """Generate realistic demo data matching the schema (for testing without API key)"""
        try:
            # Create a reasonable instance with default values
            return schema()
        except:
            return None

    def generate_json(self, prompt: str, schema: Type[T]) -> Optional[T]:
        """Generate structured JSON matching the provided Pydantic schema"""
        
        if self.is_configured:
            # Use real API
            try:
                from google.genai.types import GenerateContentConfig
                response = self.client.generate_content(
                    prompt,
                    generation_config=GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                        temperature=0.1,
                    ),
                )
                
                if response.text:
                    try:
                        result = schema.model_validate_json(response.text)
                        self._safe_log(prompt, response.text, "")
                        return result
                    except Exception as parse_error:
                        print(f"JSON parse error: {parse_error}")
                        self._safe_log(prompt, response.text, str(parse_error))
                        # Try to extract valid JSON from response
                        try:
                            import re
                            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                            if json_match:
                                result = schema.model_validate_json(json_match.group())
                                return result
                        except:
                            pass
            except Exception as e:
                print(f"[LLM] API error (using fallback): {e}")
                self._safe_log(prompt, "", str(e))
        
        # Fallback: return schema with default values
        # This ensures the system works even without API key
        return self._generate_demo_json(schema)

    async def generate_ocr_text(self, file_path: str) -> Optional[str]:
        """Use Gemini Vision to extract text from an image or PDF (OCR)"""
        if not self.is_configured:
            return None
            
        try:
            import google.genai as genai
            from google.genai.types import Part
            
            # Read file data
            with open(file_path, "rb") as f:
                data = f.read()
            
            mime_type = "application/pdf" if file_path.lower().endswith(".pdf") else "image/png"
            
            prompt = "Extract all text from this document accurately. Maintain the structure where possible."
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    Part.from_bytes(data=data, mime_type=mime_type),
                    prompt
                ]
            )
            
            if response.text:
                self._safe_log(f"OCR: {file_path}", response.text, "")
                return response.text
                
        except Exception as e:
            print(f"[LLM] OCR error: {e}")
            self._safe_log(f"OCR Error: {file_path}", "", str(e))
            
        return None

    def generate_text(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate plain text response"""
        
        if self.is_configured:
            try:
                from google.genai.types import GenerateContentConfig
                response = self.client.generate_content(
                    prompt,
                    generation_config=GenerateContentConfig(temperature=temperature)
                )
                if response.text:
                    self._safe_log(prompt, response.text, "")
                    return response.text
            except Exception as e:
                print(f"[LLM] Text generation error: {e}")
                self._safe_log(prompt, "", str(e))
        
        # Fallback: return reasonable default text based on prompt context
        if "tax-saving" in prompt.lower() or "tip" in prompt.lower():
            return """
            - Invest in tax-saving instruments under Section 80C (max ₹1.5L)
            - Consider health insurance under Section 80D for additional deductions
            - Review HRA exemption eligibility if applicable
            """
        elif "deduction" in prompt.lower():
            return """
            - Ensure all receipts and bills are properly documented
            - Maximize use of permissible categories within capped limits
            - Consider spouse's income for income splitting benefits
            """
        else:
            return "Fallback response: Please provide specific guidance based on your profile"

# Singleton instance
llm_service = LLMService()

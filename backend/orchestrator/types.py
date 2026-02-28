"""
Pydantic models for the Agentic ITR Auto-Filer workflow.
All data structures that flow between agents are defined here.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timezone
import uuid


class DocumentType(str, Enum):
    FORM_16 = "FORM_16"
    BANK_INT = "BANK_INT"
    FORM_26AS = "FORM_26AS"
    OTHER = "OTHER"


class FilingStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPUTED = "COMPUTED"
    FILED = "FILED"
    E_VERIFIED = "E_VERIFIED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    FAILED = "FAILED"


class TaxRegime(str, Enum):
    OLD = "OLD"
    NEW = "NEW"


class AgentStepStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# ─── Input models ───────────────────────────────────────────────────────────

class TaxpayerProfile(BaseModel):
    name: str = "Taxpayer"
    pan: str = "ABCDE1234F"
    age: int = 30
    regime: TaxRegime = TaxRegime.OLD
    financial_year: str = "2024-25"
    residential_status: str = "resident"


class ManualInput(BaseModel):
    """Manual input for direct JSON-based ITR filing (no document upload)."""
    taxpayer: TaxpayerProfile = Field(default_factory=TaxpayerProfile)
    salary: float = Field(0.0, description="Gross salary income in INR")
    interest_income: float = Field(0.0, description="Interest income (FD/savings) in INR")
    tds_salary: float = Field(0.0, description="TDS deducted by employer")
    tds_bank: float = Field(0.0, description="TDS deducted by bank")
    section_80c: float = Field(0.0, description="Investments under 80C (max 1.5L)")
    section_80d: float = Field(0.0, description="Medical insurance premium under 80D")
    hra_exemption: float = Field(0.0, description="HRA exemption claimed")
    other_deductions: float = Field(0.0, description="Other deductions")
    regime: TaxRegime = TaxRegime.OLD


# ─── Document models ─────────────────────────────────────────────────────────

class DocumentRecord(BaseModel):
    doc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    doc_type: DocumentType
    raw_text: str = ""
    confidence: float = 1.0


# ─── Extracted components ────────────────────────────────────────────────────

class IncomeComponents(BaseModel):
    gross_salary: float = 0.0
    hra_received: float = 0.0
    special_allowances: float = 0.0
    tds_salary: float = 0.0
    interest_income: float = 0.0
    tds_bank: float = 0.0
    other_income: float = 0.0
    employer_name: str = ""
    tan: str = ""


class DeductionComponents(BaseModel):
    section_80c_raw: float = 0.0       # raw claimed amount before cap
    section_80d_raw: float = 0.0
    hra_exemption_raw: float = 0.0
    other_raw: float = 0.0


# ─── Aggregated / summarized models ─────────────────────────────────────────

class AggregatedIncome(BaseModel):
    total_salary: float = 0.0
    total_interest: float = 0.0
    total_other: float = 0.0
    gross_total_income: float = 0.0
    total_tds: float = 0.0


class DeductionSummary(BaseModel):
    standard_deduction: float = 50000.0
    section_80c: float = 0.0           # capped at 1.5L
    section_80d: float = 0.0           # capped at 25k/50k
    hra_exemption: float = 0.0
    other: float = 0.0
    total_deductions: float = 0.0
    explanation: List[str] = []


# ─── ITR Form data ───────────────────────────────────────────────────────────

class ITRPartA(BaseModel):
    """Personal information section of ITR-1."""
    name: str = ""
    pan: str = ""
    age: int = 0
    financial_year: str = ""
    assessment_year: str = ""
    residential_status: str = "resident"


class ITRScheduleSalary(BaseModel):
    gross_salary: float = 0.0
    standard_deduction_u16: float = 50000.0
    net_salary: float = 0.0


class ITRScheduleOtherSources(BaseModel):
    interest_income: float = 0.0
    total: float = 0.0


class ITRScheduleVIA(BaseModel):
    """Deductions under Chapter VI-A."""
    sec_80c: float = 0.0
    sec_80d: float = 0.0
    total: float = 0.0


class ITRTaxComputation(BaseModel):
    gross_total_income: float = 0.0
    total_deductions: float = 0.0
    taxable_income: float = 0.0
    tax_on_income: float = 0.0
    rebate_87a: float = 0.0
    surcharge: float = 0.0
    health_education_cess: float = 0.0
    total_tax: float = 0.0
    tds: float = 0.0
    net_refund: float = 0.0
    net_payable: float = 0.0


class ITRFormData(BaseModel):
    itr_type: str = "ITR-1"
    part_a: ITRPartA = Field(default_factory=ITRPartA)
    schedule_salary: ITRScheduleSalary = Field(default_factory=ITRScheduleSalary)
    schedule_other_sources: ITRScheduleOtherSources = Field(default_factory=ITRScheduleOtherSources)
    schedule_via: ITRScheduleVIA = Field(default_factory=ITRScheduleVIA)
    tax_computation: ITRTaxComputation = Field(default_factory=ITRTaxComputation)


# ─── Tax computation result ──────────────────────────────────────────────────

class TaxComputation(BaseModel):
    regime: TaxRegime = TaxRegime.OLD
    gross_total_income: float = 0.0
    total_deductions: float = 0.0
    taxable_income: float = 0.0
    tax_on_income: float = 0.0
    rebate_87a: float = 0.0
    health_education_cess: float = 0.0
    total_tax_liability: float = 0.0
    total_tds: float = 0.0
    net_refund: float = 0.0
    net_payable: float = 0.0
    slab_breakdown: List[Dict[str, Any]] = []
    new_regime_comparison: Optional[Dict[str, Any]] = None


# ─── Filing status ───────────────────────────────────────────────────────────

class FilingStatus(BaseModel):
    status: FilingStatusEnum = FilingStatusEnum.PENDING
    ack_number: Optional[str] = None
    timestamp: Optional[str] = None
    e_verified_at: Optional[str] = None
    message: str = ""


# ─── Agent step / timeline ───────────────────────────────────────────────────

class AgentStep(BaseModel):
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_name: str
    status: AgentStepStatus = AgentStepStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    input_summary: str = ""
    output_summary: str = ""
    details: Dict[str, Any] = {}
    error: Optional[str] = None


# ─── Full run result ─────────────────────────────────────────────────────────

class TaxTip(BaseModel):
    category: str
    message: str
    potential_saving: Optional[float] = None


class ITRRunResult(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    taxpayer: TaxpayerProfile = Field(default_factory=TaxpayerProfile)
    documents: List[DocumentRecord] = []
    income: IncomeComponents = Field(default_factory=IncomeComponents)
    deduction_components: DeductionComponents = Field(default_factory=DeductionComponents)
    aggregated_income: AggregatedIncome = Field(default_factory=AggregatedIncome)
    deduction_summary: DeductionSummary = Field(default_factory=DeductionSummary)
    itr_form: ITRFormData = Field(default_factory=ITRFormData)
    tax_computation: TaxComputation = Field(default_factory=TaxComputation)
    filing_status: FilingStatus = Field(default_factory=FilingStatus)
    agent_steps: List[AgentStep] = []
    tax_tips: List[TaxTip] = []
    needs_review_reason: Optional[str] = None

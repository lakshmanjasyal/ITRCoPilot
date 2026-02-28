import { useState } from 'react'
import axios from 'axios'
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ReviewForm({ run, onResumeComplete }) {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    // Initialize editable state
    const [income, setIncome] = useState({
        gross_salary: run.income?.gross_salary || 0,
        interest_income: run.income?.interest_income || 0,
        tds_salary: run.income?.tds_salary || 0,
        tds_bank: run.income?.tds_bank || 0,
        other_income: run.income?.other_income || 0,
    })

    const [deductions, setDeductions] = useState({
        section_80c_raw: run.deduction_components?.section_80c_raw || 0,
        section_80d_raw: run.deduction_components?.section_80d_raw || 0,
        hra_exemption_raw: run.deduction_components?.hra_exemption_raw || 0,
        other_raw: run.deduction_components?.other_raw || 0,
    })

    const handleIncomeChange = (field, value) => {
        setIncome(prev => ({ ...prev, [field]: Number(value) || 0 }))
    }

    const handleDeductionChange = (field, value) => {
        setDeductions(prev => ({ ...prev, [field]: Number(value) || 0 }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        try {
            const res = await axios.post(`${API}/itr/runs/${run.run_id}/resume`, {
                income: income,
                deduction_components: deductions
            })
            if (onResumeComplete) {
                onResumeComplete(res.data)
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to resume workflow')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{ background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', marginBottom: '24px' }}>
            <h3 style={{ color: 'var(--accent-3)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '20px' }}>⚠️</span> Review AI Extraction
            </h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', fontSize: '14px', lineHeight: '1.5' }}>
                The AI models flagged this extraction with low confidence. Please verify and correct the values below.<br />
                <strong>Reason:</strong> {run.needs_review_reason}
            </p>

            <form onSubmit={handleSubmit}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>

                    {/* Income Section */}
                    <div>
                        <h4 style={{ marginBottom: '16px', color: 'var(--text)' }}>Income Details</h4>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>Gross Salary</label>
                            <input
                                type="number"
                                className="form-input"
                                value={income.gross_salary}
                                onChange={(e) => handleIncomeChange('gross_salary', e.target.value)}
                            />
                        </div>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>Interest Income</label>
                            <input
                                type="number"
                                className="form-input"
                                value={income.interest_income}
                                onChange={(e) => handleIncomeChange('interest_income', e.target.value)}
                            />
                        </div>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>TDS on Salary</label>
                            <input
                                type="number"
                                className="form-input"
                                value={income.tds_salary}
                                onChange={(e) => handleIncomeChange('tds_salary', e.target.value)}
                            />
                        </div>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>TDS on Interest (Bank)</label>
                            <input
                                type="number"
                                className="form-input"
                                value={income.tds_bank}
                                onChange={(e) => handleIncomeChange('tds_bank', e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Deductions Section */}
                    <div>
                        <h4 style={{ marginBottom: '16px', color: 'var(--text)' }}>Deductions</h4>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>80C Investments</label>
                            <input
                                type="number"
                                className="form-input"
                                value={deductions.section_80c_raw}
                                onChange={(e) => handleDeductionChange('section_80c_raw', e.target.value)}
                            />
                        </div>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>80D Health Insurance</label>
                            <input
                                type="number"
                                className="form-input"
                                value={deductions.section_80d_raw}
                                onChange={(e) => handleDeductionChange('section_80d_raw', e.target.value)}
                            />
                        </div>

                        <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>HRA Exemption</label>
                            <input
                                type="number"
                                className="form-input"
                                value={deductions.hra_exemption_raw}
                                onChange={(e) => handleDeductionChange('hra_exemption_raw', e.target.value)}
                            />
                        </div>
                    </div>
                </div>

                {error && (
                    <div className="error-box" style={{ marginTop: '16px', marginBottom: '0' }}>{error}</div>
                )}

                <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'flex-end' }}>
                    <button
                        type="submit"
                        className="btn-primary"
                        disabled={loading}
                        style={{ padding: '12px 24px' }}
                    >
                        {loading ? 'Resuming Workflow...' : '✅ Confirm Values & Resume Filing'}
                    </button>
                </div>
            </form>
        </div>
    )
}

import { useState } from 'react'
import TaxSummary from './TaxSummary'
import Timeline from './Timeline'
import FormPreview from './FormPreview'
import TaxTips from './TaxTips'
import ReviewForm from './ReviewForm'

function formatINR(amount) {
    if (!amount && amount !== 0) return '₹0'
    return '₹' + Number(amount).toLocaleString('en-IN')
}

function formatDate(isoStr) {
    if (!isoStr) return ''
    try {
        return new Date(isoStr).toLocaleString('en-IN', {
            day: '2-digit', month: 'short', year: 'numeric',
            hour: '2-digit', minute: '2-digit', hour12: true
        })
    } catch { return isoStr }
}

export default function RunDetail({ run: initialRun }) {
    const [run, setRun] = useState(initialRun)
    const [activeTab, setActiveTab] = useState('summary')
    const isVerified = run?.filing_status?.status === 'E_VERIFIED'
    const needsReview = run?.filing_status?.status === 'NEEDS_REVIEW'
    const tc = run?.tax_computation
    const ag = run?.aggregated_income
    const ds = run?.deduction_summary

    return (
        <div className="fade-in">
            {/* Header */}
            <div className="section-header" style={{ marginBottom: 20 }}>
                <div>
                    <div className="section-title">
                        {run.taxpayer?.name || 'ITR Filing'}
                        <span style={{ fontSize: 14, fontWeight: 400, color: 'var(--text-muted)', marginLeft: 12 }}>
                            PAN: {run.taxpayer?.pan}
                        </span>
                    </div>
                    <div className="section-meta">
                        FY {run.taxpayer?.financial_year || '2024-25'} • ITR-1 •
                        Age {run.taxpayer?.age} • Regime: {run.taxpayer?.regime}
                    </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                    {isVerified && (
                        <div style={{
                            display: 'inline-flex', alignItems: 'center', gap: 6,
                            padding: '4px 12px', borderRadius: 20,
                            background: 'rgba(0,214,143,0.15)', color: 'var(--accent-green)',
                            border: '1px solid rgba(0,214,143,0.3)', fontSize: 12, fontWeight: 700
                        }}>
                            ✓ E-VERIFIED
                        </div>
                    )}
                    {needsReview && (
                        <div style={{
                            display: 'inline-flex', alignItems: 'center', gap: 6,
                            padding: '4px 12px', borderRadius: 20,
                            background: 'rgba(255,101,132,0.15)', color: 'var(--accent-3)',
                            border: '1px solid rgba(255,101,132,0.3)', fontSize: 12, fontWeight: 700
                        }}>
                            ⚠ NEEDS REVIEW
                        </div>
                    )}
                    {run.run_id && (
                        <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 4 }}>
                            Run ID: {run.run_id.slice(0, 8)}...
                        </div>
                    )}
                </div>
            </div>

            {/* E-verified banner */}
            {isVerified && (
                <div className="verified-banner">
                    <div className="verified-icon">✅</div>
                    <div>
                        <div className="verified-title">ITR-1 Successfully E-Verified!</div>
                        <div className="verified-ack">Acknowledgement: {run.filing_status?.ack_number}</div>
                        <div className="verified-time">{formatDate(run.filing_status?.e_verified_at)}</div>
                    </div>
                </div>
            )}

            {needsReview && run.needs_review_reason && (
                <div className="error-box" style={{ marginBottom: 20 }}>
                    ⚠ {run.needs_review_reason}
                </div>
            )}

            {needsReview && (
                <ReviewForm run={run} onResumeComplete={setRun} />
            )}

            {/* Metric cards */}
            <div className="metric-grid">
                <div className="metric-card">
                    <div className="metric-label">Total Income</div>
                    <div className="metric-value accent">{formatINR(ag?.gross_total_income)}</div>
                    <div className="metric-sub">Salary + Interest + Other</div>
                </div>
                <div className="metric-card">
                    <div className="metric-label">Total Deductions</div>
                    <div className="metric-value">{formatINR(ds?.total_deductions)}</div>
                    <div className="metric-sub">Std. Ded. + 80C + 80D</div>
                </div>
                <div className="metric-card">
                    <div className="metric-label">{tc?.net_refund > 0 ? '🎉 Refund' : '💸 Tax Payable'}</div>
                    <div className={`metric-value ${tc?.net_refund > 0 ? 'positive' : 'negative'}`}>
                        {tc?.net_refund > 0 ? `+${formatINR(tc.net_refund)}` : formatINR(tc?.net_payable)}
                    </div>
                    <div className="metric-sub">Total TDS: {formatINR(tc?.total_tds)}</div>
                </div>
            </div>

            {/* Tabs */}
            <div className="tabs">
                {[
                    { id: 'summary', label: '📊 Tax Summary' },
                    { id: 'form', label: '📋 ITR-1 Form' },
                    { id: 'timeline', label: '⚙️ Agent Timeline' },
                    { id: 'tips', label: '💡 Tax Tips' },
                ].map(tab => (
                    <button
                        key={tab.id}
                        id={`tab-${tab.id}`}
                        className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                        {tab.id === 'tips' && run.tax_tips?.length > 0 && (
                            <span style={{
                                background: 'var(--accent)', color: 'white', borderRadius: '50%',
                                width: 16, height: 16, fontSize: 10, display: 'inline-flex',
                                alignItems: 'center', justifyContent: 'center', fontWeight: 700
                            }}>{run.tax_tips.length}</span>
                        )}
                    </button>
                ))}
            </div>

            {/* Tab content */}
            {activeTab === 'summary' && <TaxSummary run={run} />}
            {activeTab === 'form' && <FormPreview run={run} />}
            {activeTab === 'timeline' && <Timeline steps={run.agent_steps || []} />}
            {activeTab === 'tips' && <TaxTips tips={run.tax_tips || []} />}
        </div>
    )
}

import { useState } from 'react'

function formatDate(isoStr) {
    if (!isoStr) return ''
    try {
        return new Date(isoStr).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    } catch { return isoStr }
}

const AGENT_ICONS = {
    SupervisorAgent: '🎯',
    DocumentClassifierAgent: '📂',
    FieldExtractionAgent: '🔍',
    IncomeAggregatorAgent: '∑',
    DeductionClaimerAgent: '🏆',
    TaxComputationAgent: '🧮',
    ITRFormFillerAgent: '📄',
    EVerificationAgent: '✅',
}

export default function Timeline({ steps }) {
    const [expandedStep, setExpandedStep] = useState(null);

    if (!steps || steps.length === 0) {
        return <div className="empty-state">No agent steps recorded.</div>
    }

    return (
        <div className="card" style={{ padding: '24px 28px' }}>
            <div className="card-title">⚙️ Agent Processing Timeline</div>
            <div className="timeline">
                {steps.map((step, i) => {
                    const hasReasoning = step.details?.llm_explanations || step.details?.llm_confidence_logs;
                    const isExpanded = expandedStep === step.step_id;
                    return (
                        <div key={step.step_id || i} className="timeline-item" style={{ animationDelay: `${i * 0.08}s` }}>
                            <div className={`timeline-dot ${step.status?.toLowerCase()}`} />
                            <div className="timeline-content">
                                <div className="timeline-header">
                                    <div className="timeline-agent">
                                        {AGENT_ICONS[step.agent_name] || '🤖'}&nbsp; {step.agent_name.replace('Agent', ' Agent')}
                                    </div>
                                    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                                        <span className={`timeline-status ${step.status?.toLowerCase()}`}>
                                            {step.status}
                                        </span>
                                        {step.completed_at && (
                                            <span className="timeline-time">{formatDate(step.completed_at)}</span>
                                        )}
                                    </div>
                                </div>
                                {step.input_summary && (
                                    <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 3 }}>
                                        Input: {step.input_summary}
                                    </div>
                                )}
                                {step.output_summary && (
                                    <div className="timeline-output">{step.output_summary}</div>
                                )}
                                {step.error && (
                                    <div style={{ fontSize: 11, color: 'var(--accent-3)', marginTop: 4 }}>
                                        ⚠ Error: {step.error}
                                    </div>
                                )}
                                {/* Key details */}
                                {step.details && Object.keys(step.details).length > 0 && (
                                    <div style={{
                                        marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 8
                                    }}>
                                        {Object.entries(step.details)
                                            .filter(([k]) => !['run_id', 'status', 'ack_number', 'llm_explanations', 'llm_confidence_logs'].includes(k))
                                            .slice(0, 4)
                                            .map(([k, v]) => (
                                                <span key={k} style={{
                                                    fontSize: 10, padding: '2px 8px',
                                                    background: 'rgba(108,99,255,0.1)', borderRadius: 4,
                                                    color: 'var(--accent)', border: '1px solid rgba(108,99,255,0.2)'
                                                }}>
                                                    {k}: {typeof v === 'number' ? `₹${Number(v).toLocaleString('en-IN')}` : String(v).slice(0, 20)}
                                                </span>
                                            ))}
                                    </div>
                                )}

                                {/* AI Reasoning Accordion */}
                                {hasReasoning && (
                                    <div style={{ marginTop: 12 }}>
                                        <button
                                            onClick={() => setExpandedStep(isExpanded ? null : step.step_id)}
                                            style={{
                                                background: 'none', border: 'none', color: 'var(--accent)',
                                                fontSize: 11, cursor: 'pointer', padding: 0, display: 'flex', alignItems: 'center', gap: 4
                                            }}
                                        >
                                            {isExpanded ? '▼ Hide AI Reasoning' : '▶ View AI Reasoning'}
                                        </button>

                                        {isExpanded && (
                                            <div style={{
                                                marginTop: 8, padding: 12, background: 'var(--bg-secondary)',
                                                borderRadius: 6, fontSize: 11, color: 'var(--text-muted)', borderLeft: '2px solid var(--accent)'
                                            }}>
                                                {step.details.llm_explanations?.map((exp, idx) => (
                                                    <div key={idx} style={{ marginBottom: 4 }}>• {exp}</div>
                                                ))}
                                                {step.details.llm_confidence_logs && Object.entries(step.details.llm_confidence_logs).map(([file, log], idx) => (
                                                    <div key={idx} style={{ marginBottom: 4 }}>• <strong>{file}</strong>: {log}</div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

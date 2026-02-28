function formatINR(amount) {
    if (!amount) return null
    return '₹' + Number(amount).toLocaleString('en-IN')
}

export default function TaxTips({ tips }) {
    if (!tips || tips.length === 0) {
        return (
            <div className="empty-state">
                <div style={{ fontSize: 40, marginBottom: 12 }}>✅</div>
                <div>No additional optimization tips — your deductions look optimal!</div>
            </div>
        )
    }

    const totalSaving = tips.reduce((sum, t) => sum + (t.potential_saving || 0), 0)

    return (
        <div className="fade-in">
            <div className="card" style={{ marginBottom: 20 }}>
                <div className="card-title">💡 Tax Optimization Tips</div>
                <div style={{
                    padding: '14px 16px', borderRadius: 8, marginBottom: 20,
                    background: 'rgba(0,214,143,0.08)', border: '1px solid rgba(0,214,143,0.2)'
                }}>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 2 }}>
                        Total Potential Additional Savings
                    </div>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--accent-green)' }}>
                        {formatINR(totalSaving)}
                    </div>
                </div>

                {tips.map((tip, i) => (
                    <div key={i} className="tip-card">
                        <div className="tip-category">💡 {tip.category}</div>
                        <div className="tip-message">{tip.message}</div>
                        {tip.potential_saving && (
                            <div className="tip-saving">
                                Potential saving: {formatINR(tip.potential_saving)} / year
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <div className="card">
                <div className="card-title">📚 Key Tax Dates</div>
                <ul className="deduction-list">
                    {[
                        { label: 'ITR Filing Deadline (FY 2024-25)', value: '31 July 2025', note: 'Without penalty' },
                        { label: 'Belated Return Deadline', value: '31 December 2025', note: 'With penalty ₹5,000–₹10,000' },
                        { label: 'Revised Return Deadline', value: '31 December 2025', note: 'If correction needed' },
                        { label: '80C Investment Deadline', value: '31 March 2025', note: 'For FY 2024-25 claims' },
                    ].map((item, i) => (
                        <li key={i} className="deduction-item">
                            <div>
                                <div className="deduction-label">{item.label}</div>
                                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>{item.note}</div>
                            </div>
                            <span style={{ color: 'var(--accent-orange)', fontWeight: 600, fontSize: 13 }}>{item.value}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}

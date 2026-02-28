export default function WelcomeScreen({ onNew, loading }) {
    return (
        <div className="welcome fade-in">
            <div className="welcome-icon">🏛️</div>
            <h2>Agentic ITR Auto-Filer</h2>
            <p>
                India's first fully automatic ITR copilot. Upload Form 16 and Bank Interest Certificate
                — our 12 specialized AI agents will extract, compute, and e-verify your ITR-1 automatically.
            </p>

            <div style={{ display: 'flex', gap: '12px', marginTop: '24px', flexWrap: 'wrap', justifyContent: 'center' }}>
                <button className="btn-primary" style={{ width: 'auto', padding: '12px 32px', fontSize: '16px' }} onClick={onNew} disabled={loading}>
                    {loading ? '⏳ Processing...' : '📂 Upload & File ITR'}
                </button>
            </div>

            <div className="welcome-features">
                <div className="feature-chip">
                    <span className="feature-emoji">📋</span>
                    <div className="feature-label">Form 16 Upload</div>
                    <div className="feature-desc">Extract salary, TDS, and deductions automatically</div>
                </div>
                <div className="feature-chip">
                    <span className="feature-emoji">🏦</span>
                    <div className="feature-label">Bank Interest</div>
                    <div className="feature-desc">Auto-extract FD interest and TDS from statements</div>
                </div>
                <div className="feature-chip">
                    <span className="feature-emoji">🤖</span>
                    <div className="feature-label">12 AI Agents</div>
                    <div className="feature-desc">Extract → Validate → Compute → File pipeline</div>
                </div>
                <div className="feature-chip">
                    <span className="feature-emoji">💯</span>
                    <div className="feature-label">100% Automatic</div>
                    <div className="feature-desc">No manual data entry required</div>
                </div>
                <div className="feature-chip">
                    <span className="feature-emoji">✅</span>
                    <div className="feature-label">E-Verified</div>
                    <div className="feature-desc">Complete ITR-1 filing with e-verification</div>
                </div>
                <div className="feature-chip">
                    <span className="feature-emoji">💰</span>
                    <div className="feature-label">Tax Optimized</div>
                    <div className="feature-desc">Deduction caps, slab application, refund computed</div>
                </div>
            </div>

            <div style={{
                marginTop: '32px',
                padding: '16px 24px',
                background: 'rgba(76, 175, 80, 0.08)',
                border: '1px solid rgba(76, 175, 80, 0.2)',
                borderRadius: '12px',
                fontSize: '13px',
                color: 'var(--text-secondary)',
                maxWidth: '600px',
                lineHeight: '1.8'
            }}>
                <strong style={{ color: 'rgba(76, 175, 80, 1)' }}>✓ How It Works:</strong><br/>
                1️⃣ Upload your Form 16 PDF<br/>
                2️⃣ Upload Bank Interest Certificate<br/>
                3️⃣ Click "File ITR"<br/>
                4️⃣ View your ITR-1, tax computation, refund amount & timeline<br/>
                <br/>
                <strong style={{ color: 'rgba(76, 175, 80, 1)' }}>🎯 What Gets Calculated:</strong> Total income • Deduction caps (80C, 80D) • Tax liability • Refund/Payable amount • Complete ITR-1 form • Agent-by-agent timeline
            </div>
        </div>
    )
}

import { formatDistanceToNow } from 'date-fns'

function formatINR(amount) {
    if (!amount) return '₹0'
    return '₹' + Number(amount).toLocaleString('en-IN')
}

function getStatusClass(status) {
    switch (status) {
        case 'E_VERIFIED': return 'e-verified'
        case 'NEEDS_REVIEW': return 'needs-review'
        default: return 'pending'
    }
}

function getStatusLabel(status) {
    switch (status) {
        case 'E_VERIFIED': return '✓ E-Verified'
        case 'NEEDS_REVIEW': return '⚠ Review'
        case 'FILED': return '◉ Filed'
        case 'PROCESSING': return '⟳ Processing'
        default: return '◌ Pending'
    }
}

export default function RunsList({ runs, selectedId, onSelect }) {
    if (!runs.length) {
        return (
            <div className="empty-state">
                No filings yet.<br />Click "New ITR Filing" or<br />"Run Demo Scenario" to start.
            </div>
        )
    }

    return (
        <div>
            {runs.map(run => (
                <div
                    key={run.run_id}
                    className={`run-item ${selectedId === run.run_id ? 'active' : ''}`}
                    onClick={() => onSelect(run.run_id)}
                    id={`run-${run.run_id.slice(0, 8)}`}
                >
                    <div className="run-item-header">
                        <span className="run-name">{run.taxpayer_name || 'Taxpayer'}</span>
                        <span className={`status-badge ${getStatusClass(run.status)}`}>
                            {getStatusLabel(run.status)}
                        </span>
                    </div>
                    <div className="run-meta">
                        <span>PAN: {run.pan || 'N/A'}</span>
                        <span>FY: {run.financial_year || '2024-25'}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span className="run-meta" style={{ margin: 0 }}>
                            {run.created_at ? formatDistanceToNow(new Date(run.created_at), { addSuffix: true }) : ''}
                        </span>
                        {run.net_refund > 0 ? (
                            <span className="run-refund positive">+{formatINR(run.net_refund)}</span>
                        ) : run.net_payable > 0 ? (
                            <span className="run-refund negative">{formatINR(run.net_payable)}</span>
                        ) : (
                            <span className="run-refund" style={{ color: 'var(--text-muted)' }}>₹0</span>
                        )}
                    </div>
                </div>
            ))}
        </div>
    )
}

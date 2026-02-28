function formatINR(amount) {
    if (!amount && amount !== 0) return '₹0'
    return '₹' + Number(amount).toLocaleString('en-IN')
}

export default function FormPreview({ run }) {
    const form = run?.itr_form
    const tp = run?.taxpayer
    if (!form) return <div className="empty-state">No form data available.</div>

    const sal = form.schedule_salary
    const others = form.schedule_other_sources
    const via = form.schedule_via
    const tc = form.tax_computation

    return (
        <div className="card fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                <div>
                    <div style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)' }}>
                        📋 {form.itr_type} — Income Tax Return
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>
                        Assessment Year {form.part_a?.assessment_year || '2025-26'} • Indian Income Tax Department
                    </div>
                </div>
                <div style={{
                    padding: '6px 14px', borderRadius: 6,
                    background: 'rgba(0,214,143,0.1)', border: '1px solid rgba(0,214,143,0.3)',
                    fontSize: 12, fontWeight: 700, color: 'var(--accent-green)'
                }}>
                    FILED
                </div>
            </div>

            {/* Part A: Personal Information */}
            <div className="form-section">
                <div className="form-section-title">Part A — Personal Information</div>
                <div className="form-row">
                    <span className="form-row-label">Name of Assessee</span>
                    <span className="form-row-value">{form.part_a?.name || tp?.name || '—'}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Permanent Account Number (PAN)</span>
                    <span className="form-row-value">{form.part_a?.pan || tp?.pan || '—'}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Date of Birth / Age</span>
                    <span className="form-row-value">{form.part_a?.age || tp?.age || '—'} years</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Financial Year</span>
                    <span className="form-row-value">{form.part_a?.financial_year || '2024-25'}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Assessment Year</span>
                    <span className="form-row-value">{form.part_a?.assessment_year || '2025-26'}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Residential Status</span>
                    <span className="form-row-value" style={{ textTransform: 'capitalize' }}>{form.part_a?.residential_status || 'Resident'}</span>
                </div>
            </div>

            <div className="divider" />

            {/* Schedule S: Salary */}
            <div className="form-section">
                <div className="form-section-title">Schedule S — Salary Income</div>
                <div className="form-row">
                    <span className="form-row-label">Gross Salary</span>
                    <span className="form-row-value">{formatINR(sal?.gross_salary)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Less: Standard Deduction u/s 16(ia)</span>
                    <span className="form-row-value" style={{ color: 'var(--accent-green)' }}>(-) {formatINR(sal?.standard_deduction_u16)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Net Salary (after deduction)</span>
                    <span className="form-row-value" style={{ fontWeight: 700 }}>{formatINR(sal?.net_salary)}</span>
                </div>
            </div>

            <div className="divider" />

            {/* Schedule OS: Other Sources */}
            <div className="form-section">
                <div className="form-section-title">Schedule OS — Income from Other Sources</div>
                <div className="form-row">
                    <span className="form-row-label">Interest from FD / Savings</span>
                    <span className="form-row-value">{formatINR(others?.interest_income)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Total (Other Sources)</span>
                    <span className="form-row-value" style={{ fontWeight: 700 }}>{formatINR(others?.total)}</span>
                </div>
            </div>

            <div className="divider" />

            {/* Schedule VIA: Deductions */}
            <div className="form-section">
                <div className="form-section-title">Schedule VIA — Deductions (Chapter VI-A)</div>
                {via?.sec_80c > 0 && (
                    <div className="form-row">
                        <span className="form-row-label">Section 80C (PPF/ELSS/Life insurance)</span>
                        <span className="form-row-value">{formatINR(via?.sec_80c)}</span>
                    </div>
                )}
                {via?.sec_80d > 0 && (
                    <div className="form-row">
                        <span className="form-row-label">Section 80D (Health insurance)</span>
                        <span className="form-row-value">{formatINR(via?.sec_80d)}</span>
                    </div>
                )}
                <div className="form-row">
                    <span className="form-row-label">Total Deductions (VI-A)</span>
                    <span className="form-row-value" style={{ fontWeight: 700 }}>{formatINR(via?.total)}</span>
                </div>
            </div>

            <div className="divider" />

            {/* Computation of Tax */}
            <div className="form-section">
                <div className="form-section-title">Computation of Tax Liability</div>
                <div className="form-row">
                    <span className="form-row-label">Gross Total Income</span>
                    <span className="form-row-value">{formatINR(tc?.gross_total_income)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Less: Total Deductions</span>
                    <span className="form-row-value" style={{ color: 'var(--accent-green)' }}>(-) {formatINR(tc?.total_deductions)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Total Taxable Income</span>
                    <span className="form-row-value" style={{ fontWeight: 700 }}>{formatINR(tc?.taxable_income)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Tax on Total Income</span>
                    <span className="form-row-value">{formatINR(tc?.tax_on_income)}</span>
                </div>
                {tc?.rebate_87a > 0 && (
                    <div className="form-row">
                        <span className="form-row-label">Less: Rebate u/s 87A</span>
                        <span className="form-row-value" style={{ color: 'var(--accent-green)' }}>(-) {formatINR(tc?.rebate_87a)}</span>
                    </div>
                )}
                <div className="form-row">
                    <span className="form-row-label">Add: Health & Education Cess @4%</span>
                    <span className="form-row-value">{formatINR(tc?.health_education_cess)}</span>
                </div>
                <div className="form-row" style={{ fontWeight: 700, color: 'var(--accent-3)', fontSize: 14 }}>
                    <span className="form-row-label" style={{ color: 'var(--text-primary)' }}>Total Tax Liability</span>
                    <span>{formatINR(tc?.total_tax)}</span>
                </div>
                <div className="form-row">
                    <span className="form-row-label">Less: TDS (Employer + Bank)</span>
                    <span className="form-row-value" style={{ color: 'var(--accent-green)' }}>(-) {formatINR(tc?.tds)}</span>
                </div>
            </div>

            {/* Final outcome */}
            <div style={{
                marginTop: 16, padding: '18px 20px', borderRadius: 10,
                background: tc?.net_refund > 0 ? 'rgba(0,214,143,0.1)' : 'rgba(255,101,132,0.1)',
                border: tc?.net_refund > 0 ? '2px solid rgba(0,214,143,0.4)' : '2px solid rgba(255,101,132,0.4)',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
            }}>
                <div>
                    <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 4 }}>
                        {tc?.net_refund > 0 ? '🎉 Refund Due (to be credited to bank account)' : '💸 Tax Payable'}
                    </div>
                    <div style={{
                        fontSize: 32, fontWeight: 800,
                        color: tc?.net_refund > 0 ? 'var(--accent-green)' : 'var(--accent-3)'
                    }}>
                        {tc?.net_refund > 0 ? `+${formatINR(tc.net_refund)}` : formatINR(tc?.net_payable)}
                    </div>
                </div>
                {tc?.net_refund > 0 && (
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', textAlign: 'right' }}>
                        Expected within<br />
                        <strong style={{ color: 'var(--text-primary)', fontSize: 14 }}>15–45 days</strong><br />
                        after verification
                    </div>
                )}
            </div>
        </div>
    )
}

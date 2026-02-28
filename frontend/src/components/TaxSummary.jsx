function formatINR(amount) {
    if (!amount && amount !== 0) return '₹0'
    return '₹' + Number(amount).toLocaleString('en-IN')
}

export default function TaxSummary({ run }) {
    const tc = run?.tax_computation
    const ag = run?.aggregated_income
    const ds = run?.deduction_summary
    const nr = tc?.new_regime_comparison

    return (
        <div className="run-detail-grid">
            {/* Left column */}
            <div>
                {/* Income breakdown */}
                <div className="card" style={{ marginBottom: 20 }}>
                    <div className="card-title">💼 Income Breakdown</div>
                    <ul className="deduction-list">
                        <li className="deduction-item">
                            <span className="deduction-label">Salary Income</span>
                            <span className="deduction-value">{formatINR(ag?.total_salary)}</span>
                        </li>
                        <li className="deduction-item">
                            <span className="deduction-label">Interest Income</span>
                            <span className="deduction-value">{formatINR(ag?.total_interest)}</span>
                        </li>
                        {ag?.total_other > 0 && (
                            <li className="deduction-item">
                                <span className="deduction-label">Other Income</span>
                                <span className="deduction-value">{formatINR(ag?.total_other)}</span>
                            </li>
                        )}
                        <li className="deduction-total">
                            <span>Gross Total Income</span>
                            <span>{formatINR(ag?.gross_total_income)}</span>
                        </li>
                    </ul>
                </div>

                {/* Deductions */}
                <div className="card" style={{ marginBottom: 20 }}>
                    <div className="card-title">🏆 Deductions</div>
                    <ul className="deduction-list">
                        <li className="deduction-item">
                            <span className="deduction-label">Standard Deduction (u/s 16)</span>
                            <span className="deduction-value">{formatINR(ds?.standard_deduction)}</span>
                        </li>
                        {ds?.hra_exemption > 0 && (
                            <li className="deduction-item">
                                <span className="deduction-label">HRA Exemption</span>
                                <span className="deduction-value">{formatINR(ds?.hra_exemption)}</span>
                            </li>
                        )}
                        {ds?.section_80c > 0 && (
                            <li className="deduction-item">
                                <span className="deduction-label">Section 80C</span>
                                <span className="deduction-value">{formatINR(ds?.section_80c)}</span>
                            </li>
                        )}
                        {ds?.section_80d > 0 && (
                            <li className="deduction-item">
                                <span className="deduction-label">Section 80D</span>
                                <span className="deduction-value">{formatINR(ds?.section_80d)}</span>
                            </li>
                        )}
                        {ds?.other > 0 && (
                            <li className="deduction-item">
                                <span className="deduction-label">Other Deductions</span>
                                <span className="deduction-value">{formatINR(ds?.other)}</span>
                            </li>
                        )}
                        <li className="deduction-total">
                            <span>Total Deductions</span>
                            <span>{formatINR(ds?.total_deductions)}</span>
                        </li>
                    </ul>

                    {/* Deduction explanations */}
                    {ds?.explanation?.length > 0 && (
                        <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                            <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 6, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                                Agent Notes
                            </div>
                            <ul className="explanation-list">
                                {ds.explanation.map((e, i) => (
                                    <li key={i} className="explanation-item">{e}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            </div>

            {/* Right column */}
            <div>
                {/* Tax computation */}
                <div className="card" style={{ marginBottom: 20 }}>
                    <div className="card-title">💰 Tax Computation ({tc?.regime} Regime)</div>
                    <ul className="deduction-list">
                        <li className="deduction-item">
                            <span className="deduction-label">Gross Total Income</span>
                            <span className="deduction-value">{formatINR(tc?.gross_total_income)}</span>
                        </li>
                        <li className="deduction-item">
                            <span className="deduction-label">Less: Total Deductions</span>
                            <span className="deduction-value" style={{ color: 'var(--accent-green)' }}>-{formatINR(tc?.total_deductions)}</span>
                        </li>
                        <li className="deduction-item" style={{ fontWeight: 600 }}>
                            <span className="deduction-label">Taxable Income</span>
                            <span className="deduction-value">{formatINR(tc?.taxable_income)}</span>
                        </li>
                    </ul>

                    {/* Slab breakdown */}
                    {tc?.slab_breakdown?.length > 0 && (
                        <div style={{ marginTop: 16 }}>
                            <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 8 }}>
                                Slab-wise Calculation
                            </div>
                            <table className="slab-table">
                                <thead>
                                    <tr>
                                        <th>Income Slab</th>
                                        <th>Rate</th>
                                        <th>Amount</th>
                                        <th>Tax</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {tc.slab_breakdown.map((slab, i) => (
                                        <tr key={i}>
                                            <td>{slab.slab}</td>
                                            <td style={{ color: 'var(--accent)' }}>{slab.rate}</td>
                                            <td>{formatINR(slab.income)}</td>
                                            <td>{formatINR(slab.tax)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    <ul className="deduction-list" style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                        <li className="deduction-item">
                            <span className="deduction-label">Tax on Income</span>
                            <span className="deduction-value">{formatINR(tc?.tax_on_income)}</span>
                        </li>
                        {tc?.rebate_87a > 0 && (
                            <li className="deduction-item">
                                <span className="deduction-label">Less: Rebate u/s 87A</span>
                                <span className="deduction-value" style={{ color: 'var(--accent-green)' }}>-{formatINR(tc?.rebate_87a)}</span>
                            </li>
                        )}
                        <li className="deduction-item">
                            <span className="deduction-label">Add: Health & Ed. Cess (4%)</span>
                            <span className="deduction-value">{formatINR(tc?.health_education_cess)}</span>
                        </li>
                        <li className="deduction-total">
                            <span>Total Tax Liability</span>
                            <span style={{ color: 'var(--accent-3)' }}>{formatINR(tc?.total_tax_liability)}</span>
                        </li>
                        <li className="deduction-item">
                            <span className="deduction-label">Less: Total TDS</span>
                            <span className="deduction-value" style={{ color: 'var(--accent-green)' }}>-{formatINR(tc?.total_tds)}</span>
                        </li>
                    </ul>

                    <div style={{
                        marginTop: 12, padding: '14px 16px', borderRadius: 8,
                        background: tc?.net_refund > 0 ? 'rgba(0,214,143,0.1)' : 'rgba(255,101,132,0.1)',
                        border: tc?.net_refund > 0 ? '1px solid rgba(0,214,143,0.3)' : '1px solid rgba(255,101,132,0.3)',
                    }}>
                        <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 4 }}>
                            {tc?.net_refund > 0 ? '🎉 Refund Amount' : '💸 Tax Payable'}
                        </div>
                        <div style={{
                            fontSize: 28, fontWeight: 700,
                            color: tc?.net_refund > 0 ? 'var(--accent-green)' : 'var(--accent-3)'
                        }}>
                            {tc?.net_refund > 0 ? `+${formatINR(tc.net_refund)}` : formatINR(tc?.net_payable)}
                        </div>
                    </div>
                </div>

                {/* Regime comparison */}
                {nr && (
                    <div className="regime-compare">
                        <div className="regime-compare-title">⚖️ New Regime Comparison</div>
                        <div className="regime-compare-row">
                            <span>Taxable Income (New)</span>
                            <span>{formatINR(nr.taxable_income)}</span>
                        </div>
                        <div className="regime-compare-row">
                            <span>Total Tax (New Regime)</span>
                            <span>{formatINR(nr.total_tax)}</span>
                        </div>
                        <div className="regime-compare-row">
                            <span>Total Tax (Old Regime)</span>
                            <span>{formatINR(tc?.total_tax_liability)}</span>
                        </div>
                        <div className="regime-recommend">
                            💡 {nr.recommendation}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

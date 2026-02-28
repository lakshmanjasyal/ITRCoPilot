import { useState } from 'react'

const AGENTS_LOADING = [
    'DocumentClassifierAgent',
    'FieldExtractionAgent',
    'IncomeAggregatorAgent',
    'DeductionClaimerAgent',
    'TaxComputationAgent',
    'ITRFormFillerAgent',
    'EVerificationAgent',
]

export default function NewRunModal({ onSubmit, onClose, loading, error }) {
    const [files, setFiles] = useState([])
    const [dragging, setDragging] = useState(false)
    const [form, setForm] = useState({
        name: 'Taxpayer',
        pan: 'ABCDE1234F',
        age: '30',
        regime: 'OLD',
    })

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleDrop = (e) => {
        e.preventDefault()
        setDragging(false)
        const dropped = Array.from(e.dataTransfer.files)
        setFiles(prev => [...prev, ...dropped])
    }

    const handleFileInput = (e) => {
        setFiles(prev => [...prev, ...Array.from(e.target.files)])
    }

    const handleRemoveFile = (index) => {
        setFiles(prev => prev.filter((_, i) => i !== index))
    }

    const handleSubmit = () => {
        if (files.length === 0) {
            return
        }
        const fd = new FormData()
        files.forEach(f => fd.append('files', f))
        fd.append('name', form.name)
        fd.append('pan', form.pan)
        fd.append('age', form.age)
        fd.append('regime', form.regime)
        onSubmit(fd, 'upload')
    }

    return (
        <div className="fade-in" style={{ maxWidth: 740, margin: '0 auto' }}>
            <div className="section-header">
                <div>
                    <div className="section-title">📂 File Your ITR</div>
                    <div className="section-meta">Upload documents → AI extracts & files automatically</div>
                </div>
                <button
                    onClick={onClose}
                    style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 20 }}
                >✕</button>
            </div>

            {/* Taxpayer info */}
            <div className="card" style={{ marginBottom: 16 }}>
                <div className="card-title">👤 Taxpayer Profile</div>
                <div className="form-grid">
                    <div className="form-group">
                        <label className="form-label">Full Name</label>
                        <input id="input-name" name="name" className="form-input" value={form.name} onChange={handleChange} placeholder="Your Name" />
                    </div>
                    <div className="form-group">
                        <label className="form-label">PAN</label>
                        <input id="input-pan" name="pan" className="form-input" value={form.pan} onChange={handleChange} placeholder="ABCDE1234F" />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Age</label>
                        <input id="input-age" name="age" className="form-input" type="number" value={form.age} onChange={handleChange} />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Tax Regime</label>
                        <select id="select-regime" name="regime" className="form-select" value={form.regime} onChange={handleChange}>
                            <option value="OLD">Old Regime (with deductions)</option>
                            <option value="NEW">New Regime (lower slabs)</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Document Upload Section */}
            <div className="card" style={{ marginBottom: 16 }}>
                <div className="card-title">📁 Required Documents</div>
                <div style={{ color: 'var(--text-muted)', fontSize: 13, marginBottom: 16 }}>
                    Upload your Form 16 and Bank Interest Certificate. The AI will automatically extract all income, deductions, and TDS details.
                </div>
                
                <div
                    id="upload-dropzone"
                    className={`upload-zone ${dragging ? 'drag-over' : ''}`}
                    onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
                    onDragLeave={() => setDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => document.getElementById('file-input').click()}
                >
                    <div style={{ fontSize: 40 }}>📂</div>
                    <div className="upload-title">Drag & drop or click to upload</div>
                    <div className="upload-sub">Form 16 PDF • Bank Interest Certificate PDF</div>
                    <input id="file-input" type="file" multiple accept=".pdf,.png,.jpg,.jpeg" onChange={handleFileInput} style={{ display: 'none' }} />
                </div>

                {files.length > 0 && (
                    <div className="uploaded-files" style={{ marginTop: 16 }}>
                        {files.map((f, i) => (
                            <div key={i} className="uploaded-file">
                                <span style={{ fontSize: 18 }}>
                                    {f.name.toLowerCase().includes('form16') || f.name.toLowerCase().includes('16') ? '📋' : '🏦'}
                                </span>
                                <span className="uploaded-file-name">{f.name}</span>
                                <span className="uploaded-file-size">{(f.size / 1024).toFixed(1)} KB</span>
                                <button
                                    onClick={(e) => { e.stopPropagation(); handleRemoveFile(i) }}
                                    style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
                                >✕</button>
                            </div>
                        ))}
                    </div>
                )}

                <div style={{
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    border: '1px solid rgba(76, 175, 80, 0.3)',
                    borderRadius: '6px',
                    padding: '12px',
                    marginTop: '16px',
                    fontSize: '12px',
                    color: 'var(--text-secondary)',
                    lineHeight: '1.5'
                }}>
                    <strong>✓ What we'll do automatically:</strong><br/>
                    • Extract salary, FD interest, and other income from Form 16 and bank statement<br/>
                    • Calculate total income and all TDS deductionss<br/>
                    • Apply tax deduction caps (80C: ₹1.5L, etc.)<br/>
                    • Compute your tax liability and refund<br/>
                    • Fill and file your ITR-1<br/>
                    • E-verify your return
                </div>
            </div>

            {error && <div className="error-box" style={{ marginBottom: 16 }}>{error}</div>}

            {loading ? (
                <div className="loading-overlay" style={{ padding: '20px 0' }}>
                    <div className="spinner" />
                    <div className="loading-text">Processing your documents...</div>
                    <div className="loading-agents">
                        {AGENTS_LOADING.map((a, i) => (
                            <span key={a} style={{ opacity: 0.5, marginRight: 8, fontSize: 11 }}>⟳ {a}</span>
                        ))}
                    </div>
                </div>
            ) : (
                <button 
                    id="btn-file-itr" 
                    className="btn-primary" 
                    onClick={handleSubmit}
                    disabled={files.length === 0}
                    style={{ 
                        marginTop: 4,
                        opacity: files.length === 0 ? 0.5 : 1,
                        cursor: files.length === 0 ? 'not-allowed' : 'pointer'
                    }}
                >
                    {files.length === 0 
                        ? '📂 Upload documents to proceed' 
                        : `🚀 File ITR from ${files.length} Document${files.length > 1 ? 's' : ''}`
                    }
                </button>
            )}
        </div>
    )
}

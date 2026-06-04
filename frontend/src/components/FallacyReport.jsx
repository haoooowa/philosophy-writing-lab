const SEVERITY_LABELS = { critical: '严重', major: '重要', minor: '轻微' }
const TYPE_LABELS = {
  fallacy: '逻辑谬误',
  missing_premise: '缺失前提',
  vagueness: '概念模糊',
  gap: '推理跳跃',
  insufficient_evidence: '证据不足',
  category_error: '范畴错误',
}

export default function FallacyReport({ data }) {
  const issues = data?.issues || []

  if (!issues.length) {
    return (
      <div className="empty-state" style={{ color: 'var(--accent-sage)' }}>
        ✅ 未发现明显逻辑问题。论证看起来基本自洽。
      </div>
    )
  }

  return (
    <div>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1rem', fontSize: '0.9rem' }}>
        共发现 {data.total || issues.length} 个问题
      </p>
      {issues.map((issue, i) => (
        <div className={`issue-card ${issue.severity || 'minor'}`} key={i}>
          <div className="issue-header">
            <span className="issue-type">
              {TYPE_LABELS[issue.type] || issue.type || '问题'}
            </span>
            <span className="issue-severity">
              {SEVERITY_LABELS[issue.severity] || issue.severity}
            </span>
          </div>
          {issue.location && (
            <div className="issue-location">📍 {issue.location}</div>
          )}
          <div className="issue-explanation">{issue.explanation}</div>
        </div>
      ))}
    </div>
  )
}

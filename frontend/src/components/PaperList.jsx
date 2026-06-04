export default function PaperList({ data }) {
  const items = data?.papers || []
  if (!items.length) return <div className="empty-state">未找到相关文献</div>

  return (
    <div>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1rem', fontSize: '0.9rem' }}>
        共找到 {items.length} 条文献
      </p>
      <div className="card-list">
        {items.map((p, i) => {
          const isBook = p.is_book
          const title = p.title_en || p.title_cn || '未知'
          const subtitle = p.title_cn && p.title_cn !== p.title_en ? p.title_cn : ''
          const summary = p.summary || p.why_relevant || ''

          return (
            <div className="card" key={i} style={isBook ? { borderLeft: '3px solid var(--accent-gold)' } : {}}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
                {isBook && (
                  <span style={{
                    fontFamily: 'var(--font-ui)', fontSize: '0.7rem',
                    background: 'rgba(201,169,110,0.2)', color: 'var(--accent-gold)',
                    padding: '0.1rem 0.4rem', borderRadius: '4px',
                  }}>
                    📖 书籍
                  </span>
                )}
                <span className="card-title" style={{ marginBottom: 0 }}>{title}</span>
                {subtitle && (
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>({subtitle})</span>
                )}
              </div>
              <div className="card-meta">
                {(p.authors || []).join(', ')} · {p.year || '年份未知'}
                {p.source && <span style={{ marginLeft: '0.5rem', opacity: 0.5 }}>via {p.source}</span>}
              </div>
              {summary && <div className="card-summary">{summary}</div>}
            </div>
          )
        })}
      </div>
    </div>
  )
}

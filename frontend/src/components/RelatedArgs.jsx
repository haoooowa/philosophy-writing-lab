export default function RelatedArgs({ data }) {
  const sections = [
    { key: 'supporting', title: '✅ 支持性论证', color: 'var(--accent-sage)' },
    { key: 'opposing', title: '❌ 对立论证', color: 'var(--accent-rose)' },
    { key: 'variations', title: '🔄 变体论证', color: 'var(--accent-gold)' },
  ]

  return (
    <div>
      {sections.map((section) => {
        const items = data?.[section.key] || []
        if (!items.length) return null

        return (
          <div className="rel-section" key={section.key}>
            <h3 style={{ color: section.color }}>{section.title}</h3>
            <div className="card-list">
              {items.map((item, i) => (
                <div className="card" key={i}>
                  <div className="card-title">
                    {item.philosopher}
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginLeft: '0.5rem' }}>
                      {item.school}
                    </span>
                  </div>
                  <div className="card-meta">{item.argument_name}</div>
                  <div className="card-summary">{item.explanation}</div>
                </div>
              ))}
            </div>
          </div>
        )
      })}
      {!data?.supporting?.length && !data?.opposing?.length && !data?.variations?.length && (
        <div className="empty-state">未找到相关论证</div>
      )}
    </div>
  )
}

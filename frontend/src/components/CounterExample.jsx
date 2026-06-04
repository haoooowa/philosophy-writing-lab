export default function CounterExample({ data }) {
  const ce = data || {}

  if (!ce.thought_experiment && !ce.real_case && !ce.edge_case) {
    return <div className="empty-state">未能生成有效反例</div>
  }

  const items = [
    { label: '🧠 思想实验', data: ce.thought_experiment },
    { label: '📖 真实案例', data: ce.real_case },
    { label: '🔬 边界情况', data: ce.edge_case },
  ].filter((item) => item.data)

  return (
    <div>
      {items.map((item, i) => (
        <div className="ce-block" key={i}>
          <div className="ce-label">{item.label}</div>
          <div className="ce-scenario">{item.data.scenario || item.data.case}</div>
          <div className="ce-why">💡 {item.data.why_it_works}</div>
        </div>
      ))}
    </div>
  )
}

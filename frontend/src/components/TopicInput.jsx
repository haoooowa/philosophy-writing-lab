export default function TopicInput({ value, onChange }) {
  return (
    <div style={{ marginBottom: '1rem' }}>
      <label>研究主题</label>
      <input
        type="text"
        placeholder="例如：电车难题、自由意志、正义理论、存在主义..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  )
}

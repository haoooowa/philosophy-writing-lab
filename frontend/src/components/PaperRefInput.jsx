export default function PaperRefInput({ value, onChange }) {
  return (
    <div>
      <label>论文信息</label>
      <textarea
        placeholder="输入论文标题、作者等信息。例如：&#10;&#10;Harry Frankfurt, &quot;Freedom of the Will and the Concept of a Person&quot;&#10;&#10;或中文：&#10;赵汀阳《论可能生活》"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ minHeight: '80px' }}
      />
    </div>
  )
}

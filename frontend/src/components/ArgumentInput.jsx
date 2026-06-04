export default function ArgumentInput({ value, onChange }) {
  return (
    <div>
      <label>你的论证（可选，用于漏洞检测/反例生成/相关论证）</label>
      <textarea
        placeholder="请写下你的论证，包含前提和结论。例如：&#10;&#10;前提1：所有人都追求快乐&#10;前提2：快乐是唯一的内在善&#10;结论：因此，道德的标准是能否最大化快乐"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  )
}

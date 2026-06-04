import { useState } from 'react'
import ArgumentInput from './components/ArgumentInput'
import TopicInput from './components/TopicInput'
import PaperRefInput from './components/PaperRefInput'
import PaperList from './components/PaperList'
import FallacyReport from './components/FallacyReport'
import CounterExample from './components/CounterExample'
import RelatedArgs from './components/RelatedArgs'

// 本地用 localhost，线上用环境变量 VITE_API_BASE
const BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

const TABS = [
  { key: 'papers', label: '📚 主题搜文献', needs: 'topic' },
  { key: 'relatedPapers', label: '📎 论文追文献', needs: 'paper' },
  { key: 'fallacies', label: '🔍 漏洞检测', needs: 'argument' },
  { key: 'counterexamples', label: '⚡ 反例生成', needs: 'argument' },
  { key: 'related', label: '🔗 相关论证', needs: 'argument' },
]

const API_MAP = {
  papers: { endpoint: BASE + '/api/search-papers', body: (state) => ({ topic: state.topic }) },
  relatedPapers: { endpoint: BASE + '/api/related-papers', body: (state) => ({ paper: state.paperRef }) },
  fallacies: { endpoint: BASE + '/api/check-fallacies', body: (state) => ({ argument: state.argument }) },
  counterexamples: { endpoint: BASE + '/api/counterexamples', body: (state) => ({ argument: state.argument }) },
  related: { endpoint: BASE + '/api/related-arguments', body: (state) => ({ argument: state.argument }) },
}

export default function App() {
  const [topic, setTopic] = useState('')
  const [argument, setArgument] = useState('')
  const [paperRef, setPaperRef] = useState('')
  const [activeTab, setActiveTab] = useState('papers')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const state = { topic, argument, paperRef }

  const apiCall = async (endpoint, body) => {
    if (!body) return
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!res.ok) throw new Error(`请求失败 (${res.status})`)
      const data = await res.json()
      setResults(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleTab = (tab) => {
    setActiveTab(tab)
    setResults(null)
    setError(null)
    const cfg = API_MAP[tab]
    if (cfg) apiCall(cfg.endpoint, cfg.body(state))
  }

  const handleSearch = () => {
    const cfg = API_MAP[activeTab]
    if (cfg) apiCall(cfg.endpoint, cfg.body(state))
  }

  const renderInput = () => {
    switch (activeTab) {
      case 'papers':
        return <TopicInput value={topic} onChange={setTopic} label="研究主题" />
      case 'relatedPapers':
        return <PaperRefInput value={paperRef} onChange={setPaperRef} />
      case 'fallacies':
      case 'counterexamples':
      case 'related':
        return <ArgumentInput value={argument} onChange={setArgument} />
      default:
        return null
    }
  }

  return (
    <div>
      <header className="app-header">
        <h1>哲学论文写作助手</h1>
        <p>搜索文献 · 文献追踪 · 漏洞检测 · 反例生成 · 相关论证</p>
      </header>

      <main className="app-main">
        <div className="input-section">
          {renderInput()}
          <button
            onClick={handleSearch}
            disabled={loading}
            style={{
              marginTop: '1rem',
              padding: '0.65rem 2rem',
              background: 'var(--accent-gold)',
              color: 'var(--bg-primary)',
              border: 'none',
              borderRadius: 'var(--radius)',
              fontFamily: 'var(--font-ui)',
              fontWeight: 600,
              cursor: 'pointer',
              fontSize: '0.9rem',
            }}
          >
            {loading ? '分析中...' : '开始分析'}
          </button>
        </div>

        <div className="tabs">
          {TABS.map((t) => (
            <button
              key={t.key}
              className={`tab ${activeTab === t.key ? 'active' : ''}`}
              onClick={() => handleTab(t.key)}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div className="result-area">
          {loading && <div className="loading">⏳ 正在分析，请稍候...</div>}
          {error && <div className="error-state">❌ {error}</div>}
          {!loading && !error && results && (
            <>
              {(activeTab === 'papers' || activeTab === 'relatedPapers') && <PaperList data={results} />}
              {activeTab === 'fallacies' && <FallacyReport data={results} />}
              {activeTab === 'counterexamples' && <CounterExample data={results} />}
              {activeTab === 'related' && <RelatedArgs data={results} />}
            </>
          )}
          {!loading && !error && !results && (
            <div className="empty-state">
              {activeTab === 'papers' && '输入主题后点击"开始分析"搜索相关文献'}
              {activeTab === 'relatedPapers' && '输入一篇论文的标题（可加作者），查找相关文献'}
              {activeTab === 'fallacies' && '输入你的论证后点击"开始分析"检测逻辑漏洞'}
              {activeTab === 'counterexamples' && '输入你的论证后点击"开始分析"生成反例'}
              {activeTab === 'related' && '输入你的论证后点击"开始分析"检索相关论证'}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

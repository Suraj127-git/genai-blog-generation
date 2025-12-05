import { useDispatch, useSelector } from 'react-redux'
import { setLLM, setModel } from '../store/slices/blogSlice'
import type { RootState } from '../store'

const groqModels = [
  'llama-3.1-8b-instant',
  'llama3-8b-8192',
  'llama3-70b-8192',
  'gemma2-9b-it-1.2'
]

export default function ModelSelect() {
  const dispatch = useDispatch()
  const llm = useSelector((s: RootState) => s.blog.llm)
  const model = useSelector((s: RootState) => s.blog.model)
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      <select
        className="p-3 rounded border border-gray-300"
        value={llm}
        onChange={e => dispatch(setLLM(e.target.value))}
      >
        <option value="Groq">Groq</option>
      </select>
      <select
        className="p-3 rounded border border-gray-300"
        value={model}
        onChange={e => dispatch(setModel(e.target.value))}
      >
        {groqModels.map(m => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>
    </div>
  )
}

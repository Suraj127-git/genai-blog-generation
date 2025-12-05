import { useDispatch, useSelector } from 'react-redux'
import { setLanguage } from '../store/slices/blogSlice'
import type { RootState } from '../store'

const options = [
  { label: 'English', value: 'english' },
  { label: 'Hindi', value: 'hindi' },
  { label: 'French', value: 'french' }
]

export default function LanguageSelect() {
  const dispatch = useDispatch()
  const language = useSelector((s: RootState) => s.blog.language)
  return (
    <select
      className="w-full p-3 rounded border border-gray-300"
      value={language}
      onChange={e => dispatch(setLanguage(e.target.value))}
    >
      {options.map(o => (
        <option key={o.value} value={o.value}>{o.label}</option>
      ))}
    </select>
  )
}

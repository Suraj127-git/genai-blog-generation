import { useDispatch, useSelector } from 'react-redux'
import { generateBlog } from '../store/slices/blogSlice'
import type { RootState } from '../store'

export default function GenerateButton() {
  const dispatch = useDispatch()
  const loading = useSelector((s: RootState) => s.blog.loading)
  const topic = useSelector((s: RootState) => s.blog.topic)
  const disabled = loading || !topic
  return (
    <button
      className="w-full p-3 rounded bg-indigo-600 text-white disabled:opacity-50"
      disabled={disabled}
      onClick={() => dispatch(generateBlog())}
    >
      {loading ? 'Generating...' : 'Generate Blog'}
    </button>
  )
}

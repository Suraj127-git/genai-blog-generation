import { useSelector } from 'react-redux'
import type { RootState } from '../store'

export default function BlogDisplay() {
  const blog = useSelector((s: RootState) => s.blog.blog)
  const error = useSelector((s: RootState) => s.blog.error)
  if (error) return <div className="p-4 bg-red-100 text-red-800 rounded">{error}</div>
  if (!blog) return null
  const title = blog.title || 'Generated Blog'
  const content = blog.content || ''
  return (
    <div className="mt-6 bg-white rounded shadow p-6">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <pre className="whitespace-pre-wrap text-gray-700">{content}</pre>
    </div>
  )
}

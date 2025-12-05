import { useDispatch, useSelector } from 'react-redux'
import { setTopic } from '../store/slices/blogSlice'
import type { RootState } from '../store'

export default function TopicInput() {
  const dispatch = useDispatch()
  const topic = useSelector((s: RootState) => s.blog.topic)
  return (
    <input
      className="w-full p-3 rounded border border-gray-300 focus:outline-none focus:ring"
      placeholder="Enter blog topic"
      value={topic}
      onChange={e => dispatch(setTopic(e.target.value))}
    />
  )
}

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

export type BlogState = {
  topic: string
  language: string
  llm: string
  model: string
  loading: boolean
  error: string | null
  blog: { title?: string; content?: string } | null
}

const initialState: BlogState = {
  topic: '',
  language: 'english',
  llm: 'Groq',
  model: 'llama-3.1-8b-instant',
  loading: false,
  error: null,
  blog: null
}

export const generateBlog = createAsyncThunk(
  'blog/generate',
  async (_: void, { getState }) => {
    const state = getState() as { blog: BlogState }
    const payload = {
      topic: state.blog.topic,
      language: state.blog.language,
      llm: state.blog.llm,
      model: state.blog.model
    }
    const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const res = await axios.post(`${base}/blogs`, payload)
    return res.data
  }
)

const slice = createSlice({
  name: 'blog',
  initialState,
  reducers: {
    setTopic(state, action) { state.topic = action.payload },
    setLanguage(state, action) { state.language = action.payload },
    setLLM(state, action) { state.llm = action.payload },
    setModel(state, action) { state.model = action.payload }
  },
  extraReducers: builder => {
    builder.addCase(generateBlog.pending, state => { state.loading = true; state.error = null })
    builder.addCase(generateBlog.fulfilled, (state, action) => {
      state.loading = false
      const data = action.payload?.data || action.payload
      state.blog = data?.blog || data
    })
    builder.addCase(generateBlog.rejected, (state, action) => {
      state.loading = false
      state.error = action.error.message || 'Request failed'
    })
  }
})

export const { setTopic, setLanguage, setLLM, setModel } = slice.actions
export default slice.reducer

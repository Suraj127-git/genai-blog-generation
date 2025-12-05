import reducer, { setTopic, setLanguage, setLLM, setModel } from './blogSlice'

it('updates fields', () => {
  const s = reducer(undefined, { type: '@@INIT' })
  const s1 = reducer(s, setTopic('X'))
  expect(s1.topic).toBe('X')
  const s2 = reducer(s1, setLanguage('hindi'))
  expect(s2.language).toBe('hindi')
  const s3 = reducer(s2, setLLM('Groq'))
  expect(s3.llm).toBe('Groq')
  const s4 = reducer(s3, setModel('m'))
  expect(s4.model).toBe('m')
})

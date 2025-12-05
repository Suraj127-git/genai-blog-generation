import TopicInput from './components/TopicInput'
import LanguageSelect from './components/LanguageSelect'
import ModelSelect from './components/ModelSelect'
import GenerateButton from './components/GenerateButton'
import BlogDisplay from './components/BlogDisplay'

export default function App() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded p-6 mb-6">
        <h1 className="text-3xl font-bold">AI Blog Generator</h1>
        <p className="opacity-90">Generate engaging content with modern AI stack</p>
      </div>
      <div className="bg-white rounded shadow p-6 grid gap-4">
        <TopicInput />
        <LanguageSelect />
        <ModelSelect />
        <GenerateButton />
      </div>
      <BlogDisplay />
    </div>
  )
}

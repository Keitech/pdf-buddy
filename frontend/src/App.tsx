import { useRef, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'

type UploadedDocument = {
  id: string
  original_filename: string
  file_size: number
  character_count: number
  upload_time: string
}

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function App() {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [documents, setDocuments] = useState<UploadedDocument[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState<string | null>(null)
  const [asking, setAsking] = useState(false)
  const [chatError, setChatError] = useState<string | null>(null)

  async function handleUpload(files: FileList | null) {
    if (!files?.length) return

    setUploading(true)
    setUploadError(null)

    try {
      const uploaded: UploadedDocument[] = []

      for (const file of Array.from(files)) {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('/documents/upload', {
          method: 'POST',
          body: formData,
        })

        if (!response.ok) {
          const detail = await response.json().catch(() => null)
          throw new Error(detail?.detail ?? `Failed to upload ${file.name}`)
        }

        uploaded.push(await response.json())
      }

      setDocuments((current) => [...uploaded, ...current])
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : 'Upload failed')
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  async function handleAsk(event: FormEvent) {
    event.preventDefault()
    const trimmed = question.trim()
    if (!trimmed || asking) return

    setAsking(true)
    setChatError(null)
    setAnswer(null)

    try {
      const response = await fetch('/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed }),
      })

      if (!response.ok) {
        const detail = await response.json().catch(() => null)
        throw new Error(detail?.detail ?? 'Failed to get an answer')
      }

      const data = await response.json()
      setAnswer(data.answer)
    } catch (error) {
      setChatError(error instanceof Error ? error.message : 'Search failed')
    } finally {
      setAsking(false)
    }
  }

  return (
    <main className="app">
      <header className="brand">
        <p className="brand-mark">PDF Buddy</p>
        <h1>Welcome to PDF Buddy</h1>
        <p className="lede">
          Upload documents, then ask questions to search across them.
        </p>
      </header>

      <section className="upload" aria-labelledby="upload-heading">
        <h2 id="upload-heading">Documents</h2>
        <label className="dropzone">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            multiple
            disabled={uploading}
            onChange={(event) => handleUpload(event.target.files)}
          />
          <span className="dropzone-title">
            {uploading ? 'Uploading…' : 'Choose PDF files'}
          </span>
          <span className="dropzone-hint">One or more PDFs</span>
        </label>
        {uploadError && <p className="error">{uploadError}</p>}

        <ul className="doc-list" aria-live="polite">
          {documents.length === 0 ? (
            <li className="empty">No documents uploaded yet.</li>
          ) : (
            documents.map((doc) => (
              <li key={doc.id}>
                <span className="doc-name">{doc.original_filename}</span>
                <span className="doc-meta">
                  {formatBytes(doc.file_size)} · {doc.character_count.toLocaleString()} chars
                </span>
              </li>
            ))
          )}
        </ul>
      </section>

      <section className="chat" aria-labelledby="chat-heading">
        <h2 id="chat-heading">Ask a question</h2>
        <form onSubmit={handleAsk}>
          <label className="sr-only" htmlFor="question">
            Question
          </label>
          <textarea
            id="question"
            rows={3}
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="What would you like to find in your documents?"
            disabled={asking}
          />
          <button type="submit" disabled={asking || !question.trim()}>
            {asking ? 'Searching…' : 'Search documents'}
          </button>
        </form>
        {chatError && <p className="error">{chatError}</p>}

        <div className="answer" aria-live="polite">
          <h3>Answer</h3>
          <p>{answer ?? 'Ask a question to see results here.'}</p>
        </div>
      </section>
    </main>
  )
}

export default App

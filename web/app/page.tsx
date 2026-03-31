'use client'

import { useState } from 'react'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [caption, setCaption] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    alert('⚠️ Web Demo Only!\n\nFor real Instagram posting, download the desktop version from GitHub.')
    setIsLoggedIn(true)
  }

  const handlePost = (type: string) => {
    if (!isLoggedIn) {
      alert('Please login first!')
      return
    }
    alert(`📸 ${type} feature available in desktop version!\n\nDownload from: https://github.com/SauravDnj/Instagram-Automation`)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <span className="text-3xl">📸</span>
              <h1 className="text-2xl font-bold text-gray-900">Instagram Automation</h1>
            </div>
            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
              ✅ 100% FREE
            </span>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Alert */}
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <span className="text-2xl">⚠️</span>
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                <strong>Demo Version!</strong> For real Instagram posting, download the{' '}
                <a
                  href="https://github.com/SauravDnj/Instagram-Automation"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-bold underline hover:text-yellow-800"
                >
                  Desktop Version
                </a>
              </p>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Login Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              {isLoggedIn ? '✅ Demo Login' : '🔐 Login'}
            </h2>

            {!isLoggedIn ? (
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Instagram Username
                  </label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    placeholder="your_username"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Password (Demo)
                  </label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    placeholder="your_password"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-3 px-4 rounded-lg hover:from-purple-700 hover:to-pink-700"
                >
                  Demo Login
                </button>
              </form>
            ) : (
              <div className="text-center py-8">
                <div className="text-6xl mb-4">✅</div>
                <p className="text-lg font-semibold text-green-600">
                  Demo Login Active
                </p>
              </div>
            )}
          </div>

          {/* Post Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">📤 Quick Post</h2>

            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-3">
                <button
                  onClick={() => handlePost('Photo')}
                  className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-6 px-4 rounded-lg"
                >
                  <div className="text-3xl mb-2">📷</div>
                  <div className="text-sm">Photo</div>
                </button>

                <button
                  onClick={() => handlePost('Video')}
                  className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-6 px-4 rounded-lg"
                >
                  <div className="text-3xl mb-2">🎥</div>
                  <div className="text-sm">Video</div>
                </button>

                <button
                  onClick={() => handlePost('Story')}
                  className="bg-pink-500 hover:bg-pink-600 text-white font-bold py-6 px-4 rounded-lg"
                >
                  <div className="text-3xl mb-2">📖</div>
                  <div className="text-sm">Story</div>
                </button>
              </div>

              <textarea
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                rows={4}
                placeholder="Caption #hashtags"
              />
            </div>
          </div>
        </div>

        {/* Download CTA */}
        <div className="mt-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg shadow-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">🖥️ Get the Desktop Version</h2>
          <p className="text-lg mb-6">
            Full features, better security, real Instagram posting!
          </p>
          <a
            href="https://github.com/SauravDnj/Instagram-Automation"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-white text-purple-600 font-bold py-3 px-8 rounded-lg hover:bg-gray-100"
          >
            Download from GitHub →
          </a>
        </div>
      </div>

      <footer className="bg-white mt-12 border-t">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
          <p>Made with ❤️ by <a href="https://github.com/SauravDnj" className="text-purple-600 hover:underline">Saurav Dnj</a></p>
        </div>
      </footer>
    </main>
  )
}

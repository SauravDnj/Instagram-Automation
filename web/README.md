# Instagram Automation - Web Version

🌐 **Deploy to Vercel** - Web-based Instagram automation interface

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/SauravDnj/Instagram-Automation)

## 📦 Local Development

1. **Install dependencies**
```bash
cd web
npm install
```

2. **Run development server**
```bash
npm run dev
```

3. **Open in browser**
```
http://localhost:3000
```

## 🌐 Deploy to Vercel

### Method 1: One-Click Deploy (Easiest)

1. Click the "Deploy with Vercel" button above
2. Sign in to Vercel with GitHub
3. Connect your repository
4. Click "Deploy"
5. Done! Your app will be live in ~2 minutes

### Method 2: Vercel CLI

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
cd web
vercel
```

4. **Follow prompts** and your app will be deployed!

## ⚠️ Important Notes

**Security Considerations:**
- The web version is for demonstration purposes
- Instagram credentials should NEVER be stored on a server
- For production use, implement proper authentication and encryption
- Consider using the desktop version for better security

**Instagram API Limitations:**
- Instagram may block server-based automation
- Desktop version is more reliable and secure
- Use web version at your own risk

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **UI**: React + Tailwind CSS
- **Deployment**: Vercel
- **API**: Serverless functions

## 📁 Structure

```
web/
├── app/              # Next.js app directory
├── components/       # React components
├── public/          # Static assets
└── styles/          # Global styles
```

## 🔒 Security Best Practices

For production deployment:

1. **Never store passwords in plain text**
2. **Use environment variables** for sensitive data
3. **Implement rate limiting**
4. **Add authentication** (OAuth, JWT)
5. **Use HTTPS only**
6. **Encrypt all data in transit and at rest**

## 📝 License

MIT License - See LICENSE file

---

**Recommendation**: Use the desktop version for better security and reliability!

# 🧠 AI Blog Generator from YouTube Videos

The **AI Blog Generator** is a smart web app that generates high-quality blog posts from **YouTube video links** using **OpenAI's GPT models** and a **Django (Python)** backend. It transcribes, summarizes, and transforms video content into well-structured, readable blogs in seconds.

![Demo Banner](https://your-image-link-if-any)

---
## 🚀 Key Features

- 🔗 **Input YouTube Link** — Just paste a video link
- 🧠 **AI-Powered Blog Creation** — Summarized using OpenAI (GPT-4 / GPT-3.5)
- ✍️ **Well-Formatted Output** — Auto-generated blog with proper headings and paragraphs
- 🌐 **Responsive UI** — Built for both desktop and mobile
- ⚙️ **Backend with Django** — Handles transcription, OpenAI calls, and blog generation

---

## ⚙️ How It Works

1. User enters a **YouTube video URL**
2. Backend extracts **video transcript** using `youtube-transcript-api`
3. Transcript is sent to **OpenAI** to summarize and format into a blog
4. Blog is returned and displayed on the frontend

---
## 🚀 Setup & Run

### 1. Clone the Repository
```bash
git clone https://github.com/jaiganesh2108/AI-Blog-Generator.git
cd AI_Blog_Generator

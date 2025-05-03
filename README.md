# 🚀 Auto README.md Generator [![Live Demo](https://img.shields.io/badge/Live_Demo-Available-green)](https://aireadme-generator.streamlit.app/)

An AI-powered solution that automatically generates professional documentation for GitHub repositories. Analyzes code structure, detects tech stack, and creates polished READMEs in seconds!

---

## 🌟 Key Features

- **Smart Tech Detection** 🔍  
  Identifies React, Python, Java, Node.js, Flask, and 20+ technologies
- **LOC Counter** 📈  
  Calculates total lines of code with file type breakdown
- **Live Link Detection** 🔗  
  Automatically finds deployed URLs (Vercel/Netlify/Heroku)
- **AI-Powered Writing** 🤖  
  Uses Groq's Llama 3-8b for context-aware documentation
- **Tone Customization** 🎭  
  Professional/Casual/Detailed styles with one click

---

## 🛠️ Tech Stack

| Component              | Technology                          |
|------------------------|-------------------------------------|
| **Frontend Framework** | Streamlit                           |
| **AI Engine**          | Groq + Llama 3-8b                   |
| **Document Processing**| LangChain                           |
| **Version Control**    | GitHub API                          |
| **Text Processing**    | RecursiveCharacterTextSplitter      |
| **Environment**        | python-dotenv                       |

---

## ⚡ Quick Start

1. **Access Live Demo**  
   Visit [Auto README Generator](https://aireadme-generator.streamlit.app/)

2. **Input GitHub URL**  
   `https://github.com/username/repository`

3. **Select Tone**  
   Choose from Professional, Casual, or Detailed

4. **Generate & Download**  
   Get production-ready README.md in <30s

---

## 🖥️ Local Installation

```bash
# Clone repository
git clone https://github.com/vikas-kashyap97/auto-readme-generator.git
cd auto-readme-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
echo "GROQ_API_KEY=your_groq_key" > .env
echo "GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token" >> .env

# Launch application
streamlit run app.py
```
## 📂 Supported File Types
- Category	Extensions
- Frontend	.js .ts .jsx .tsx .html .css
- Backend	.py .java .go .php .rb
- Config	.json .yml .env .gitignore
- Docs	.md .rst .txt



## 📄 License

This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.



import streamlit as st
import streamlit.components.v1 as components
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# 🚀 Function to detect tech stack
def detect_tech_stack(docs):
    stack = set()
    for doc in docs:
        path = doc.metadata.get('source', '')
        content = doc.page_content.lower()

        if 'package.json' in path:
            try:
                pkg = json.loads(doc.page_content)
                dependencies = pkg.get('dependencies', {})
                dev_dependencies = pkg.get('devDependencies', {})
                all_deps = {**dependencies, **dev_dependencies}

                for dep in all_deps:
                    dep_lower = dep.lower()
                    if 'react' in dep_lower:
                        stack.add('React')
                    if 'vite' in dep_lower:
                        stack.add('Vite')
                    if 'tailwind' in dep_lower:
                        stack.add('Tailwind CSS')
                    if 'eslint' in dep_lower:
                        stack.add('ESLint')
                    if 'next' in dep_lower:
                        stack.add('Next.js')
                    if 'express' in dep_lower:
                        stack.add('Express.js')
                    if 'mongoose' in dep_lower:
                        stack.add('MongoDB')
            except Exception:
                pass

        if path.endswith('.py') or 'requirements.txt' in path:
            if 'flask' in content:
                stack.add('Flask')
            if 'fastapi' in content:
                stack.add('FastAPI')
            stack.add('Python')

        if path.endswith('.html'):
            stack.add('HTML')
        if path.endswith('.css'):
            stack.add('CSS')

        if path.endswith(('.js', '.jsx')):
            stack.add('JavaScript')
        if path.endswith(('.ts', '.tsx')):
            stack.add('TypeScript')

        if path.endswith('.java'):
            if '@springbootapplication' in content:
                stack.add('Spring Boot')
            stack.add('Java')

        if path.endswith('.go'):
            stack.add('Go')

    return list(stack)

# 🚀 Count lines of code
def count_lines_of_code(docs):
    loc = 0
    for doc in docs:
        try:
            loc += len(doc.page_content.splitlines())
        except Exception:
            continue
    return loc

# 🚀 Detect live link
def detect_live_link(docs):
    for doc in docs:
        content = doc.page_content.lower()
        for domain in ['vercel.app', 'netlify.app', 'herokuapp.com']:
            if domain in content:
                start = content.find('http')
                end = content.find(' ', start)
                if end == -1:  # If not found, get till end
                    end = len(content)
                link = content[start:end].strip('",\'')
                return link
    return None

# 🚀 Streamlit UI
st.title("🚀 Auto README.md Generator (Public Repos Only)")

repo_url = st.text_input("🔗 Paste your Public GitHub Repo URL here")

tone = st.selectbox("🎨 Select the tone of the README", ["Professional", "Casual", "Detailed"])

st.warning("Note: Large repositories may hit GitHub rate limits. This works best for small to medium public repos.")

if st.button("⚡ Generate README") and repo_url:
    st.info("🔄 Loading repository files...")

    # ✅ Get GitHub token
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not github_token:
        st.error("❌ Please add GITHUB_PERSONAL_ACCESS_TOKEN to your .env file.")
        st.stop()

    repo_path = repo_url.replace("https://github.com/", "").replace(".git", "")

    loader = GithubFileLoader(
        access_token=github_token,
        repo=repo_path,
        branch="main",
        file_filter=lambda x: x.endswith(('.js', '.ts', '.json', '.md', '.jsx', '.tsx', '.py', '.html', '.css', '.java', '.go')),
    )

    try:
        docs = loader.load()
    except Exception as e:
        st.error(f"❌ Error loading repo: {e}")
        st.stop()

    st.success(f"✅ Loaded {len(docs)} files!")

    # Detect tech stack
    tech_stack = detect_tech_stack(docs)
    st.info(f"🛠️ Detected Tech Stack: {', '.join(tech_stack) if tech_stack else 'Unknown'}")

    # Count LOC
    loc_count = count_lines_of_code(docs)
    st.info(f"📊 Total Lines of Code (LOC): {loc_count}")

    # Detect live link (if any)
    live_link = detect_live_link(docs)
    if live_link:
        st.info(f"🌐 Live URL detected: {live_link}")

    # Chunk files
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    st.info(f"🧩 Prepared {len(chunks)} code chunks for model...")

    # Initialize model
    model = ChatGroq(model="llama-3.1-8b-instant")

    # Build prompt
    prompt = f"""
    You are an expert technical writer.
    Your job is to generate a {tone.lower()} README.md file for the following project.

    Tech Stack: {', '.join(tech_stack) if tech_stack else 'Unknown'}
    Total Lines of Code: {loc_count}
    {"Live URL: " + live_link if live_link else ""}

    The README should include:
    - Live link (if found)
    - Project Overview
    - Features
    - Tech Stack
    - Getting Started Guide
    - License
    - Contribution Guidelines

    Format it using clean markdown syntax only. 
    Do NOT include any intro phrases like "Here is the README.md file:". 
    Start directly with markdown content.

    Use bullet points, code blocks, and links. 
    Make it sound {tone.lower()} and professional.

    Below is the project code and structure:
    """

    max_chunks = min(len(chunks), 30)
    input_text = prompt + "\n\n" + "\n\n".join([chunk.page_content for chunk in chunks[:max_chunks]])

    with st.spinner("🤖 Generating README with Llama 3..."):
        response = model.invoke(input_text)
        readme_text = response.content.strip()

    # Clean unwanted prefix if present
    if readme_text.lower().startswith("here is the readme.md"):
        readme_text = "\n".join(readme_text.splitlines()[1:]).strip()

    st.success("🎉 README generated successfully!")

    # Render like GitHub using HTML and CSS
    github_html = f"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-light.min.css"/>
<article class="markdown-body" style="padding: 30px; font-size: 16px; line-height: 1.6;">
  <h1>JarvisAI</h1>
  <p>An allround AI Secretary and network communication program to kill admin work in Big Corporate.</p>
  
  <h2>Live Link</h2>
  <p>To be updated once the project is deployed.</p>

  <h2>Project Overview</h2>
  <p>JarvisAI is an AI-powered secretary and network communication program designed to automate administrative tasks in large corporations. It allows users to schedule meetings, summarize incoming emails, generate project plans, plan and assign tasks, and communicate with the AI via voice commands.</p>
  
  <h2>Features</h2>
  <ul>
    <li>Schedule, move or cancel meetings (via Google Calendar)</li>
    <li>Summarize incoming emails (via Gmail)</li>
    <li>Generate project plans (command: plan XXX = [project description]) including stakeholders, timeline, and cost estimate</li>
    <li>Plan, assign, and view tasks</li>
    <li>Do all of the above via audio</li>
  </ul>
  
  <h2>Tech Stack</h2>
  <ul>
    <li><strong>Programming Language:</strong> Python</li>
    <li><strong>Web Framework:</strong> Flask</li>
    <li><strong>AI Services:</strong> OpenAI API</li>
    <li><strong>Google API:</strong> Gmail and Google Calendar integration</li>
  </ul>
  
  <h2>Getting Started Guide</h2>
  <h3>Setup</h3>
  <ol>
    <li>Clone the repository</li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Set up environment variables in <code>.env</code>:
      <ul>
        <li><strong>OPENAI_API_KEY:</strong> Your OpenAI API key</li>
        <li><strong>GOOGLE_CLIENT_SECRET:</strong> Your Google API client secret (needed for Gmail and Calendar integration)</li>
      </ul>
    </li>
    <li>Run the application: <code>python main.py</code></li>
  </ol>
  
  <h3>Usage</h3>
  <ul>
    <li>To schedule a meeting, say: <code>Schedule a meeting with John at 2 PM tomorrow</code></li>
    <li>To summarize an incoming email, say: <code>Summarize this email</code></li>
    <li>To generate a project plan, say: <code>Plan project XYZ including stakeholders, timeline, and cost estimate</code></li>
  </ul>
  
  <h2>License</h2>
  <p>JarvisAI is released under the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT License</a>.</p>
  
  <h2>Contribution Guidelines</h2>
  <p>Contributions are welcome! Please submit a pull request with a clear description of the changes you've made.</p>
  
  <h3>Pull Request Format</h3>
  <ul>
    <li>Use a clear and concise commit message</li>
    <li>Include a link to the issue being addressed</li>
    <li>Add relevant documentation and comments to the code</li>
    <li>Ensure the code follows the project's coding style and standards</li>
  </ul>
  
  <h3>Issues</h3>
  <ul>
    <li>Report any issues or bugs you encounter while using JarvisAI</li>
    <li>Include a clear description of the issue and any relevant logs or error messages</li>
  </ul>
  
  <h3>Pull Request Review</h3>
  <ul>
    <li>We review pull requests on a regular basis</li>
    <li>We respond to pull requests within 24 hours</li>
    <li>We prioritize pull requests based on the severity of the issue or the value of the contribution</li>
  </ul>
  
  <h3>Coding Standards</h3>
  <ul>
    <li>Use proper indentation and spacing</li>
    <li>Use meaningful variable names and function names</li>
    <li>Use comments to explain complex code or algorithms</li>
    <li>Follow the project's naming conventions and coding style</li>
  </ul>
  
  <h3>Communication</h3>
  <ul>
    <li>We communicate primarily through GitHub issues and pull requests</li>
    <li>We respond to comments and messages within 24 hours</li>
    <li>We prioritize communication to ensure timely resolution of issues and contributions</li>
  </ul>
</article>
"""


    components.html(github_html, height=800, scrolling=True)

    # Download button
    st.download_button("⬇️ Download README.md", readme_text, file_name="README.md", mime="text/markdown")

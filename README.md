# LLM-Powered File System

## Project brief

A small system that combines **file-system tools** (read, list, write, search, find path by name) with an **LLM assistant** that calls those tools from natural-language prompts. Use it to list directories, read PDF/TXT/DOCX resumes, search for keywords (including inside PDF/DOCX), write summary files, and resolve paths by name (e.g. “Read all resumes in the resumes folder”, “Find resumes mentioning Python experience”).

**Part A:** `fs_tools.py` — core file tools. **Part B:** `llm_file_assistant.py` — OpenAI tool-calling assistant.

---

## Quick start: GPT-style terminal chat (Part B)

From the project root, with `OPENAI_API_KEY` set in `.env`:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python llm_file_assistant.py --chat
```

You get an interactive terminal UI (Rich panels): type natural-language requests, the model calls file tools, and answers appear in the chat. Type `exit` or `quit` to leave.

**Example prompts to try:**

```text
List all files in the resumes folder.
Find resumes mentioning Python experience.
Create a summary file resumes/summary_john_doe.txt for resume_john_doe.pdf.
```

While the model runs, the UI shows **Thinking…** and which tools are invoked (e.g. `Calling: list_files, search_in_file`).

**One-shot demo (no chat UI):**

```bash
python llm_file_assistant.py
```

Runs a single built-in prompt (list resumes + search for Python). Change the `prompt` at the bottom of `llm_file_assistant.py` to experiment.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  User prompt                                                     │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  llm_file_assistant.py                                           │
│  • OpenAI client (gpt-5.1)                                    │
│  • Tools: read_file, list_files, write_file, search_in_file,      │
│    get_path_by_name (OpenAI function-calling format)              │
│  • Loop: chat completion → if tool_calls → run_tool() →           │
│    append results → repeat until model returns text              │
│  • Paths resolved relative to PROJECT_ROOT; leading project-name │
│    segment stripped to avoid double-nesting                      │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  fs_tools.py                                                     │
│  • read_file(filepath)     → dict (content, filename, size, err) │
│  • list_files(dir, ext?)   → list of {name, size, modified}       │
│  • write_file(path, content) → dict (success, path, error)        │
│  • search_in_file(path, keyword) → dict (matches; PDF/DOCX/TXT)   │
│  • get_path_by_name(root_dir, name) → dict (paths[], name)       │
│  Supported: PDF (pypdf), DOCX (python-docx), TXT                  │
└─────────────────────────────────────────────────────────────────┘
```

- **fs_tools**: Pure file I/O. Paths may use `~`; it is expanded. `get_path_by_name(root_dir, name)` finds files/dirs by exact case-sensitive name under a root. No LLM dependency.
- **llm_file_assistant**: Loads `.env` for `OPENAI_API_KEY`, defines tools (including optional `extension` on `list_files`), runs the chat loop, and executes tools via `fs_tools`. Paths are resolved against `PROJECT_ROOT`.
- **Sample data**: `resumes/` holds TXT, PDF, and DOCX examples aligned with the assignment brief (`resume_john_doe.*`, `resume_jane_smith.txt`).

---

## How to run (full setup)

1. **Create a virtualenv and install dependencies** (skip if you did this in Quick start)

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**

   Create a `.env` file in the project root:

   ```text
   OPENAI_API_KEY=sk-...
   ```

3. **Start the GPT-style file assistant**

   ```bash
   python llm_file_assistant.py --chat
   ```

   See [Quick start: GPT-style terminal chat (Part B)](#quick-start-gpt-style-terminal-chat-part-b) for example prompts and UI behavior.

4. **Use the file tools alone (optional, Part A — no API key)**

   Guided walkthrough: lists `resumes/`, explains each step, searches `resume_john_doe.pdf` for `Python`. Steps are spaced with a short silent delay (not printed in the terminal).

   Default (2.5s between steps):

   ```bash
   python fs_tools.py
   ```

   Slower — useful for screen recordings:

   ```bash
   FS_TOOLS_DEMO_PAUSE=4 python fs_tools.py
   ```

   Faster — when iterating locally:

   ```bash
   FS_TOOLS_DEMO_PAUSE=0.5 python fs_tools.py
   ```

   No LLM or API key required.

5. **Run tests (Part A)**

   ```bash
   python -m pytest tests/
   ```

   Prints each test name, outcome, and PASS/FAIL in the terminal (`pytest.ini` enables verbose output).

---

## Command reference

| What you want | Command |
|---------------|---------|
| **Interactive GPT-style chat over the file system** | `python llm_file_assistant.py --chat` |
| Single automated prompt (no chat) | `python llm_file_assistant.py` |
| File tools demo (no LLM) | `python fs_tools.py` |
| Slower Part A demo (recording) | `FS_TOOLS_DEMO_PAUSE=4 python fs_tools.py` |
| Tests | `python -m pytest tests/` |

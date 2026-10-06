# LLM-Powered File System

## Project brief

A small system that combines **file-system tools** (read, list, write, search, find path by name) with an **LLM assistant** that calls those tools from natural-language prompts. Use it to list directories, read PDF/TXT/DOCX resumes, search for keywords (including inside PDF/DOCX), write summary files, and resolve paths by name (e.g. “Read all resumes in the resumes folder”, “Find resumes mentioning Python experience”).

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

## How to run

1. **Create a virtualenv and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**

   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=sk-...
   ```

3. **Run the assistant**

   From the project root:

   **Terminal chat (ChatGPT-style):**

   ```bash
   python llm_file_assistant.py --chat
   ```

   Interactive multi-turn chat: type prompts (e.g. “List files in resumes”, “Find resumes mentioning Python”, “Create a summary file for resume_john_doe.pdf”). While the model thinks, you’ll see “Thinking…” and which tools are being called (e.g. “Calling: list_files, search_in_file”). Responses appear in panels. Type `exit` or `quit` to end.

   **Single prompt (no UI):**

   ```bash
   python llm_file_assistant.py
   ```

   Runs one built-in prompt (list resumes + search for Python). Edit the `prompt` in `if __name__ == "__main__"` to try other queries.

4. **Use the file tools alone (optional)**

   ```bash
   python fs_tools.py
   ```

   Lists files in `resumes/` and runs a sample keyword search. Useful to verify file I/O without the LLM.

5. **Run tests (Part A)**

   ```bash
   pytest tests/ -q
   ```

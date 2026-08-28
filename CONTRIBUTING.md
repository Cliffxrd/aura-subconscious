# Contributing to A.U.R.A.

Thank you for your interest in contributing to the **Agentic Unified Recollection Archive (AURA)**! We welcome contributions that help autonomous AI agents compound knowledge, preserve persistent identity, and eliminate stateless amnesia.

---

## 🌟 Ways to Contribute

1. **🧠 Universal Engineering Memories (`Extras/starter_memories/`)**:
   - Contribute sanitized, high-value engineering patterns (e.g. Compose UDF, KMP coroutine testing, backend optimizations).
   - Use our GitHub Issue template: `🧠 Universal Memory Contribution`.
2. **🌐 Platform Scrapers (`core/ingestion/`)**:
   - Add scrapers or format adapters for newly released AI coding platforms, IDEs, or ACP agents.
3. **🎭 Persona Blueprints (`Personas/`)**:
   - Create specialized subagent personas with unique cognitive traits, tools, and domain mandates.
4. **⚡ Core Architecture & Algorithms**:
   - Optimize the 4-6-8-8 Birthday Matrix cascade deduplication or HSL circular math.

---

## 🛠️ Local Development & Quality Gates

### 1. Setup Environment
```bash
git clone https://github.com/Cliffxrd/aura-subconscious.git
cd aura-subconscious
pip install -e .
```

### 2. Run Test Suite
All contributions must pass 100% of the unit test suite:
```bash
python -m unittest discover -s tests
```

### 3. Run Neuro-Architecture Health Check
```bash
python core/cli/main.py doctor
```

---

## 📜 Execution & Coding Standards (Zero Shortcuts)

AURA enforces strict engineering standards:
* **Zero Placeholders**: Never commit `// TODO`, empty `pass` blocks, or truncated code snippets.
* **3-Tier Casing Law**:
  * `ALL_CAPS.md` for root manifests (`AURA.md`, `SOUL.md`, `HEARTBEAT.md`, `THE_ORIGIN.md`).
  * `PascalCase.md` for human-edited context (`PersonalContext.md`, `RequestedMemories.md`, `Topics.md`).
  * `snake_case` for runtime files, memory artifacts (`memory_001.md`), and Python modules.
* **Pure Python Standard Library**: Core modules should avoid unnecessary third-party dependencies wherever possible.

---

## 🤝 Submitting a Pull Request

1. Fork the repository and create a feature branch (`git checkout -b feat/your-feature`).
2. Verify all tests and diagnostics pass (`python -m unittest discover -s tests`).
3. Open a Pull Request referencing the relevant Issue.
4. Fill out the PR Checklist completely.

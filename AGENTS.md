# Paper Reader Skill for arXiv

> **Version**: 1.0.0
> **Purpose**: Automated arXiv paper reading workflow with AI-powered analysis
> **Language**: All outputs in Chinese (中文)
> **Scope**: arXiv platform only

---

## Overview

This is an AI workflow configuration for reading and analyzing academic papers from arXiv. When you provide a paper title or arXiv ID, the AI agent will:

1. Locate the paper on arXiv
2. Download the LaTeX source code
3. Generate a comprehensive Chinese summary
4. Push everything to GitHub for backup
5. Support follow-up discussions based on the paper content

---

## Workflow Steps

### Step 1: Paper Identification

**Input**: User provides either:
- A paper title (e.g., "LLaDA2.0: Scaling Up Diffusion Language Models to 100B")
- An arXiv ID (e.g., "2512.15745")

**Action**:

If title is provided:
- Search the web for the paper on arXiv
- Extract the arXiv ID from the URL (e.g., `https://arxiv.org/abs/2512.15745` → ID is `2512.15745`)
- **If multiple results are found** (name collisions), STOP and ask the user to choose
- Confirm the found paper with the user before proceeding

If arXiv ID is provided:
- Validate the format (usually `XXXX.XXXXX` or `XXXX`)
- Proceed directly to Step 2

**Constraints**:
- Only process papers from arXiv platform
- Do NOT process other platforms (OpenReview, etc.)

---

### Step 2: Download LaTeX Source

**Source URL Pattern**: `https://arxiv.org/src/{arxiv_id}`

Example: `https://arxiv.org/src/2512.15745`

**Action**:
1. Create a `papers/` directory in the **repository root** if it doesn't exist
2. Inside `papers/`, create a directory named after the sanitized paper title (or `paper_<arxiv_id>`)
3. Inside the paper directory, create two subdirectories:
   - `src/` — for extracted LaTeX source files
   - `analysis_report/` — for all AI-generated documents
4. Download the LaTeX source using Python `requests` (NOT curl, as it may be blocked by security tools)
5. Extract the `.tar.gz` archive into the `src/` subdirectory

**Final Directory Structure**:
```
PaperRead/                                  # GitHub repo root
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── scripts/
│   └── download_arxiv.py                  # Python download helper
├── papers/                                # All papers go here
│   └── paper-title/                       # Named after paper (sanitized)
│       ├── src/                           # Extracted LaTeX source files
│       └── analysis_report/               # AI-generated documents
│           └── summary.md
└── .git/
```

**Sanitization Rules**:
- Remove/replace characters invalid for directory names: `/\:*?"<>|`
- Replace spaces with underscores or hyphens
- Keep the title readable

---

### Step 3: Generate Comprehensive Summary

**Input**: The extracted LaTeX source files (primarily `.tex` files)

**Action**:
1. Read and analyze the main `.tex` file(s)
2. Generate a detailed summary in **Chinese (中文)** covering:

   - **Background (背景)**: Research context and motivation
   - **Problem Statement (问题陈述)**: What problem does this paper solve?
   - **Key Innovations (核心创新)**: Main contributions and novel ideas
   - **Methodology (方法)**: Core methods, algorithms, and technical details
   - **Experiments (实验)**: Experimental setup, datasets, metrics, and results
   - **Conclusions (结论)**: Key findings and future work
   - **Personal Insights (个人见解)**: Critical analysis of strengths and limitations

3. Save the summary as a Markdown file in `analysis_report/summary.md`

**Output Requirements**:
- Language: Chinese (中文)
- Format: Markdown with clear headings
- Depth: Comprehensive but concise; aim for 1000-3000 words depending on paper complexity
- Include specific technical details, not just high-level descriptions
- Use formatting (lists, code blocks, tables) where appropriate

---

### Step 4: GitHub Backup

**Repository**: `https://github.com/CxsGhost/opencode-paper-reader-arxiv`

**Action**:
1. Stage the new paper directory and all generated files
2. Commit with a descriptive message (e.g., `Add paper: [Paper Title]`)
3. Push to GitHub using HTTPS

**Constraints**:
- Use HTTPS for remote operations
- Ensure `.gitignore` excludes large binary files and build artifacts

---

### Step 5: Follow-up Discussions

After the user reads the summary:

**Action**:
- Answer specific questions about the paper
- Reference the original LaTeX source when answering
- Generate additional analysis documents if requested (e.g., methodology deep-dive, comparison with other works)
- Save any new documents to `analysis_report/`

**Constraints**:
- Always base answers on the actual paper content
- If uncertain, re-read the relevant `.tex` sections
- Maintain Chinese language for all communications

---

## Prompt Template for Summary Generation

Use this structured prompt when generating the paper summary:

```
You are an expert academic paper analyst. Read the following LaTeX source of an arXiv paper and produce a comprehensive Chinese summary.

Paper Title: [TITLE]
ArXiv ID: [ID]

Please analyze the paper and generate a summary in Chinese containing:

1. **背景与动机**：这篇论文的研究背景是什么？为什么要做这项工作？
2. **问题定义**：论文试图解决什么具体问题？
3. **核心创新**：论文的主要贡献和创新点有哪些？
4. **方法论**：详细描述论文提出的方法、算法或模型架构。
5. **实验结果**：实验设置、数据集、评价指标和主要结果。
6. **结论与展望**：主要发现、局限性和未来工作方向。
7. **个人评价**：你对这篇论文的看法，包括优点和不足。

要求：
- 使用 Markdown 格式
- 包含具体的技术细节，不仅仅是泛泛而谈
- 对关键公式和算法进行解释
- 适当使用列表、表格和代码块增强可读性
- 字数：1000-3000 字（根据论文复杂度调整）
```

---

## File Structure Convention

```
PaperRead/                                  # GitHub repo root
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── scripts/
│   └── download_arxiv.py                  # Python download helper
├── papers/                                # All papers go here
│   └── paper-title/                       # Named after paper (sanitized)
│       ├── src/                           # Extracted LaTeX source files
│       └── analysis_report/               # AI-generated documents
│           ├── summary.md                 # Main comprehensive summary
│           └── [additional documents]     # Follow-up analysis, if any
└── .git/
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Paper not found on arXiv | Inform user, suggest checking the title or trying the arXiv ID directly |
| arXiv ID invalid | Inform user, ask for correction |
| Download fails (network) | Retry up to 3 times, then report failure |
| LaTeX source unavailable | Some papers only have PDF; inform user and offer to analyze PDF instead |
| Multiple papers with same title | List options and ask user to choose |
| GitHub push fails | Check credentials, report error, suggest manual push |

---

## Best Practices

1. **Always confirm**: Before downloading, confirm the identified paper with the user
2. **Read LaTeX, not PDF**: Prioritize `.tex` source files over PDF for better text extraction
3. **Preserve structure**: Maintain the paper's section structure in the summary
4. **Technical accuracy**: Ensure mathematical notation and algorithm descriptions are correct
5. **Chinese output**: All AI-generated content must be in Chinese
6. **Git hygiene**: Commit after each paper is processed; never mix multiple papers in one commit

---

## Usage Example

**User**: "帮我读一下 LLaDA2.0: Scaling Up Diffusion Language Models to 100B"

**Agent**:
1. Search arXiv for the title
2. Confirm: "找到论文：LLaDA2.0: Scaling Up Diffusion Language Models to 100B (arXiv:2512.15745)，是否正确？"
3. After confirmation, download source from `https://arxiv.org/src/2512.15745`
4. Create `papers/LLaDA2.0_Scaling_Up_Diffusion_Language_Models/` directory
5. Extract source to `papers/LLaDA2.0_Scaling_Up_Diffusion_Language_Models/src/`
6. Create `papers/LLaDA2.0_Scaling_Up_Diffusion_Language_Models/analysis_report/` subdirectory
7. Generate `summary.md` in Chinese inside `analysis_report/`
8. Git commit and push
9. Notify user: "论文分析完成！摘要已保存至 `papers/LLaDA2.0_Scaling_Up_Diffusion_Language_Models/analysis_report/summary.md` 并推送至 GitHub。"

**User**: "这个方法的核心公式是什么？"

**Agent**:
1. Re-read the relevant `.tex` sections
2. Answer in Chinese with precise formula references
3. Optionally generate a supplementary document in `analysis_report/`

---

## Notes

- This workflow is designed for arXiv papers with available LaTeX source
- For papers without LaTeX source, PDF parsing is a fallback (with reduced accuracy)
- The workflow prioritizes automation while maintaining user control at key decision points
- All generated content is in Chinese to serve Chinese-speaking researchers

# Paper Reader for Claude Code

> **Version**: 1.0.0
> **Purpose**: Automated arXiv paper reading workflow with AI-powered analysis
> **Language**: All outputs in Chinese (中文)

## Workflow

When a user provides a paper title or arXiv ID, follow these steps:

### 1. Identify Paper
- If title given: Search web for arXiv page, extract ID from URL (e.g., `2512.15745` from `https://arxiv.org/abs/2512.15745`)
- If multiple results found: Ask user to choose
- If ID given: Validate and proceed

### 2. Download Source
- URL: `https://arxiv.org/src/{arxiv_id}`
- Create directory named after sanitized paper title
- Extract `.tar.gz` into directory
- Create `analysis_report/` subdirectory

### 3. Generate Summary (Chinese)
Read LaTeX source and generate `analysis_report/summary.md` covering:
- 背景与动机
- 问题定义
- 核心创新
- 方法论
- 实验结果
- 结论与展望
- 个人评价

### 4. Push to GitHub
- Repo: `https://github.com/CxsGhost/opencode-paper-reader-arxiv`
- Use HTTPS
- Commit: `Add paper: [Title]`

### 5. Follow-up
- Answer questions based on paper content
- Generate additional docs in `analysis_report/` if needed
- Use Chinese for all outputs

## Key Constraints
- arXiv only
- HTTPS for Git
- Chinese output
- Confirm before downloading

# arXiv Paper Reader

一个跨平台的 AI 工作流项目，用于自动化阅读和分析 arXiv 论文。

## 特性

- 🔍 自动搜索并定位 arXiv 论文
- 📥 下载 LaTeX 源码（而非 PDF）
- 🧠 AI 生成详细的中文论文摘要
- 💾 GitHub 自动备份
- 💬 支持基于论文内容的深度讨论

## 快速开始

### 前提条件

- 支持 AI Agent 的代码编辑器（如 Claude Code、OpenCode 等）
- Git（用于推送到 GitHub）
- Python 3.x + requests（用于下载论文源码）

### 安装

1. 克隆此仓库：
```bash
git clone https://github.com/CxsGhost/opencode-paper-reader-arxiv.git
cd opencode-paper-reader-arxiv
```

2. 在您的 AI Agent 工具中加载工作流配置：
   - **Claude Code**: 项目根目录的 `CLAUDE.md` 会被自动读取
   - **OpenCode**: 使用 `AGENTS.md` 作为工作流定义

3. 确保可以访问 GitHub（使用 HTTPS）：
```bash
git remote -v
# 应显示: https://github.com/CxsGhost/opencode-paper-reader-arxiv.git
```

### 使用

直接告诉 AI Agent 您想读的论文：

```
帮我读一下论文：LLaDA2.0: Scaling Up Diffusion Language Models to 100B
```

或直接提供 arXiv 编号：

```
帮我读一下论文：arxiv 2512.15745
```

Agent 将自动完成以下流程：
1. 在 arXiv 上定位论文
2. 下载 LaTeX 源码
3. 生成中文详细摘要
4. 推送到 GitHub 备份
5. 等待您阅读后进一步提问

## 项目结构

```
opencode-paper-reader-arxiv/
├── AGENTS.md              # 主工作流定义（OpenCode 等）
├── CLAUDE.md              # Claude Code 兼容配置
├── README.md              # 本文件
├── scripts/
│   └── download_arxiv.py  # Python 下载辅助脚本
├── papers/                # 论文存放目录（自动生成）
│   └── paper-title/
│       ├── src/           # LaTeX 源码
│       └── analysis_report/
└── .gitignore             # Git 忽略配置
```

## 工作流详情

### 1. 论文识别
- 根据标题搜索 arXiv
- 或直接使用 arXiv ID
- 处理同名论文冲突（询问用户）

### 2. 下载源码
- 从 `https://arxiv.org/src/{id}` 使用 Python `requests` 下载 LaTeX 源码（避免 curl 被拦截）
- 解压到 `papers/{title}/src/`
- 创建 `papers/{title}/analysis_report/` 子目录

### 3. 生成摘要
AI 阅读 LaTeX 源码后，生成包含以下内容的中文摘要：
- 背景与动机
- 问题定义
- 核心创新
- 方法论
- 实验结果
- 结论与展望
- 个人评价

### 4. GitHub 备份
- 自动提交并推送到 GitHub
- 每篇论文独立提交

### 5. 后续讨论
- 基于论文内容回答问题
- 生成补充分析文档
- 所有内容保存在 `analysis_report/` 中

## 辅助脚本

### download_arxiv.py

用于手动下载 arXiv 论文源码（Python + requests，避免 curl 被拦截）：

```bash
# 下载到当前目录
python scripts/download_arxiv.py 2512.15745

# 下载到指定目录
python scripts/download_arxiv.py 2512.15745 ./papers
```

## 注意事项

- 仅支持 arXiv 平台（其他平台源码格式不确定）
- 所有 AI 生成的内容均为中文
- 使用 HTTPS 进行 Git 操作（无需 SSH 密钥配置）
- 某些论文可能没有 LaTeX 源码，此时会回退到 PDF 分析

## 兼容性

| 平台 | 配置文件 | 支持状态 |
|------|----------|----------|
| OpenCode | `AGENTS.md` | ✅ 完整支持 |
| Claude Code | `CLAUDE.md` | ✅ 完整支持 |
| Cursor | `CLAUDE.md` | ⚠️ 可能支持（需测试） |
| 其他 | `AGENTS.md` | ⚠️ 视具体实现而定 |

## 贡献

欢迎提交 Issue 或 PR 来改进此工作流！

## 许可证

MIT License

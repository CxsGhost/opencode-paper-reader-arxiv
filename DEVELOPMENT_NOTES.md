# Paper Reader arXiv - 研发笔记

> **版本**: 1.0.0
> **日期**: 2026-05-30
> **作者**: Sisyphus (AI辅助) / CxsGhost
> **目的**: 记录关键设计决策和踩坑经历，供未来迭代参考

---

## 一、项目性质：这不是CLI工具，而是AI工作流配置

### 初始设想 vs 最终形态

| 维度 | 方案A（CLI工具） | 方案B（AI工作流配置）✅ |
|------|-----------------|----------------------|
| 实现方式 | Python脚本，用户手动运行 | AGENTS.md + CLAUDE.md |
| 使用方式 | `python read_paper.py "题目"` | 对AI Agent说"帮我读这篇论文" |
| 跨平台 | 需要安装Python、配置API key | 任何支持Agent的编辑器直接可用 |
| 部署 | pip install 或 clone + setup | git clone 即用 |

**结论**: 选择了方案B。工作流简单到不需要一个独立的CLI工具，AI Agent本身就是执行引擎。

---

## 二、关键设计决策树

### 决策1：Git仓库位置（最大的坑）

**问题**: 论文下载后在哪里？怎么推送到GitHub？

| 阶段 | 布局 | 问题 |
|------|------|------|
| 初版 | `PaperRead/opencode-paper-reader-arxiv/.git/` | Git在子目录，论文在根目录，论文无法被Git管理 |
| 修正版A | `PaperRead/.git/` | 把Git上移，但配置文件还在 `opencode-xxx/` 子目录 |
| 修正版B | `PaperRead/.git/` + 配置文件全部在根目录 | ✅ 正确！工作目录=Git仓库=配置发现目录 |

**关键经验**:
- Agent 的工作目录 = 仓库根目录 = Git管理范围
- AGENTS.md 必须在根目录，否则Agent无法自动发现
- 论文文件必须与 `.git` 同级，才能被Git追踪

### 决策2：下载方式（curl → Python requests）

**问题**: curl被安全工具拦截

**演变**:
```bash
# v1: Shell + curl  ❌ 被拦截
curl -L -o archive.tar.gz "https://arxiv.org/src/2512.15745"

# v2: Python + requests ✅ 稳定可靠
python scripts/download_arxiv.py 2512.15745
```

**教训**: 在企业/安全敏感环境中，shell命令（curl、wget）容易被拦截，Python标准HTTP库更安全。虽然requests需要额外安装，但在Python生态中是事实标准。

### 决策3：论文目录结构（反复调整）

**演变过程**:

```
# v1: 直接放在根目录 ❌ 根目录越来越乱
PaperRead/
├── AGENTS.md
├── LLaDA2.0_xxx/          # 论文1
├── Another_Paper/          # 论文2
├── Yet_Another/           # 论文3
└── ...                   # 灾难

# v2: 放在papers/目录，但内容混杂 ❌ 源码和报告混在一起
PaperRead/
├── AGENTS.md
└── papers/
    └── LLaDA2.0_xxx/
        ├── main.tex       # 源码
        ├── doc/
        ├── images/
        └── summary.md     # 报告混在一起

# v3: papers/ + src/ + analysis_report/ ✅ 最终方案
PaperRead/
├── AGENTS.md
└── papers/
    └── LLaDA2.0_xxx/
        ├── src/              # 源码隔离
        │   ├── main.tex
        │   └── ...
        └── analysis_report/  # AI报告独立
            └── summary.md
```

**设计原则**:
- 论文不能与项目配置混在一起
- 源码和AI生成的报告必须分离，一眼可辨识
- `analysis_report/` 作为未来追问和深度分析的容器

### 决策4：AGENTS.md vs CLAUDE.md

| 文件 | 用途 | 目标平台 |
|------|------|---------|
| AGENTS.md | 详细工作流定义、prompt模板、错误处理 | OpenCode 等通用Agent平台 |
| CLAUDE.md | 精简版工作流程（5步） | Claude Code |

**策略**: 双文件覆盖，不放弃任何平台。AGENTS.md是主文档，CLAUDE.md是Claude的精简适配。

---

## 三、踩坑记录（按时间线）

### 坑1：嵌套目录 Git 初始化
- **现象**: 第一次 `git init` 在 `opencode-paper-reader-arxiv/` 子目录
- **后果**: 根目录 `PaperRead/` 下的文件不受Git管理，论文无法备份
- **修复**: 删除 `.git`，在根目录重新 `git init`

### 坑2：配置文件藏在子目录
- **现象**: AGENTS.md 在 `opencode-paper-reader-arxiv/AGENTS.md`
- **后果**: Agent 在工作目录（根）找不到配置，工作流不生效
- **修复**: 将 AGENTS.md、CLAUDE.md 移动到根目录

### 坑3：curl 被拦截
- **发现者**: 用户（CxsGhost），实际测试时发现
- **后果**: 下载arXiv源码失败，工作流中断
- **修复**: 用 Python requests 替代 curl

### 坑4：论文文件夹命名不规范
- **现象**: 第一次测试时论文名用了原始标题，包含冒号等字符
- **后果**: 文件系统不友好，跨平台兼容性差
- **修复**: 在脚本中添加 `sanitize_dirname()` 函数，替换 `/\:*?"<>|` 等非法字符

### 坑5：tar.gz 解压后残留
- **现象**: `source.tar.gz` 留在论文目录中
- **后果**: git 会追踪这个冗余文件，浪费空间和带宽
- **修复**: 解压后立即 `os.remove(archive_path)`

---

## 四、文件清单与职责

| 文件/目录 | 职责 | 关键属性 |
|----------|------|---------|
| `AGENTS.md` | OpenCode主工作流定义 | 必须放在仓库根，Agent自动读取 |
| `CLAUDE.md` | Claude Code精简配置 | 必须放在根，Claude启动时加载 |
| `README.md` | 项目说明、安装指南 | 面向用户的中文文档 |
| `.gitignore` | 忽略LaTeX编译产物、压缩包 | 根目录级，全局生效 |
| `scripts/download_arxiv.py` | Python下载辅助脚本 | requests-based，可独立运行 |
| `papers/` | 所有论文的存放目录 | 自动创建，论文分目录存放 |

---

## 五、工作流程的精确描述（给AI读取）

1. **识别**: 用户给标题 → 网络搜索 → 提取arXiv ID；用户给ID → 直接验证
2. **确认**: 展示论文信息，用户确认后再继续
3. **创建目录**: `papers/{sanitized_title}/`，内部预建 `src/` 和 `analysis_report/`
4. **下载**: Python requests 从 `https://arxiv.org/src/{id}` 下载 tar.gz
5. **解压**: `tarfile` 解压到 `papers/{title}/src/`，删除原始压缩包
6. **阅读摘要**: 读取 `.tex` 源码，用结构化prompt生成中文摘要
7. **保存**: 摘要写入 `papers/{title}/analysis_report/summary.md`
8. **提交**: `git add papers/{title}/ && git commit -m "Add paper: {title}" && git push`
9. **待命**: 等待用户基于摘要提问，AI引用 `.tex` 原文回答

---

## 六、未来迭代方向

| 方向 | 可能性 | 优先级 |
|------|--------|--------|
| PDF fallback | 某些论文无LaTeX源码 | 高（用户提到） |
| 论文去重 | 避免重复下载 | 中 |
| 批量处理 | 一次读多篇论文 | 低 |
| 标签/分类 | 给论文打标签 | 低 |
| 论文间对比 | 多篇论文横向分析 | 待定 |
| arXiv API | 用API而非页面搜索查ID | 中 |

---

## 七、关键代码片段备忘

### 1. Python下载 + 解压
```python
import requests
import tarfile
import os

response = requests.get(f"https://arxiv.org/src/{arxiv_id}")
with open(f"arxiv_{arxiv_id}.tar.gz", "wb") as f:
    f.write(response.content)

with tarfile.open(f"arxiv_{arxiv_id}.tar.gz", "r:gz") as tar:
    tar.extractall(path=src_dir)

os.remove(f"arxiv_{arxiv_id}.tar.gz")  # 清理残留
```

### 2. 目录名清洗
```python
import re

def sanitize_dirname(name):
    sanitized = re.sub(r'[\\/*?:"<>|]', ' ', name)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized.replace(' ', '-')
```

### 3. 完整目录创建
```python
import os

paper_dir = os.path.join("papers", sanitize_dirname(title))
src_dir = os.path.join(paper_dir, "src")
report_dir = os.path.join(paper_dir, "analysis_report")

os.makedirs(src_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)
```

---

## 八、Git提交策略

- **每篇论文独立commit**: `Add paper: [Title]`
- **工作流变更单独commit**: 如 `Refactor: Use Python requests`
- **结构重组单独commit**: 如 `Restructure: Move config to root`
- **论文文件夹进Git**: 源码和摘要都追踪，但 `.gitignore` 排除 `*.tar.gz`、`*.aux`、`.DS_Store` 等

---

## 九、兼容性说明

| 平台 | 兼容文件 | 状态 |
|------|---------|------|
| OpenCode | `AGENTS.md` | ✅ 完整支持 |
| Claude Code | `CLAUDE.md` + `AGENTS.md` | ✅ 完整支持 |
| Cursor | `CLAUDE.md` | ⚠️ 未测试，但格式类似 |
| 其他Agent | `AGENTS.md` | ⚠️ 取决于是否支持markdown工作流定义 |

---

## 十、开发者笔记

###  Repositories 地址
`https://github.com/CxsGhost/opencode-paper-reader-arxiv`

### 本地路径（开发时）
`/Users/cxsghost/Desktop/PaperRead/`

### 使用HTTPS而非SSH
- 简化跨设备配置，无需管理SSH密钥
- 缺点：每次push可能需要输入密码（取决于Git凭证管理器配置）

### 核心不变量
1. 仓库根目录 = Agent工作目录 = Git管理范围
2. `papers/` 是所有论文的唯一入口
3. 每篇论文内部必须是 `src/` + `analysis_report/` 结构
4. 所有AI输出必须中文
5. 下载用Python requests，不用curl/wget

---

> 这份文档的价值在于记录"为什么这样设计"，而不仅仅是"做了什么"。当三个月后回头看时，能迅速理解当时的选择逻辑，避免重复踩坑。

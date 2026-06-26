# Codex Skills Share Temp

这是一个临时公开仓库，用来给学员分享讲师实战在用的 Codex Skill 的脱敏版。

这些 Skill 已经移除个人账号、本机路径、Cookie、API Key、云盘目录和私有项目名称。仓库只保留可复用的工作流、配置入口和安全边界。

## 包含的 Skill

- `cdp-browser-reuse`：复用已登录浏览器，不重复登录网站。
- `google-flow-generate`：通过 Google Flow 生成概念图、风格图和沟通图。
- `chatgpt-image`：通过 ChatGPT 网页端生成图片。
- `x-to-obsidian`：把 X/Twitter 链接整理成 Obsidian 笔记。
- `media-to-obsidian`：把视频或音频转录、总结并保存到 Obsidian。
- `pdf-typeset`：把结构化内容排版成 A4 PDF。
- `seedance-video`：通过 Seedance 2.0 API 生成视频，支持 dry-run 调试。

## 一键安装

Windows PowerShell：

```powershell
.\install.ps1
```

macOS / Linux：

```bash
bash install.sh
```

默认会复制到：

- Codex：`~/.codex/skills`
- Claude Code：`~/.claude/skills`

如需指定目录：

```powershell
.\install.ps1 -CodexDir "$HOME\.codex\skills" -ClaudeDir "$HOME\.claude\skills"
```

```bash
CODEX_SKILLS_DIR="$HOME/.codex/skills" CLAUDE_SKILLS_DIR="$HOME/.claude/skills" bash install.sh
```

## 使用前配置

这些 Skill 不内置任何账号或密钥。需要登录态的网站，请先在你自己的浏览器中登录。

推荐环境变量：

```bash
OBSIDIAN_VAULT="/path/to/your/ObsidianVault"
X_AUTH_TOKEN="your_x_auth_token"
X_CT0="your_x_ct0"
```

Windows PowerShell 示例：

```powershell
$env:OBSIDIAN_VAULT="$HOME\Documents\ObsidianVault"
$env:X_AUTH_TOKEN="your_x_auth_token"
$env:X_CT0="your_x_ct0"
```

## 安全说明

不要把下面这些文件提交到公开仓库：

- `cookies.json`
- `api-keys.json`
- `.env`
- `*.cookies.txt`
- `config.json`
- 任何包含邮箱、Token、Cookie、客户资料或本机绝对路径的文件

这个仓库是课堂临时分享用，用完可以删除。

# GitHub 创意项目展台

快速把 GitHub 项目整理成可视化、可分类的卡片式作品集。

它面向 AI 产品、AI 业务及其他需要展示实践能力的同学，适合在面试现场通过一个链接，向面试官集中呈现自己的创意、项目价值与落地成果。无需额外服务，生成后可通过 GitHub Pages 长期维护。

## 它能做什么

- 读取任意用户的公开 GitHub 项目；
- 根据项目描述、README 和必要代码理解项目价值；
- 生成项目名称、一句话价值和投产价值；
- 自动建议分类，也允许每位用户定义自己的分类体系；
- 生成笔记本标签式导航和项目卡片；
- 发布到 GitHub Pages，不依赖额外后端；
- 增量更新项目，同时保留用户人工确认过的文案。

## 安全与可信原则

- 只读取和展示公开仓库；
- 私有仓库信息不会进入草稿、日志或页面；
- 没有证据时不编造金额、比例、用户量等量化收益；
- 自动更新不会覆盖人工确认的分类和文案；
- 写入 GitHub 和发布 Pages 前必须展示变更并获得确认。

## 安装 Skill

将 [`skills/publish-github-project-page`](skills/publish-github-project-page) 文件夹复制到你的 Codex Skills 目录，或让 Codex 从本仓库安装该 Skill。

调用示例：

```text
使用 $publish-github-project-page，把我的 GitHub 公开项目生成卡片式主页并发布。
```

只需要提供 GitHub 用户名或主页地址。分类、语言、标题、主题色和仓库范围均为可选项。

## 生成流程

1. 获取公开仓库并提出默认排除项；
2. 分析项目依据，生成分类和价值文案草稿；
3. 用户统一确认仓库、分类和文案；
4. 生成纯 HTML、CSS 和 JavaScript 静态站点；
5. 列出 GitHub 远程变更并请求最终确认；
6. 发布 GitHub Pages 并返回网址。

## 仓库结构

```text
skills/publish-github-project-page/
├── SKILL.md
├── agents/openai.yaml
├── scripts/project_page.py
├── references/project-data.md
├── assets/site-template/
└── tests/
```

## 验证

```bash
python3 -m unittest discover -s skills/publish-github-project-page/tests -v
python3 skills/publish-github-project-page/scripts/project_page.py validate --data projects.json
```

## License

MIT

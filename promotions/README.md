# 推广素材包

复制对应文件内容，到各平台发布。

## 平台与文件

| 平台 | 文件 | 操作 |
|------|------|------|
| 知乎 | 知乎-技术文章.md | 新建文章，粘贴内容，可适当配图 |
| 掘金 | 掘金-短文.md | 新建文章，粘贴 |
| Hacker News | HackerNews-ShowHN.txt | 打开 news.ycombinator.com/submit，选 "Show"，粘贴标题+URL；正文可发在评论区 |
| Reddit | Reddit-post.txt | 发到 r/MachineLearning 或 r/Python |
| Twitter/X | Twitter-推文.txt | 发推，可加 #LLM #Agent |
| V2EX | V2EX-分享.txt | 创意/分享节点发帖 |

## Hacker News 提交

1. 打开 https://news.ycombinator.com/submit
2. Title: `Show HN: Code-as-Orchestration Agent – ~50 lines, no JSON, no DAG`
3. URL: `https://github.com/wenduntang/push-u`
4. 可选：在评论区补充 HackerNews-ShowHN.txt 的正文

## Hugging Face Spaces 部署

1. 登录 https://huggingface.co
2. 进入 https://huggingface.co/new-space
3. Space 名称：`push-u-demo`
4. SDK：Streamlit
5. 选择 "Clone from a repo"，填入 `wenduntang/push-u`
6. 或手动上传：app.py、code_executor.py、requirements.txt
7. 创建后等待构建，获得公开 URL

## 发布顺序建议

1. Hugging Face Spaces（先有在线 Demo）
2. 知乎 / 掘金（中文技术文章）
3. Hacker News（国际曝光）
4. V2EX、Reddit、Twitter（按需）

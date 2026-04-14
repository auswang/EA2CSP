# EA2CSP - Azure 资源跨订阅迁移可行性分析工具

> **E**valuate **A**zure resources **2** (to) **C**ross-**S**ubscription **P**ortability

快速查询您 Azure 订阅中的资源是否支持跨订阅 / 跨资源组迁移。

## ✨ 功能特性

- **Microsoft 账号登录** — 基于 MSAL.js (SPA) 弹窗认证，无需后端存储密钥
- **订阅选择** — 自动列出当前账号可访问的所有 Azure 订阅
- **资源迁移评估** — 获取订阅内所有资源，逐一分析跨资源组/跨订阅迁移能力
- **内置资源数据库** — 包含 500+ Azure 资源类型的迁移支持数据（来源：[Microsoft 官方文档](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/move-support-resources)）
- **筛选与搜索** — 支持按资源名称/类型搜索，按迁移状态和资源组筛选
- **CSV 导出** — 一键导出分析报告
- **可调列宽** — 表格列宽支持拖拽调整
- **多语言 (i18n)** — 简体中文 / 繁體中文 / English / 日本語 / Français

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.12 · Flask 3.1 · Gunicorn |
| 前端 | MSAL.js 2.38 (SPA) · Bootstrap 5.3 · Bootstrap Icons |
| 认证 | Azure AD App Registration (SPA, 无 Client Secret) |
| 部署 | Azure Web App (Linux, F1 Free Tier) |

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Azure AD 应用注册（SPA 重定向 URI）

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/auswang/EA2CSP.git
cd EA2CSP

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 Azure AD 应用信息

# 启动
python app.py
```

浏览器访问 `http://localhost:8000`

### 环境变量

| 变量 | 说明 |
|------|------|
| `AZURE_CLIENT_ID` | Azure AD 应用的 Client ID |
| `AZURE_TENANT_ID` | 租户 ID（默认 `common` 支持多租户） |
| `AUSTIN_TENANT` | 可选，特定租户 ID（用于快捷登录） |

## ☁️ 部署到 Azure

```bash
# 创建资源组与 Web App
az group create --name rg-ea2csp --location eastasia
az appservice plan create --name plan-ea2csp --resource-group rg-ea2csp --sku F1 --is-linux
az webapp create --name ea2csp --resource-group rg-ea2csp --plan plan-ea2csp --runtime "PYTHON:3.12"

# 配置应用设置
az webapp config appsettings set --name ea2csp --resource-group rg-ea2csp \
  --settings AZURE_CLIENT_ID=<your-client-id> AZURE_TENANT_ID=<your-tenant-id>

# 启用 HTTPS
az webapp update --name ea2csp --resource-group rg-ea2csp --https-only true

# 部署代码
zip -r /tmp/ea2csp-deploy.zip . -x ".env*" "__pycache__/*" ".git/*" ".venv/*" "venv/*"
az webapp deploy --name ea2csp --resource-group rg-ea2csp --src-path /tmp/ea2csp-deploy.zip --type zip
```

## 📁 项目结构

```
EA2CSP/
├── app.py                  # Flask 后端主程序
├── move_support_data.py    # 500+ Azure 资源类型迁移支持数据
├── templates/
│   └── index.html          # 单页应用（SPA）前端
├── requirements.txt        # Python 依赖
├── startup.sh              # Gunicorn 启动脚本
├── .env.example            # 环境变量示例
└── .gitignore
```

## 📖 数据来源

资源迁移支持数据来自：
- [Azure 资源迁移支持文档](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/move-support-resources)
- [tfitzmac/resource-capabilities](https://github.com/tfitzmac/resource-capabilities/blob/master/move-support-resources.csv)

## 📝 License

MIT

---

*Vibe coding by GitHub Copilot* 🐾

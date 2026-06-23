# docker-tools

Sub-repo chứa public base images cho **QuanLyCongViec**.

## 📦 Public Images

| Image | Tag | Mô tả |
|-------|-----|-------|
| `ghcr.io/tannhatcms/docker-tools` | `qlcv-web-base-deps-{hash}` | Pre-built pnpm + workspace deps |
| `ghcr.io/tannhatcms/docker-tools` | `qlcv-web-base-latest` | Pointer tới base mới nhất |

## 🚀 Quick Start

```bash
# Pull base
docker pull ghcr.io/tannhatcms/docker-tools:qlcv-web-base-latest

# Build full web image dùng base
docker build -f docker/nextjs/Dockerfile \
  --build-arg BASE_IMAGE=ghcr.io/tannhatcms/docker-tools:qlcv-web-base-latest \
  -t qlcv-web:dev .
```

## 🔧 Workflows

| Workflow | Trigger | Output |
|----------|---------|--------|
| `.github/workflows/docker-tools.yml` | push to `main` (deps changed) hoặc manual | base image → `docker-tools` package |
| `.github/workflows/docker-publish-web.yml` | push to `main` (version changed) hoặc manual | web image → `quan-ly-cong-viec-web` (pulls base từ `docker-tools`) |

## 📝 Tại sao tách riêng?

- **Public** base → share được cho fork/contributor.
- **Cache reuse** cross-repo.
- **Tách triggers:** deps đổi → rebuild base. Source đổi → rebuild web.

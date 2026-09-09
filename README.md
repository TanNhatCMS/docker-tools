# docker-tools

Sub-repo chứa các workflow build & publish Docker images cho **QuanLyCongViec** lên GHCR
(`ghcr.io/tannhatcms/*`). Main repo chỉ gửi `repository_dispatch` kèm payload đã mã hoá;
build thực tế chạy tại đây (dùng secrets `MAIN_REPO_CHECKOUT_TOKEN`, `PAYLOAD_ENCRYPTION_KEY`).

## 🔧 Workflows

| Workflow                         | Trigger                             | Output                                                        |
| -------------------------------- | ----------------------------------- | ------------------------------------------------------------- |
| `publish-docker-web.yml`         | `repository_dispatch` (web)         | `qlcv-web` — build all-in-one (deps → builder → nginx runner) |
| `publish-docker-api.yml`         | `repository_dispatch` (api)         | `qlcv-api`                                                    |
| `publish-docker-api-base.yml`    | `repository_dispatch` (api-base)    | `qlcv-api-base` (NuGet restore cache)                         |
| `publish-docker-api-runtime.yml` | `repository_dispatch` (api-runtime) | `qlcv-api-runtime-base`                                       |
| `publish-docker-nginx.yml`       | `repository_dispatch` (nginx)       | `qlcv-nginx`                                                  |
| `publish-docker-migrator.yml`    | `repository_dispatch` (migrator)    | `qlcv-db-migrator`                                            |

## 🌐 Web — all-in-one

Web build gộp trong **một** workflow + **một** Dockerfile (`docker/nextjs/Dockerfile`
ở main repo): stage `deps` (pnpm install) → `builder` (Next.js static export) →
`runner` (nginx). Không còn image trung gian `qlcv-web-base` / `qlcv-web-runtime-base`.

- Base: `node:26-bookworm-slim` (+ `libatomic1` — node 26 cần libatomic để chạy lifecycle scripts).
- Layer deps được cache qua registry tag `qlcv-web:buildcache[-lane]` + gha cache:
  chỉ `pnpm install` lại khi `pnpm-lock.yaml` đổi.

```bash
# Build local tương đương
docker buildx build -f docker/nextjs/Dockerfile -t qlcv-web:dev .
```

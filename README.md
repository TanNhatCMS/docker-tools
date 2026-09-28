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
| `test-dotnet.yml`                | `repository_dispatch` (test-api)    | .NET build & test + coverage → comment PR                     |
| `test-web.yml`                   | `repository_dispatch` (test-web)    | Inline styles + Vitest coverage → comment PR                  |
| `test-database.yml`              | `repository_dispatch` (test-db)     | Prisma migrate + seed trên MariaDB → comment PR               |
| `test-desktop.yml`               | `repository_dispatch` (test-app)    | Tauri UI build + cargo llvm-cov → comment PR                  |

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

## 🧪 Test workflows

Main repo (`test-*.yml`) gửi `repository_dispatch` với payload:

| Field              | Ý nghĩa                                                                 |
| ------------------ | ----------------------------------------------------------------------- |
| `sha` / `branch`   | Commit/nhánh cần test (checkout kèm submodules)                          |
| `pr_number`        | PR để comment kết quả (rỗng → không comment)                             |
| `dispatch_id`      | Đưa vào `run-name` để main repo tìm đúng run và chờ kết quả              |
| `caller_run_url`   | Link run phía main repo, hiện ở cuối comment                             |
| `comment_id`       | Comment lệnh `$test-*` (qua ci-dispatcher) → thả 👍/👎 khi test kết thúc |
| `coverage_gist_id` | Chỉ gửi khi chạy trên `main` → cập nhật badge coverage (cần `GIST_TOKEN`) |

Sau khi test xong (kể cả khi fail), workflow comment sticky vào PR của `TanNhatCMS/QuanLyCongViec`
(bảng kết quả từng bước + coverage nếu có) và set commit status tương ứng.
Nếu lệnh đến từ comment `$test-*`, workflow thả 👍 (pass) / 👎 (fail) vào chính comment đó
(main repo chỉ thả 👀 khi nhận lệnh và 🚀 khi đã gửi dispatch, không đứng chờ kết quả).

Secrets dùng: `MAIN_REPO_CHECKOUT_TOKEN` (checkout + mặc định dùng để comment/status),
`MAIN_REPO_PR_TOKEN` (tùy chọn — token riêng có quyền `pull-requests`/`statuses: write` trên main repo),
`GIST_TOKEN` (tùy chọn — badge coverage).

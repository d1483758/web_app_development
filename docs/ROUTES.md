# API 路由與頁面設計 (Routes)

本文件根據 PRD、FLOWCHART 與架構需求，將所有的 Flask 路由依模組切分為多支 Blueprint，並規畫對應的 HTTP 方法、輸入輸出與 Jinja2 模板對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (食譜列表) | GET | `/` | `index.html` | 顯示最新上架的食譜列表 |
| 搜尋結果 | GET | `/search` | `index.html` | 帶有查詢字串參數 `?q=` 返回過濾後的名單 |
| 註冊頁面/送出 | GET, POST | `/register` | `auth.html` | GET 顯示表單，POST 處理 DB 寫入與 Session |
| 登入頁面/送出 | GET, POST | `/login` | `auth.html` | GET 顯示表單，POST 檢查憑證並儲存 Session |
| 登出 | GET, POST | `/logout` | — | 清除 Session 後跳回首頁 (重導向) |
| 個人與收藏主頁 | GET | `/profile` | `profile.html` | 列出我的收藏食譜與自己發布的食譜 |
| 單篇食譜詳細檢視 | GET | `/recipe/<int:recipe_id>` | `recipe.html` | 印出完整食譜與關聯材料、步驟 |
| 新增食譜頁/送出 | GET, POST | `/recipe/new` | `edit_recipe.html` | GET 顯示空白表單，POST 新增 Recipe |
| 編輯食譜頁/送出 | GET, POST | `/recipe/<int:recipe_id>/edit`| `edit_recipe.html` | GET 帶入舊資料，POST 局部更新 |
| 刪除自己發布的食譜 | POST | `/recipe/<int:recipe_id>/delete`| — | 刪除資源、並重導向個人主頁 |
| 收藏或取消收藏食譜 | POST | `/recipe/<int:recipe_id>/favorite`| — | 若無則加、若有則移除，重新整理頁面 |
| 管理員儀表板 | GET | `/admin` | `admin.html` | 檢視包含使用者與所有內容的統整數據 |
| 管理員下架食譜 | POST | `/admin/recipe/<int:recipe_id>/delete`| — | 管理權限強制刪除內容 |
| 管理員停權使用者 | POST | `/admin/user/<int:user_id>/ban`| — | 管理員將使用者狀態切換為停權 |

---

## 2. 路由詳細說明

### Main Router (`app/routes/main.py`)
- **GET `/`**：
  - 輸入：無
  - 處理邏輯：查詢 `Recipe.get_all()` 或做適當的分頁，傳遞給 Template。
  - 輸出：渲染 `index.html`。
- **GET `/search`**：
  - 輸入：URL 參數 `?q=` (Keyword)。
  - 處理邏輯：利用 SQLAlchemy 的 `ilike` 功能過濾名稱中符合 `q` 的 Recipe。
  - 輸出：將資料清單餵給 `index.html` 渲染。

### Auth Router (`app/routes/auth.py`)
- **GET/POST `/register`**：
  - 輸入：表單包含 `username`, `email`, `password`。
  - 處理邏輯：呼叫 `User.create`，並且實作雜湊。已有該 email 則報錯。
  - 輸出：GET 呈現註冊表單，POST 成功後跳至 Login。
- **GET/POST `/login`**：
  - 輸入：表單傳回 `email`, `password`。
  - 處理邏輯：由 `User.query.filter_by(email)` 查出，校驗密碼後在 Session 裡指定 `user_id`。
  - 輸出：成功一律 Redirect 到 `/`。
- **GET/POST `/logout`**：
  - 輸入：無
  - 處理邏輯：呼叫 `session.pop('user_id', None)`，執行登出。
  - 輸出：重導向至 GET `/`。
- **GET `/profile`**：
  - 輸入：Session 內的 `user_id`
  - 處理邏輯：查出並傳回 `user.recipes` 與 `user.favorites`。
  - 輸出：渲染 `profile.html`。

### Recipe Router (`app/routes/recipe.py`)
- **GET `/recipe/<id>`**：
  - 輸入：`recipe_id`
  - 處理邏輯：`Recipe.query.get_or_404(recipe_id)`，這會自帶材料與步驟的資料屬性。
  - 輸出：渲染單獨的 `recipe.html`。
- **GET/POST `/recipe/new`**：
  - 輸入：表單資料包含了多組的 materials, steps 陣列。
  - 處理邏輯：先 `Recipe.create()` 產生 Recipe 去拿到 ID，再迭代新建多組 Ingredient 與 Step 綁定至該食譜。
  - 輸出：重導向去展示該篇建立好後的新 `GET /recipe/<id>` 介面。
- **GET/POST `/recipe/<id>/edit`**：
  - 輸入與邏輯：必須檢查 session `user_id` == `recipe.user_id` 確保非越權更動。
- **POST `/recipe/<id>/delete`**：
  - 同樣檢查所有者權限，確認為自己或 Admin 後針對該篇 `recipe.delete()`。
- **POST `/recipe/<id>/favorite`**：
  - 搜尋 `Favorite.query` 中該使用者對該篇是否已點過。沒有就呼叫 `Favorite.create()`，有就呼叫 `.delete()`。

### Admin Router (`app/routes/admin.py`)
- 包含三個路由：`/admin`、`/admin/recipe/<id>/delete`、`/admin/user/<id>/ban`。
- 皆須實作與確認 `current_user.is_admin == True` 否則退回 `403 Forbidden`。

---

## 3. Jinja2 模板清單

所有的模板檔案會建立在 `app/templates` 底下：
1. **`base.html`**：基礎共用版型。定義 `{% block content %}`、導覽列(包含登入狀態判定邏輯)與 Flash 訊息區格。
2. **`index.html`**：首頁/列表模板，繼承自 `base.html`。
3. **`auth.html`**：註冊與登入共用的表單，繼承自 `base.html`。
4. **`profile.html`**：個人檔案/收藏清單分區展示，繼承自 `base.html`。
5. **`recipe.html`**：單獨食譜的詳情頁，繼承自 `base.html`。
6. **`edit_recipe.html`**：新增、編輯食譜用的複雜表單（含有動態新增材料列的操作）。
7. **`admin.html`**：管理員儀表板，繼承自 `base.html`。

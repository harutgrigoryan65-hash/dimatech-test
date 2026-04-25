from __future__ import annotations


INDEX_HTML = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dimatech Payment API</title>
  <style>
    :root {
      --bg: #f4f5f2;
      --surface: #ffffff;
      --surface-2: #eef1ea;
      --text: #1d2420;
      --muted: #667069;
      --line: #d9ddd4;
      --accent: #166b5b;
      --accent-2: #9a5728;
      --danger: #a23b3b;
      --ok: #23764f;
      --shadow: 0 14px 34px rgba(35, 43, 38, 0.09);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 15px;
      line-height: 1.45;
    }

    header {
      border-bottom: 1px solid var(--line);
      background: var(--surface);
    }

    .wrap {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }

    .topbar {
      min-height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .mark {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background: var(--accent);
      display: grid;
      place-items: center;
      color: #fff;
      font-weight: 800;
      font-size: 18px;
    }

    h1, h2, h3, p { margin: 0; }

    h1 { font-size: 20px; font-weight: 750; }
    h2 { font-size: 17px; font-weight: 740; }
    h3 { font-size: 14px; font-weight: 700; }

    .subtitle { color: var(--muted); font-size: 13px; margin-top: 3px; }

    .status-line {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
    }

    .dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--accent-2);
      display: inline-block;
    }

    .dot.ok { background: var(--ok); }

    main {
      padding: 24px 0 36px;
    }

    .grid {
      display: grid;
      grid-template-columns: minmax(280px, 360px) 1fr;
      gap: 18px;
      align-items: start;
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .panel-head {
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfa;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .panel-body { padding: 18px; }

    .stack { display: grid; gap: 14px; }
    .stack-sm { display: grid; gap: 10px; }

    .tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 3px;
      gap: 3px;
    }

    .tab {
      border: 0;
      border-radius: 6px;
      background: transparent;
      color: var(--muted);
      min-height: 36px;
      font: inherit;
      cursor: pointer;
    }

    .tab.active {
      background: var(--surface);
      color: var(--text);
      box-shadow: 0 1px 4px rgba(35, 43, 38, 0.1);
    }

    label {
      display: grid;
      gap: 6px;
      color: var(--muted);
      font-size: 13px;
    }

    input {
      width: 100%;
      height: 39px;
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 0 11px;
      color: var(--text);
      background: #fff;
      font: inherit;
    }

    input:focus {
      outline: 2px solid rgba(22, 107, 91, 0.18);
      border-color: var(--accent);
    }

    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    button {
      min-height: 39px;
      border: 1px solid transparent;
      border-radius: 7px;
      padding: 0 13px;
      font: inherit;
      font-weight: 650;
      cursor: pointer;
      background: var(--accent);
      color: white;
    }

    button.secondary {
      background: var(--surface);
      color: var(--text);
      border-color: var(--line);
    }

    button.warn { background: var(--accent-2); }
    button:disabled { opacity: 0.55; cursor: not-allowed; }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .workspace {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }

    .wide { grid-column: 1 / -1; }

    .data {
      min-height: 104px;
      border-radius: 8px;
      background: #161b18;
      color: #edf2ed;
      padding: 13px;
      overflow: auto;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      white-space: pre-wrap;
    }

    .list {
      display: grid;
      gap: 8px;
    }

    .item {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fff;
      display: grid;
      gap: 4px;
    }

    .item strong { font-size: 14px; }
    .item span { color: var(--muted); font-size: 13px; }

    .message {
      min-height: 22px;
      font-size: 13px;
      color: var(--muted);
    }

    .message.ok { color: var(--ok); }
    .message.err { color: var(--danger); }

    @media (max-width: 900px) {
      .grid, .workspace, .row {
        grid-template-columns: 1fr;
      }

      .topbar {
        align-items: flex-start;
        flex-direction: column;
        padding: 16px 0;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap topbar">
      <div class="brand">
        <div class="mark">D</div>
        <div>
          <h1>Dimatech Payment API</h1>
          <p class="subtitle">REST backend demo</p>
        </div>
      </div>
      <div class="status-line"><span id="healthDot" class="dot"></span><span id="healthText">checking localhost:3993</span></div>
    </div>
  </header>

  <main class="wrap">
    <div class="grid">
      <section class="panel">
        <div class="panel-head">
          <h2>Session</h2>
          <button class="secondary" id="logoutBtn">Logout</button>
        </div>
        <div class="panel-body stack">
          <div class="tabs">
            <button class="tab active" data-role="user">User</button>
            <button class="tab" data-role="admin">Admin</button>
          </div>
          <label>Email<input id="email" type="email" autocomplete="username" value="user@example.com"></label>
          <label>Password<input id="password" type="password" autocomplete="current-password" value="user12345"></label>
          <button id="loginBtn">Login</button>
          <div id="loginMessage" class="message"></div>
          <div class="data" id="sessionBox">{}</div>
        </div>
      </section>

      <section class="workspace">
        <section class="panel">
          <div class="panel-head">
            <h2>User</h2>
            <button class="secondary" id="refreshUserBtn">Refresh</button>
          </div>
          <div class="panel-body stack">
            <div class="actions">
              <button class="secondary" id="loadMeBtn">Me</button>
              <button class="secondary" id="loadAccountsBtn">Accounts</button>
              <button class="secondary" id="loadPaymentsBtn">Payments</button>
            </div>
            <div id="userList" class="list"></div>
            <div class="data" id="userBox">{}</div>
          </div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <h2>Admin</h2>
            <button class="secondary" id="loadAdminUsersBtn">Users</button>
          </div>
          <div class="panel-body stack">
            <div class="row">
              <label>Email<input id="newUserEmail" type="email" value="new.user@example.com"></label>
              <label>Full name<input id="newUserName" type="text" value="New User"></label>
            </div>
            <label>Password<input id="newUserPassword" type="text" value="new12345"></label>
            <div class="actions">
              <button id="createUserBtn">Create user</button>
            </div>
            <div id="adminList" class="list"></div>
            <div class="data" id="adminBox">{}</div>
          </div>
        </section>

        <section class="panel wide">
          <div class="panel-head">
            <h2>Payment webhook</h2>
            <div class="actions">
              <button class="secondary" id="signBtn">Sign</button>
              <button class="warn" id="sendWebhookBtn">Send</button>
            </div>
          </div>
          <div class="panel-body stack">
            <div class="row">
              <label>Transaction ID<input id="transactionId" type="text" value="demo-transaction-001"></label>
              <label>Amount<input id="amount" type="number" min="0" step="0.01" value="100"></label>
            </div>
            <div class="row">
              <label>User ID<input id="userId" type="number" min="1" value="1"></label>
              <label>Account ID<input id="accountId" type="number" min="1" value="1"></label>
            </div>
            <label>Secret key<input id="secretKey" type="text" value="gfdmhghif38yrf9ew0jkf32"></label>
            <label>Signature<input id="signature" type="text"></label>
            <div id="webhookMessage" class="message"></div>
            <div class="data" id="webhookBox">{}</div>
          </div>
        </section>
      </section>
    </div>
  </main>

  <script>
    const state = {
      role: localStorage.getItem("role") || "user",
      userToken: localStorage.getItem("userToken") || "",
      adminToken: localStorage.getItem("adminToken") || ""
    };

    const $ = (id) => document.getElementById(id);
    const pretty = (data) => JSON.stringify(data, null, 2);

    function tokenFor(role = state.role) {
      return role === "admin" ? state.adminToken : state.userToken;
    }

    function setMessage(id, text, kind = "") {
      const node = $(id);
      node.textContent = text;
      node.className = `message ${kind}`;
    }

    function setJson(id, data) {
      $(id).textContent = pretty(data);
    }

    async function request(path, options = {}, role = state.role) {
      const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
      const token = tokenFor(role);
      if (token) headers.Authorization = `Bearer ${token}`;

      const response = await fetch(path, { ...options, headers });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        const message = data.error || `HTTP ${response.status}`;
        throw Object.assign(new Error(message), { data, status: response.status });
      }
      return data;
    }

    function syncRole() {
      document.querySelectorAll(".tab").forEach((tab) => {
        tab.classList.toggle("active", tab.dataset.role === state.role);
      });
      $("email").value = state.role === "admin" ? "admin@example.com" : "user@example.com";
      $("password").value = state.role === "admin" ? "admin12345" : "user12345";
      localStorage.setItem("role", state.role);
      renderSession();
    }

    function renderSession() {
      setJson("sessionBox", {
        role: state.role,
        userToken: state.userToken ? "stored" : "empty",
        adminToken: state.adminToken ? "stored" : "empty"
      });
    }

    async function checkHealth() {
      try {
        const data = await request("/health", {}, "");
        $("healthDot").classList.add("ok");
        $("healthText").textContent = data.status === "ok" ? "localhost:3993 online" : "localhost:3993";
      } catch (_error) {
        $("healthDot").classList.remove("ok");
        $("healthText").textContent = "localhost:3993 offline";
      }
    }

    async function login() {
      setMessage("loginMessage", "");
      try {
        const data = await request(`/api/${state.role === "admin" ? "admin" : "users"}/login`, {
          method: "POST",
          body: JSON.stringify({ email: $("email").value, password: $("password").value })
        }, "");
        if (state.role === "admin") {
          state.adminToken = data.access_token;
          localStorage.setItem("adminToken", state.adminToken);
        } else {
          state.userToken = data.access_token;
          localStorage.setItem("userToken", state.userToken);
        }
        setMessage("loginMessage", "Logged in", "ok");
        renderSession();
      } catch (error) {
        setMessage("loginMessage", error.message, "err");
      }
    }

    function logout() {
      state.userToken = "";
      state.adminToken = "";
      localStorage.removeItem("userToken");
      localStorage.removeItem("adminToken");
      setMessage("loginMessage", "Logged out");
      renderSession();
    }

    async function loadUser(path) {
      try {
        const data = await request(path, {}, "user");
        setJson("userBox", data);
        renderItems("userList", data.items || [data]);
      } catch (error) {
        setJson("userBox", error.data || { error: error.message });
      }
    }

    async function loadAdminUsers() {
      try {
        const data = await request("/api/admin/users", {}, "admin");
        setJson("adminBox", data);
        renderItems("adminList", data.items || []);
      } catch (error) {
        setJson("adminBox", error.data || { error: error.message });
      }
    }

    async function createUser() {
      try {
        const data = await request("/api/admin/users", {
          method: "POST",
          body: JSON.stringify({
            email: $("newUserEmail").value,
            full_name: $("newUserName").value,
            password: $("newUserPassword").value
          })
        }, "admin");
        setJson("adminBox", data);
        await loadAdminUsers();
      } catch (error) {
        setJson("adminBox", error.data || { error: error.message });
      }
    }

    function renderItems(id, items) {
      const node = $(id);
      node.innerHTML = "";
      items.slice(0, 6).forEach((item) => {
        const row = document.createElement("div");
        row.className = "item";
        const title = item.email || item.transaction_id || `Account #${item.id || item.account_id}`;
        const meta = item.balance ? `balance ${item.balance}` : item.amount ? `amount ${item.amount}` : item.full_name || "";
        row.innerHTML = `<strong>${escapeHtml(title)}</strong><span>${escapeHtml(meta)}</span>`;
        node.appendChild(row);
      });
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
      }[char]));
    }

    async function sha256(text) {
      const bytes = new TextEncoder().encode(text);
      const hash = await crypto.subtle.digest("SHA-256", bytes);
      return Array.from(new Uint8Array(hash)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
    }

    function webhookPayload(includeSignature = true) {
      const payload = {
        transaction_id: $("transactionId").value,
        user_id: Number($("userId").value),
        account_id: Number($("accountId").value),
        amount: Number($("amount").value)
      };
      if (includeSignature) payload.signature = $("signature").value;
      return payload;
    }

    async function signWebhook() {
      const payload = webhookPayload(false);
      const source = `${payload.account_id}${payload.amount}${payload.transaction_id}${payload.user_id}${$("secretKey").value}`;
      $("signature").value = await sha256(source);
      setMessage("webhookMessage", "Signed", "ok");
    }

    async function sendWebhook() {
      try {
        if (!$("signature").value) await signWebhook();
        const data = await request("/api/payments/webhook", {
          method: "POST",
          body: JSON.stringify(webhookPayload(true))
        }, "");
        setJson("webhookBox", data);
        setMessage("webhookMessage", data.status, "ok");
        await loadUser("/api/users/me/accounts");
      } catch (error) {
        setJson("webhookBox", error.data || { error: error.message });
        setMessage("webhookMessage", error.message, "err");
      }
    }

    document.querySelectorAll(".tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        state.role = tab.dataset.role;
        syncRole();
      });
    });

    $("loginBtn").addEventListener("click", login);
    $("logoutBtn").addEventListener("click", logout);
    $("loadMeBtn").addEventListener("click", () => loadUser("/api/users/me"));
    $("loadAccountsBtn").addEventListener("click", () => loadUser("/api/users/me/accounts"));
    $("loadPaymentsBtn").addEventListener("click", () => loadUser("/api/users/me/payments"));
    $("refreshUserBtn").addEventListener("click", () => loadUser("/api/users/me/accounts"));
    $("loadAdminUsersBtn").addEventListener("click", loadAdminUsers);
    $("createUserBtn").addEventListener("click", createUser);
    $("signBtn").addEventListener("click", signWebhook);
    $("sendWebhookBtn").addEventListener("click", sendWebhook);

    syncRole();
    checkHealth();
    signWebhook();
  </script>
</body>
</html>
"""

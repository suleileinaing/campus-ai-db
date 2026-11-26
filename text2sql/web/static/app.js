"use strict";

const $ = (id) => document.getElementById(id);
const TIMEOUT_MS = 90000;
const A = "assets/";
const ico = (file, w) => `<span class="ico" style="--src:url(${A}${file})" data-w="${w}"></span>`;
const img = (file, w, h = w) => `<img src="${A}${file}" alt="" width="${w}" height="${h}">`;

const state = {
  token: null, name: null, studentId: null, college: "", expired: false,
  convs: [], active: null, busy: false, controller: null,
};

/* ---------- 공통 ---------- */
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
/** 답변의 간단한 마크다운(**굵게**, * / - 목록)만 HTML 로 바꾼다. 먼저 이스케이프한다. */
function md(s) {
  return esc(s).trim()
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/^\s*[*-]\s+/gm, "• ")
    .replace(/\n{3,}/g, "\n\n");
}
function el(html) {
  const t = document.createElement("template");
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
}
const newId = () => (crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random()));

async function api(path, body, signal) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const r = await fetch(path, { method: body ? "POST" : "GET", headers, body: body ? JSON.stringify(body) : undefined, signal });
  const data = await r.json().catch(() => ({ error: "결과를 불러오지 못했어요.", retry: true }));
  if (!r.ok) throw Object.assign(new Error(data.error), { status: r.status, data });
  return data;
}

/* ---------- 화면 전환: 01 랜딩 ↔ 채팅 ---------- */
function showApp() {
  $("landing").hidden = true;
  $("app").hidden = false;
  if (!state.active) newConversation();
  syncSend();
  $("input").focus();
}
document.querySelectorAll("[data-start]").forEach((b) => b.addEventListener("click", showApp));

// 랜딩 미리보기: 질문 → (1.2초) 답변 → (3초) 처음으로 반복 (Figma 프로토타입과 같은 흐름)
(function heroLoop() {
  const a = $("hpAnswer");
  let on = false;
  setInterval(() => {
    on = !on;
    a.textContent = on ? "지금까지 총 123학점을 이수했어요." : "• • •";
    a.classList.toggle("done", on);
  }, 2100);
})();

/* ---------- 테마 ---------- */
function setTheme(t) {
  document.documentElement.dataset.theme = t;
  document.querySelectorAll("[data-theme-btn]").forEach((b) => b.classList.toggle("on", b.dataset.themeBtn === t));
  try { localStorage.setItem("theme", t); } catch (_) {}
}
document.querySelectorAll("[data-theme-btn]").forEach((b) => b.addEventListener("click", () => setTheme(b.dataset.themeBtn)));
let savedTheme = "crimson";
try { savedTheme = localStorage.getItem("theme") || "crimson"; } catch (_) {}
setTheme(savedTheme);

/* ---------- 계정 ---------- */
function renderAccount() {
  const box = $("account");
  if (state.token) {
    box.innerHTML = `<div class="profile">나</div>
      <div class="acct-info"><b>${esc(state.studentId)}</b><span>${esc(state.college || state.name)}</span></div>
      <button class="acct-action" id="logoutBtn">로그아웃</button>`;
    $("logoutBtn").onclick = logout;
  } else {
    box.innerHTML = `<div class="profile">나</div>
      <div class="acct-info"><b>로그인 필요</b><span>${state.expired ? "세션이 만료됐어요" : "본인 정보는 로그인 후"}</span></div>
      <button class="acct-action strong" data-open-login>로그인</button>`;
  }
}

function openLogin() {
  $("expiredNotice").hidden = !state.expired;
  $("loginError").hidden = true;
  $("loginModal").hidden = false;
  $("sid").focus();
}
function closeLogin() { $("loginModal").hidden = true; }
document.addEventListener("click", (e) => {
  if (e.target.closest("[data-open-login]")) openLogin();
  if (e.target.closest("[data-close-login]") || e.target === $("loginModal")) closeLogin();
});

$("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = $("loginBtn");
  btn.disabled = true;
  $("loginError").hidden = true;
  try {
    const d = await api("/api/login", { student_id: $("sid").value, password: $("pw").value });
    Object.assign(state, { token: d.token, name: d.name, studentId: d.student_id, college: d.college, expired: false });
    $("pw").value = "";
    closeLogin();
    document.querySelectorAll(".expired-banner").forEach((b) => b.remove());
    $("input").placeholder = "궁금한 학사 정보를 물어보세요";
    renderAccount();
    if ($("landing").hidden === false) showApp();
  } catch (err) {
    $("loginError").textContent = err.message || "로그인하지 못했어요.";
    $("loginError").hidden = false;
  } finally {
    btn.disabled = false;
  }
});

async function logout() {
  try { await api("/api/logout", {}); } catch (_) {}
  Object.assign(state, { token: null, name: null, studentId: null, college: "", expired: false });
  erasePersonal();
  renderAccount();
}

/** 08-1: 세션 만료 → 개인 답변을 지우고 위쪽 배너로 재로그인 안내 */
function onExpired() {
  Object.assign(state, { token: null, name: null, studentId: null, college: "", expired: true });
  erasePersonal();
  renderAccount();
  const msgs = cur().box;
  if (!msgs.querySelector(".expired-banner")) {
    msgs.prepend(el(`<div class="expired-banner">${img("icon-clock-18.svg", 18)}
      <span>로그인 시간이 만료됐어요. 다시 로그인해 주세요</span>
      <button class="btn-solid" data-open-login>다시 로그인</button></div>`));
  }
  $("input").placeholder = "다시 로그인하면 이어서 물어볼 수 있어요";
}

/** 개인 정보가 담긴 답변을 모든 대화에서 지운다. 서버의 대화 기록도 지운다. */
function erasePersonal() {
  for (const c of state.convs) {
    c.box.querySelectorAll(".bot.personal").forEach((m) => {
      m.classList.remove("personal");
      m.querySelector(".bot-content").innerHTML = `<p class="bot-name">쿠옹이</p>
        <div class="bubble erased">개인 정보가 담긴 답변은 로그인이 만료되어 지웠어요.</div>`;
      let n = m.nextElementSibling;
      while (n && n.dataset.owner === m.dataset.id) { const x = n.nextElementSibling; n.remove(); n = x; }
      m.after(el(`<div class="status">${img("icon-lock.svg", 13)}숨긴 답변 · 다시 로그인하면 새로 조회해요</div>`));
    });
    api("/api/reset", { conversation_id: c.id }).catch(() => {});
  }
}

/* ---------- 대화 목록 ---------- */
const cur = () => state.convs.find((c) => c.id === state.active);

function newConversation() {
  const old = cur();
  if (old && !old.box.children.length) return switchTo(old.id); // 빈 대화가 이미 열려 있으면 그대로
  const c = { id: newId(), title: "새 대화", box: el(`<div class="messages"></div>`) };
  state.convs.unshift(c);
  switchTo(c.id);
}
function switchTo(id) {
  if (state.busy) state.controller?.abort("stop");
  state.active = id;
  const c = cur();
  $("messages").replaceWith(c.box);
  c.box.id = "messages";
  $("welcome").hidden = c.box.children.length > 0;
  $("chatTitle").textContent = c.title;
  renderConvList();
  $("sidebar").classList.remove("open");
}
function renderConvList() {
  const list = $("convList");
  const used = state.convs.filter((c) => c.box.children.length || c.id === state.active);
  list.innerHTML = used.length
    ? used.map((c) => `<button class="conv-item ${c.id === state.active ? "active" : ""}" data-conv="${c.id}">${esc(c.title)}</button>`).join("")
    : `<p class="conv-empty">아직 대화가 없어요</p>`;
}
$("convList").addEventListener("click", (e) => {
  const b = e.target.closest("[data-conv]");
  if (b) switchTo(b.dataset.conv);
});
$("newChat").addEventListener("click", newConversation);
$("menuBtn").addEventListener("click", () => $("sidebar").classList.toggle("open"));

/* ---------- 입력창 (06-1 / 06-2 / 05) ---------- */
const input = $("input");
function syncSend() {
  const empty = !input.value.trim();
  $("sendBtn").disabled = state.busy || empty;
  // 자리는 남겨 두고 글자만 숨긴다(없애면 입력 영역 높이가 줄어 입력창이 아래로 밀린다)
  $("hint").style.visibility = !empty || state.busy || cur()?.box.children.length > 0 ? "hidden" : "visible";
  $("composer").classList.toggle("filled", !empty);
  input.style.height = "auto";
  if (input.scrollHeight) input.style.height = Math.min(input.scrollHeight, 140) + "px";
}
input.addEventListener("input", syncSend);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    $("composer").requestSubmit();
  }
});
$("composer").addEventListener("submit", (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (q && !state.busy) ask(q);
});
$("stopBtn").addEventListener("click", () => state.controller?.abort("stop"));
$("stopPill").addEventListener("click", () => state.controller?.abort("stop"));

function setBusy(b) {
  state.busy = b;
  $("sendBtn").hidden = b;
  $("stopBtn").hidden = !b;
  $("stopPill").hidden = !b;
  input.disabled = b;
  input.placeholder = b ? "쿠옹이가 답변을 만드는 중이에요…"
    : state.expired ? "다시 로그인하면 이어서 물어볼 수 있어요" : "궁금한 학사 정보를 물어보세요";
  syncSend();
}

/* ---------- 메시지 ---------- */
function scrollDown() { const a = $("chatArea"); a.scrollTop = a.scrollHeight; }

function addQuestion(q) {
  const c = cur();
  if (c.title === "새 대화") {
    c.title = q.length > 18 ? q.slice(0, 18) + "…" : q;
    $("chatTitle").textContent = c.title;
  }
  $("welcome").hidden = true;
  c.box.append(el(`<div class="q-row"><div class="q-bubble">${esc(q)}</div></div>`));
  renderConvList();
}

/** 봇 답변 한 덩어리: 말풍선 + 아래 줄들(표·상태·버튼). 아래 줄은 data-owner 로 묶어 둔다. */
function addBot(bubbleHtml, rows = [], opts = {}) {
  const id = newId();
  const box = cur().box;
  const m = el(`<div class="bot ${opts.cls || ""}" data-id="${id}">${img("kuong-hello.png", 40)}
    <div class="bot-content"><p class="bot-name">쿠옹이</p>${bubbleHtml}</div></div>`);
  if (opts.q) m.dataset.q = opts.q;
  box.append(m);
  for (const r of rows) {
    const n = el(r);
    n.dataset.owner = id;
    if (opts.q) n.dataset.q = opts.q;
    box.append(n);
  }
  scrollDown();
  return m;
}
function removeBot(m) {
  let n = m.nextElementSibling;
  while (n && n.dataset.owner === m.dataset.id) { const x = n.nextElementSibling; n.remove(); n = x; }
  m.remove();
}

async function ask(q) {
  addQuestion(q);
  input.value = "";
  setBusy(true);
  // 05 답변 생성 중
  const typing = addBot(`<div class="bubble typing">• • •</div>`, [
    `<div class="status">${ico("icon-check.svg", 12)}<span class="medium">질문 이해</span><span>·</span>${ico("icon-search-12.svg", 12)}<span class="step-on">학교 DB에서 찾는 중…</span></div>`,
  ]);
  const controller = new AbortController();
  state.controller = controller;
  const timer = setTimeout(() => controller.abort("timeout"), TIMEOUT_MS);
  try {
    const d = await api("/api/chat", { question: q, conversation_id: state.active }, controller.signal);
    removeBot(typing);
    renderAnswer(d, q);
  } catch (err) {
    removeBot(typing);
    const reason = controller.signal.aborted ? controller.signal.reason : null;
    if (reason === "stop") {
      // 05-1 답변 멈춤
      addBot(`<div class="bubble stopped">답변을 멈췄어요.</div>`, [
        `<div class="row"><button class="btn-outline" data-retry>${ico("icon-retry.svg", 16)}다시 생성</button>
          <button class="chip" data-edit>질문 고치기</button></div>`,
      ], { q });
    } else if (err.status === 401 && err.data?.expired) {
      onExpired();
    } else if (err.status === 400 || err.status === 429) {
      addBot(`<div class="bubble">${esc(err.message)}</div>`);
    } else {
      // 04-3 오류·시간 초과
      const why = reason === "timeout" ? `응답 시간이 초과됐어요 (${TIMEOUT_MS / 1000}초)` : "서버에서 답을 받지 못했어요";
      addBot(`<div class="bubble error">결과를 불러오지 못했어요.\n잠시 후 다시 시도해 주세요. 문제가 계속되면 질문을 조금 바꿔 보세요.</div>`, [
        `<div class="status">${img("icon-alert.svg", 14)}<span class="medium">${why}</span></div>`,
        `<div class="row"><button class="btn-outline" data-retry>${ico("icon-retry.svg", 16)}같은 질문 다시 시도</button></div>`,
      ], { q });
    }
  } finally {
    clearTimeout(timer);
    state.controller = null;
    setBusy(false);
    input.focus();
  }
}

document.addEventListener("click", (e) => {
  const t = e.target;
  const retry = t.closest("[data-retry]");
  if (retry && !state.busy) return ask(retry.closest("[data-q]").dataset.q);
  const edit = t.closest("[data-edit]");
  if (edit) {
    input.value = edit.closest("[data-q]").dataset.q;
    syncSend();
    input.focus();
    return;
  }
  const chip = t.closest("[data-ask]");
  if (chip && !state.busy) {
    if ($("app").hidden) showApp();
    return ask(chip.dataset.ask);
  }
  const src = t.closest("[data-src]");
  if (src) openSyllabus(src.dataset.code, src.dataset.section, src.dataset.snip);
});

function cell(v) {
  if (v === "미기재") return `<span class="badge missing">미기재</span>`;
  if (v === "확인 필요") return `<span class="badge check">확인 필요</span>`;
  return esc(v);
}
function tableRows(t) {
  const hasMissing = t.rows.some((r) => r.includes("미기재"));
  const more = t.total > t.rows.length ? `<p class="table-more">${t.total}건 중 ${t.rows.length}건만 보여요</p>` : "";
  const legend = hasMissing
    ? `<div class="legend"><span class="badge missing">미기재</span>자료에 값이 적혀 있지 않아요</div>` : "";
  return `<div class="table-block"><div class="table-wrap"><table>
    <thead><tr>${t.columns.map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead>
    <tbody>${t.rows.map((r) => `<tr>${r.map((v) => `<td>${cell(v)}</td>`).join("")}</tr>`).join("")}</tbody>
  </table></div>${legend}${more}</div>`;
}

const SCOPE = [
  ["icon-calendar.svg", "개설 강좌·시간표·담당 교수", "2020~2026학년도"],
  ["icon-doc-16.svg", "강의계획서", "평가 비율, 수업 방법, 주차별 계획 (2026-2 본문 검색)"],
  ["icon-cap.svg", "졸업요건·교양 기본구조표", "학과·학번별 이수 기준"],
  ["icon-person.svg", "내 수강 이력·이수 학점", "로그인한 본인만"],
];

function renderAnswer(d, q) {
  const rows = [];
  let bubbleCls = "";
  let botCls = "";

  if (d.table) rows.push(tableRows(d.table));

  if (d.kind === "empty") {
    // 04-2 결과 0건
    rows.push(`<div class="row"><button class="btn-outline" data-edit>${ico("icon-filter.svg", 16)}조건 변경</button></div>`);
  } else if (d.kind === "error") {
    bubbleCls = "error";
    rows.push(`<div class="row"><button class="btn-outline" data-retry>${ico("icon-retry.svg", 16)}같은 질문 다시 시도</button></div>`);
  } else if (d.kind === "not_found") {
    // 09-1 확인 범위 안내
    rows.push(`<div class="row"><div class="scope-card"><b>확인할 수 있는 정보</b>${SCOPE.map(([f, t, s]) =>
      `<div class="scope-item"><span class="scope-icon">${ico(f, 16)}</span><div><strong>${t}</strong><small>${s}</small></div></div>`).join("")}</div></div>`);
    rows.push(`<div class="row"><button class="chip" data-ask="이번 학기 내 시간표 알려줘">이번 학기 내 시간표</button>
      <button class="chip" data-ask="졸업까지 남은 학점 알려줘">졸업까지 남은 학점</button>
      <button class="chip" data-ask="2026-2 월요일 1교시 수업 알려줘">월요일 1교시 수업</button></div>`);
  } else if (d.kind === "refused") {
    // 09-2 타인 정보 차단
    bubbleCls = "blocked";
    rows.push(`<div class="status accent">${ico("icon-shield-block.svg", 13)}개인정보 보호를 위해 요청을 차단했어요</div>`);
    rows.push(`<div class="row"><button class="chip" data-ask="내 성적 보여줘">내 성적 보기</button>
      <button class="chip" data-ask="내가 지금까지 이수한 학점은?">내 이수 학점</button></div>`);
  } else if (d.kind === "login_required") {
    rows.push(`<div class="row"><button class="btn-outline" data-open-login>로그인</button></div>`);
  }

  // 07 출처 · 원문 열기
  if (d.route === "search" && d.sources.length) {
    rows.push(`<div class="row"><span class="row-label">출처</span>${d.sources.map((s) =>
      `<button class="src-btn" data-src data-code="${esc(s.code)}" data-section="${esc(s.section)}" data-snip="${esc((s.snippets || []).join("\n"))}">
        ${img("icon-doc.svg", 14)}<span class="code">${esc(s.label)}</span><b>원문 열기</b>${ico("icon-external.svg", 11)}</button>`).join("")}</div>`);
  }
  // 08 본인 정보 표시
  if (d.personal) {
    botCls = "personal";
    rows.push(`<div class="status">${img("icon-lock.svg", 13)}본인 정보 · 학번 ${esc(d.student_id)} 기준</div>`);
  }
  addBot(`<div class="bubble ${bubbleCls}">${md(d.answer)}</div>`, rows, { q, cls: botCls });
}

/* ---------- 07-1 강의계획서 원문 ---------- */
async function openSyllabus(code, section, snip) {
  $("dKicker").textContent = "강의계획서 원문";
  $("dTitle").textContent = `${code}-${section}`;
  $("dMeta").textContent = "";
  $("drawerBody").innerHTML = `<p class="d-meta">불러오는 중…</p>`;
  $("drawer").hidden = false;
  $("drawerDim").hidden = false;
  try {
    const s = await api(`/api/syllabus?code=${encodeURIComponent(code)}&section=${encodeURIComponent(section)}`);
    $("dKicker").textContent = `${s.term} 강의계획서 원문`;
    $("dTitle").textContent = s.title;
    const meta = [];
    if (s.professors.length) meta.push(`담당 ${s.professors.join(", ")}`);
    if (s.methods.length) meta.push(`수업 방법 ${s.methods.join(", ")}`);
    $("dMeta").textContent = meta.join(" · ");

    const rates = s.rates.filter((r) => r.label !== "기타" || (r.value != null && r.value !== "0")).map((r) =>
      `<div class="rate"><small>${esc(r.label.replace("고사", ""))}</small>${r.value == null
        ? `<span class="badge missing">미기재</span>` : `<strong>${esc(r.value)}%</strong>`}</div>`).join("");

    const texts = [["수업 개요", s.overview], ["수업 목표", s.objectives], ["과제", s.assignments]].filter(([, v]) => v && v.trim());
    const overview = texts.length
      ? texts.map(([k, v]) => `<p class="d-text"><b>${k}</b>\n${esc(v.trim())}</p>`).join("")
      : `<div class="d-missing"><span class="badge missing">미기재</span>강의계획서에 수업 개요·목표·과제 설명이 적혀 있지 않아요</div>`;

    $("drawerBody").innerHTML = `
      <div class="d-section"><b>평가 비율</b><div class="rates">${rates}</div></div>
      <div class="d-section"><b>수업 개요·과제</b>${overview}</div>
      <div class="d-section"><b>주차별 계획</b>${weeksHtml(s.weeks, snip || "")}</div>
      <a class="orig-link" href="${esc(s.source_url)}" target="_blank" rel="noopener">학교 강의계획서 사이트에서 원본 보기${ico("icon-external-12.svg", 12)}</a>`;
  } catch (err) {
    $("drawerBody").innerHTML = `<p class="d-meta">${esc(err.message || "원문을 불러오지 못했어요.")}</p>`;
  }
}

/** 같은 내용이 이어지는 주차는 'n~m주차도 같은 내용'으로 접고, 답변 근거가 된 주차는 강조한다. */
function weeksHtml(weeks, snip) {
  if (!weeks.length) return `<div class="d-missing"><span class="badge missing">미기재</span>주차별 계획이 적혀 있지 않아요</div>`;
  const norm = (t) => (t || "").replace(/\s+/g, " ").trim();
  const snipN = norm(snip);
  let hitShown = false;
  const out = [];
  for (let i = 0; i < weeks.length; i++) {
    const w = weeks[i];
    const t = norm(w.topic_content);
    let j = i;
    while (j + 1 < weeks.length && norm(weeks[j + 1].topic_content) === t && t) j++;
    const isHit = !hitShown && t && snipN.includes(t);
    const row = (wk, cls = "") => `<div class="week ${cls}"><small>${wk.week}주</small><span>${t ? esc(wk.topic_content) : `<span class="badge missing">미기재</span>`}</span>${
      cls === "hit" ? `<span class="badge yes">답변 근거</span>` : ""}</div>`;
    out.push(row(w, isHit ? "hit" : ""));
    if (isHit) hitShown = true;
    if (j - i >= 5) {
      // 1~3주는 보여 주고, 가운데는 접고, 마지막 2주는 다시 보여 준다(Figma 07-1 과 같은 모양)
      out.push(row(weeks[i + 1]), row(weeks[i + 2]));
      out.push(`<div class="week same">${weeks[i + 3].week}~${weeks[j - 2].week}주차도 같은 내용</div>`);
      out.push(row(weeks[j - 1]), row(weeks[j]));
    } else {
      for (let k = i + 1; k <= j; k++) out.push(row(weeks[k]));
    }
    i = j;
  }
  return `<div class="weeks">${out.join("")}</div>`;
}
function closeDrawer() { $("drawer").hidden = true; $("drawerDim").hidden = true; }
$("drawerClose").onclick = closeDrawer;
$("drawerDim").onclick = closeDrawer;
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { closeDrawer(); closeLogin(); }
});

/* ---------- 시작 ---------- */
renderAccount();
if (location.hash === "#chat") showApp();
syncSend();

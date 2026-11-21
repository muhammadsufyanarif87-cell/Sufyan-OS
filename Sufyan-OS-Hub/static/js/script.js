async function searchHub() {
  const input = document.getElementById("searchInput");
  const results = document.getElementById("results");
  if (!input || !results) return;
  const q = input.value.trim();
  if (!q) { results.innerHTML = '<p class="empty-state">Kuch search karo, jaise ls ya RAM.</p>'; return; }
  results.innerHTML = '<p class="muted">Searching...</p>';
  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const data = await response.json();
    results.replaceChildren();
    if (data.type === "hardware") {
      const card = document.createElement("div");
      card.className = "result-card";
      const title = document.createElement("h3");
      title.textContent = data.label + " — " + data.value;
      const detail = document.createElement("p");
      detail.textContent = "Live information tumhare computer se read ki gayi hai.";
      card.append(title, detail);
      results.append(card);
    } else if (data.results && data.results.length) {
      data.results.forEach(item => {
        const card = document.createElement("div");
        card.className = "result-card";
        const title = document.createElement("h3");
        title.textContent = item.command + " — " + item.title;
        const desc = document.createElement("p");
        desc.textContent = item.description;
        const code = document.createElement("code");
        code.textContent = item.example;
        const copy = document.createElement("button");
        copy.className = "copy-btn";
        copy.textContent = "Copy";
        copy.addEventListener("click", () => copyText(item.example, copy));
        card.append(title, desc, code, copy);
        results.append(card);
      });
    } else {
      results.innerHTML = '<p class="empty-state">Koi matching command nahi mila. Commands page par bhi search kar sakte ho.</p>';
    }
  } catch (error) {
    results.innerHTML = '<p class="error-text">Search failed. Flask server check karo.</p>';
  }
}
function quickSearch(value) {
  const input = document.getElementById("searchInput");
  if (input) { input.value = value; searchHub(); }
}
async function copyText(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    if (button) { const old = button.textContent; button.textContent = "Copied ✓"; setTimeout(() => button.textContent = old, 1200); }
  } catch { alert("Clipboard access nahi mila. Command manually copy karo: " + text); }
}
document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  if (searchInput) searchInput.addEventListener("keydown", e => { if (e.key === "Enter") searchHub(); });
  document.querySelectorAll("[data-copy]").forEach(button => button.addEventListener("click", () => copyText(button.dataset.copy, button)));
  const filter = document.getElementById("commandFilter");
  if (filter) filter.addEventListener("input", () => {
    const q = filter.value.toLowerCase();
    let shown = 0;
    document.querySelectorAll(".command-card").forEach(card => {
      const match = card.dataset.search.toLowerCase().includes(q);
      card.hidden = !match;
      if (match) shown++;
    });
    const empty = document.getElementById("noCommands");
    if (empty) empty.hidden = shown !== 0;
  });
});
async function refreshComputer() {
  const status = document.getElementById("refreshStatus");
  if (status) status.textContent = "Refreshing...";
  try {
    const r = await fetch("/api/computer");
    const d = await r.json();
    const put = (id, value) => { const el = document.getElementById(id); if (el) el.textContent = value; };
    put("cpu", d.cpu);
    put("cpuMeta", `${d.cpu_cores} cores • ${d.cpu_threads} threads • ${d.cpu_speed}`);
    put("ram", `${d.ram_total_gb} GB`);
    put("ramMeta", `${d.ram_used_gb} GB used • ${d.ram_percent}%`);
    const bar = document.getElementById("ramBar"); if (bar) bar.style.width = `${d.ram_percent}%`;
    put("disk", `${d.disk_total_gb} GB`);
    put("diskMeta", `${d.disk_used_gb} GB used • ${d.disk_free_gb} GB free`);
    put("gpu", d.gpu); put("distribution", d.distribution);
    put("osMeta", `${d.os} • ${d.architecture}`); put("network", d.network); put("uptime", d.uptime);
    if (status) status.textContent = "Updated just now.";
  } catch { if (status) status.textContent = "Refresh failed."; }
}

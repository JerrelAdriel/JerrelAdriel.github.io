# 📚 Portfolio & Projects — Update Documentation

> **Author:** Jerrel Adriel A Hutahaean
> **Last Updated:** 2 Juni 2026
> **Live Portfolio:** [jerreladriel.github.io](https://jerreladriel.github.io)

Dokumen ini merangkum semua pembaruan major yang dilakukan pada portfolio website dan 5 project di dalamnya, termasuk penjelasan teknis dan keputusan desain di setiap perubahan.

---

## 📑 Table of Contents

1. [Portfolio Website](#1-portfolio-website)
2. [Agent-JR](#2-agent-jr--multi-platform-ai-assistant)
3. [Brain Tumor Classification](#3-brain-tumor-classification)
4. [Lelang Binar (Second Hand)](#4-lelang-binar-second-hand)
5. [Stockop / jStock](#5-stockop--jstock)
6. [Jump Game](#6-jump-game)
7. [Infrastructure & Security](#7-infrastructure--security)

---

## 1. Portfolio Website

**Repo:** [JerrelAdriel/JerrelAdriel.github.io](https://github.com/JerrelAdriel/JerrelAdriel.github.io)
**Live:** [jerreladriel.github.io](https://jerreladriel.github.io)
**Tech Stack:** HTML5, CSS3, Vanilla JavaScript

### What was built

Halaman single-page portfolio yang lengkap dengan 6 section: **Hero, About, Experience, Projects, Skills, Contact**. Bilingual (English default + Indonesian toggle), responsive desktop & mobile, dark-mode, dengan animasi smooth.

### Key Features

| Feature | File | Notes |
|---|---|---|
| Bilingual EN/ID toggle | `i18n.js` | localStorage persistence, default EN |
| Project lightbox gallery | `portfolio.js` | Keyboard nav (← →), ESC close, klik luar = close |
| Smooth scroll navigation | `portfolio.js` | Anchor links + observer fade-in animation |
| Photo with transparent BG | `assets/profile/jerrel.png` | AI-processed via `rembg` (U²-Net model) |
| Work Experience timeline | `index.html` | Pulsing dot indikator current job |

### Code Highlights

#### `i18n.js` — Bilingual System

Pattern yang dipakai: **HTML attribute-based translation** dengan dictionary lookup.

```html
<!-- HTML -->
<h2 data-i="about.title">About</h2>
<p data-i-html="exp.surge.list">
  <li>...</li>
</p>
```

```javascript
// i18n.js
const TRANSLATIONS = {
  en: { 'about.title': 'About', /* ... */ },
  id: { 'about.title': 'Tentang', /* ... */ },
};

function applyLanguage(lang) {
  const dict = TRANSLATIONS[lang];
  // Plain text replacement
  document.querySelectorAll('[data-i]').forEach(el => {
    if (dict[el.dataset.i]) el.innerHTML = dict[el.dataset.i];
  });
  // HTML replacement (for lists with <li>)
  document.querySelectorAll('[data-i-html]').forEach(el => {
    if (dict[el.dataset.iHtml]) el.innerHTML = dict[el.dataset.iHtml];
  });
  localStorage.setItem('portfolio_lang', lang);
}
```

**Kenapa pakai pola ini:**
- Tidak butuh framework (React/Vue), tetap pakai vanilla JS
- Default bahasa terlihat dari HTML asli (English) → SEO-friendly
- Tinggal tambah `data-i="key"` ke element baru, lalu tambah key ke dictionary

#### `portfolio.js` — Lightbox Gallery

```javascript
const SCREENSHOTS = {
  'agent-jr':   [{ src: '...', caption: '...' }],
  'brain-tumor': [/* multiple screenshots with captions */],
  // dst.
};

document.querySelectorAll('[data-screenshots]').forEach(el => {
  el.addEventListener('click', () => openLightbox(
    el.dataset.screenshots,
    el.dataset.title
  ));
});

document.addEventListener('keydown', (e) => {
  if (lightbox.classList.contains('hidden')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft')  navigateLightbox(-1);
  if (e.key === 'ArrowRight') navigateLightbox(1);
});
```

**Keputusan desain:**
- Modal `position: fixed` dengan `inset: 0` — selalu cover full screen
- Counter "1/3" cuma muncul kalau ada >1 gambar
- Backdrop click → close (UX standar)

#### `portfolio.css` — Responsive Avatar Blur

**Bug yang sempat terjadi:** Blur ungu di belakang foto profil tidak ikut foto saat resize.

**Solusi:** Pakai pseudo-element `::before` di parent `.avatar`, ukuran pakai `padding-bottom` trick untuk maintain aspect ratio:

```css
.avatar::before {
  content: '';
  position: absolute;
  width: 92%;
  padding-bottom: 92%;       /* bikin selalu square */
  top: 5%;
  left: 50%;
  transform: translateX(-50%);  /* centered */
  background: radial-gradient(circle at 50% 50%,
    rgba(124,58,237,0.4), transparent 65%);
  border-radius: 50%;
  z-index: -1;                /* di belakang foto */
}
```

Sekarang blur selalu **proportional & centered** di setiap viewport size.

---

## 2. Agent-JR — Multi-Platform AI Assistant

**Repo:** [JerrelAdriel/agent-jr](https://github.com/JerrelAdriel/agent-jr)
**Tech Stack:** Python (FastAPI), Node.js (Electron + whatsapp-web.js), HTML/CSS/JS

### What it is

AI assistant pribadi yang berjalan di **3 platform sekaligus**:
- 🌐 Web chat UI (dark mode, streaming response)
- 📱 WhatsApp Bot (respon di-tag/reply, command `/all`, `/reset`)
- 🖥️ Desktop App (Electron wrapper)

Powered by **Claude (Anthropic)** dengan **fallback otomatis ke Groq (Llama 3.1)** kalau Claude tidak tersedia.

### Architecture

```
                   ┌──────────────────────┐
                   │  Backend FastAPI     │
                   │  Claude → Groq       │
                   └──┬──────┬──────┬─────┘
                      │      │      │
              ┌───────┘      │      └────────┐
              ▼              ▼               ▼
        ┌──────────┐  ┌────────────┐  ┌────────────┐
        │ Web Chat │  │ WhatsApp   │  │ Desktop    │
        │ (HTML/JS)│  │ Bot (Node) │  │ (Electron) │
        └──────────┘  └────────────┘  └────────────┘
```

Satu backend FastAPI melayani 3 frontend. Kalau backend down, semua frontend mati. Kalau salah satu frontend bermasalah, yang lain tetap jalan.

### Code Highlights

#### `main.py` — Fallback Logic Claude → Groq

```python
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Coba Claude dulu
    if anthropic_client:
        try:
            response = anthropic_client.messages.create(
                model="claude-haiku-4-5-20251001",
                system=SYSTEM_PROMPT,
                messages=to_messages(request.messages)
            )
            return {"reply": response.content[0].text, "source": "claude"}
        except Exception as e:
            print(f"[Claude gagal] {e} → beralih ke Groq...")

    # Fallback ke Groq
    if groq_client:
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + to_messages(request.messages)
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=msgs
        )
        return {"reply": response.choices[0].message.content, "source": "groq"}
```

**Kenapa pola ini:**
- Claude lebih bagus tapi berbayar; Groq gratis tapi quality sedikit di bawah
- Try-catch + fallback → graceful degradation
- Field `source` di response biar frontend tahu API mana yang dipakai

#### `whatsapp/bot.js` — Mention/Reply Detection

```javascript
client.on("message", async (msg) => {
  // Di grup: hanya respon kalau bot di-tag atau pesan kita di-reply
  if (msg.from.endsWith("@g.us")) {
    const botNumber = client.info.wid.user;
    const mentions = await msg.getMentions();
    const diTag = mentions.some(c => c.id.user === botNumber);

    let diReply = false;
    if (!diTag && msg.hasQuotedMsg) {
      const quoted = await msg.getQuotedMessage();
      diReply = quoted.fromMe;
    }
    if (!diTag && !diReply) return;
  }
  // ... lanjut proses pesan
});
```

**Penting:** WhatsApp Web sekarang punya 2 format ID (`@c.us` legacy + `@lid` baru). Solusi: pakai `msg.getMentions()` (resolved contacts) bukan `msg.mentionedIds` (raw IDs).

#### `frontend/script.js` — Streaming Response

```javascript
const res = await fetch(`${API_URL}/chat/stream`, { /* ... */ });
const reader = res.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const chunk = decoder.decode(value);
  // Parse SSE format "data: {...}\n\n"
  for (const line of chunk.split("\n")) {
    if (line.startsWith("data: ")) {
      const data = line.slice(6);
      if (data === "[DONE]") break;
      const { text } = JSON.parse(data);
      fullReply += text;
      bubble.innerHTML = renderMarkdown(fullReply);  // realtime update
    }
  }
}
```

**Efek "typing":** SSE (Server-Sent Events) → text mengalir token-per-token, UX seperti ChatGPT.

---

## 3. Brain Tumor Classification

**Repo:** [JerrelAdriel/brain-tumor-classification](https://github.com/JerrelAdriel/brain-tumor-classification)
**Tech Stack:** Python (Flask, TensorFlow, VGG16 CNN), HTML/CSS/JS

### What it does

Aplikasi web untuk klasifikasi tumor otak dari **gambar MRI** menggunakan deep learning. Model VGG16 dengan transfer learning, akurasi >95%. Ini adalah aplikasi dari **thesis S1** Jerrel di Universitas Sriwijaya.

### Updates yang dilakukan

| Sebelum | Sesudah |
|---|---|
| UI Bootstrap default, look kuno | Dark theme modern dengan cyan accent |
| Form upload simple `<input type="file">` | **Drag & drop zone** dengan file preview, progress, hapus button |
| Landing page minimal | Hero section + stats cards (95% accuracy, VGG16, <3s, 2 classes) + features grid |
| Hasil klasifikasi text biasa | Color-coded badge (red = tumor, green = no tumor) |

### Code Highlights

#### `templates/predict.html` — Drag & Drop Upload

```javascript
['dragover','dragenter'].forEach(ev =>
  dropZone.addEventListener(ev, e => {
    e.preventDefault();
    dropZone.classList.add('dragover');  // highlight saat hover
  })
);
['dragleave','drop'].forEach(ev =>
  dropZone.addEventListener(ev, e => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
  })
);
dropZone.addEventListener('drop', e => {
  const f = e.dataTransfer.files[0];
  if (f) {
    fileInput.files = e.dataTransfer.files;
    showFile(f);  // preview + enable submit
  }
});
```

**UX flow:**
1. User drag file → drop zone highlight cyan
2. Drop → file preview muncul (thumbnail + nama + size)
3. Button "Analisis Sekarang" enabled
4. Submit → POST ke `/predict` Flask endpoint
5. Hasil ditampilkan dengan badge color-coded

#### `templates/predict.html` — Modern CSS (Highlights)

```css
:root {
  --bg: #0a0a14;          /* dark navy background */
  --accent: #06b6d4;       /* cyan primary */
  --accent-glow: rgba(6,182,212,0.25);
}

.drop-zone {
  border: 2px dashed var(--border);
  transition: all 0.3s;
}
.drop-zone:hover, .drop-zone.dragover {
  border-color: var(--accent);
  background: rgba(6,182,212,0.05);
  transform: scale(1.01);   /* mini zoom feedback */
}
```

CSS variables + smooth transitions = profesional look.

---

## 4. Lelang Binar (Second Hand)

**Repo:** [JerrelAdriel/lelang-binar](https://github.com/JerrelAdriel/lelang-binar)
**Tech Stack:** React.js, React Bootstrap, Node.js + Express (backend), REST API, JWT Auth

### What it is

Aplikasi e-commerce lelang barang bekas — **final project Studi Independen Binar Academy** (2022). Pengguna bisa list produk, melakukan penawaran (nego), dan kelola transaksi.

### Bugs yang ditemukan & diperbaiki

#### Bug 1: `CardComponent` crash saat user belum login

**File:** `src/components/Cards/CardProduct.jsx`

**Before (crash):**
```javascript
const token = localStorage.getItem('token');
const decode = jwt(token);  // crash kalau token null
```

**After (safe):**
```javascript
const token = localStorage.getItem('token');
let decode = null;
try { if (token) decode = jwt(token); } catch (e) { /* invalid token */ }
```

**Penjelasan:** `jwt-decode` library throw error kalau input bukan JWT valid. Pakai `try-catch` + null guard supaya komponen tetap render.

#### Bug 2: React Bootstrap `Container md` props warning

`<Container md>` tanpa value dianggap `md={true}` oleh React, tapi react-bootstrap mau `fluid="md"`.

**Fix:** Ganti `<Container md>` → `<Container fluid="md">` di 2 file:
- `Cards/CardProduct.jsx`
- `NavbarBeforeLogin/NavbarDashboard.jsx`

#### Bug 3: Halaman gak bisa di-scroll

**File:** `src/index.css`
```css
/* BEFORE */
body { overflow: hidden; }   /* << biang kerok scroll terblokir */

/* AFTER */
body { overflow-x: hidden; overflow-y: auto; }
```

#### Bug 4: `p { height: 20px }` di `button.module.css` leak ke semua `<p>`

**Root cause:** CSS Modules **hanya scope class selector**, bukan element selector. Aturan `p { ... }` di file `*.module.css` apapun, akan **leak ke seluruh app**.

**Fix:** Scope ke class parent:
```css
/* BEFORE — leak ke semua <p> */
p { height: 20px; }

/* AFTER — cuma <p> di dalam .button */
.button p { height: 20px; }
```

#### Bug 5: `jwt-decode` v4 ganti export style

```javascript
// v3 (lama)
import jwt from 'jwt-decode';

// v4 (baru)
import { jwtDecode as jwt } from 'jwt-decode';
```

### Fitur baru: Dummy Data Fallback

Backend dummy server tidak selalu jalan (free hosting tier sleep). Solusi: **auto fallback** ke data dummy lokal.

**File:** `src/dummyProducts.js` — 12 produk lengkap dengan:
- Nama, harga (IDR), kategori, deskripsi panjang
- Profile penjual (nama, kota, foto Unsplash)
- 1-3 gambar produk per item

```javascript
// CardProduct.jsx
const getProducts = async () => {
  try {
    const res = await axios.get(url, { timeout: 3000 });
    if (res?.data?.data?.product?.length) {
      setItems(res.data.data.product);   // pakai API
    } else {
      setItems(DUMMY_PRODUCTS);          // fallback
    }
  } catch (error) {
    setItems(DUMMY_PRODUCTS);            // backend down → dummy
  }
};
```

### Fitur baru: Mock Nego Submit

Pop-up "Saya Tertarik dan Ingin Nego" — submit-nya juga di-mock kalau backend tidak tersedia, supaya demo tetap bisa dipakai untuk portfolio.

```javascript
const handleOrder = async (e) => {
  e.preventDefault();
  try {
    await axios.post(url, {...}, { timeout: 3000 });
    nav('/buyer/logged/sent/' + item.id);
  } catch (error) {
    // Backend tidak tersedia → tampilkan success demo
    setSubmitted(true);   // show ✅ Tawaran Terkirim screen
  }
};
```

### UI Improvements

- Cards di-refactor pakai Bootstrap `Row` + `Col` dengan `g-3` gap → uniform size, centered, responsive (xs=2, sm=3, md=4, lg=5 columns)
- Image aspect-ratio 1:1, object-fit cover → konsisten
- Hover lift effect + price warna merah
- Detail page: foto carousel, profile penjual, deskripsi panjang
- Success modal: layout proper dengan CSS module classes (no inline style yang konflik)

---

## 5. Stockop / jStock

**Repo:** [JerrelAdriel/jstockop-teknik](https://github.com/JerrelAdriel/jstockop-teknik)
**Tech Stack:** Next.js 14, React, TypeScript, Tailwind CSS, NextUI

### What it is

Sistem manajemen stok untuk **Gudang Teknik Pelabuhan Belawan (Pelindo Multi Terminal)** — proyek internship Jerrel saat Magenta MSIB (Oct 2023 – Aug 2024). Multi-user role (admin/user), CRUD barang, sistem peminjaman & pengambilan barang.

### Updates yang dilakukan

#### 1. Login Page — Responsive + Modern

**Before:**
- Fixed grid `grid-cols-2` (tidak responsive)
- Inline class numbers tidak responsive (`ml-40`, `w-9/12`, `right-36`)

**After:**
- Mobile-first: `grid-cols-1 lg:grid-cols-2`
- Responsive padding & font sizes (`p-4 sm:p-6 lg:p-16`)
- Modern card design dengan gradient bg & shadow
- Right side: hero image dengan overlay branding "jStock"

#### 2. Demo Mode Login

API backend dummy hosted di Vercel sering sleep. Solusi: tambah dummy credentials check **sebelum** call API.

```typescript
const handleLogin = async (event) => {
  event.preventDefault();
  if ((username === 'admin' && password === 'admin123') ||
      (username === 'user'  && password === 'user123')) {
    localStorage.setItem('token', 'dummy-admin-token-preview');
    setTimeout(() => router.push(
      username === 'admin' ? '/pages/admin/dashboard' : '/pages/users/home'
    ), 200);
    return;
  }
  // ... try real API
};
```

#### 3. Dummy Data Peminjaman & Pengambilan

**File:** `client/app/dummyData.ts`

- **DUMMY_LOANS** — 12 data peminjaman (Bor Listrik, Welding Machine, Tang, Kunci Pas, Gerinda, Multimeter, Helm Safety, Gergaji, Obeng Set, Compressor, Senter, Palu) dengan info lengkap: peminjam, spek alat, jumlah, lokasi, waktu peminjaman/pengembalian, status
- **DUMMY_TAKEN** — 11 data pengambilan barang konsumable (Sarung Tangan, Kawat Las, Cat Anti Karat, Mata Bor, Mata Gerinda, Kabel, Masker N95, Mur Baut, Oli Shell, Lakban, Lem)

```typescript
const handleDataLoan = async () => {
  const token = localStorage.getItem('token');
  if (isDummyToken(token)) {
    setDataLoan(DUMMY_LOANS as any);
    setCountDataLoan(DUMMY_LOANS.length);
    return;
  }
  try {
    const response = await axios.get(API_URL, { headers: { Authorization: `Bearer ${token}` } });
    // ... process response
  } catch (error) {
    setDataLoan(DUMMY_LOANS as any);   // fallback
  }
};
```

#### 4. UI/UX Beautification

**Sebelum:**
- Sidebar putih besar, area utama biru (`bg-primary-400`) dengan ruang kosong banyak
- Table di card kecil di tengah blue space
- Sidebar badges (NextUI Badge) overflow ke main content area

**Sesudah:**
- Sidebar gradient slate (subtle), area utama gradient blue subtle, tabel di card putih bersih
- 3 stats cards di atas tabel (Total / In Progress / Selesai) dengan colored numbers
- Header dengan subtitle descriptive ("Kelola permintaan peminjaman alat & barang teknik")
- Custom inline counter (bukan NextUI Badge) supaya tidak overflow:

```tsx
function Counter({ value, color }) {
  if (!value) return null;
  const bg = color === 'primary' ? 'bg-blue-600' : 'bg-amber-500';
  return (
    <span className={`${bg} text-white text-xs font-bold
                      rounded-full min-w-[22px] h-[22px]
                      flex items-center justify-center px-1.5 ml-auto`}>
      {value}
    </span>
  );
}

<Button endContent={<Counter value={amountDataLoan} color="primary" />}>
  Peminjaman
</Button>
```

---

## 6. Jump Game

**Repo:** Di dalam portfolio repo: [`JerrelAdriel.github.io/script.js`](https://github.com/JerrelAdriel/JerrelAdriel.github.io)
**Tech Stack:** HTML5, CSS3, Vanilla JavaScript

### What it is

Browser game sederhana — karakter dino harus loncat menghindari rintangan. Awalnya simple game untuk belajar JS, sekarang full physics-based dengan double jump dan rintangan random.

### Updates major

#### Sebelum (simple):
- Single jump pakai CSS animation
- Rintangan statis muncul terus-menerus
- Game over pakai `alert()`
- Tidak responsive
- Tidak ada skor

#### Sesudah (full game):
- **Physics-based jumping** (gravity + velocity)
- **Double jump** (2x lompat sebelum mendarat)
- **Random obstacles**: 65% darat (crate), 35% udara (flying box yang harus double-jump)
- **Score counter** + **high score** di localStorage
- **Difficulty scaling**: speed naik per skor, spawn interval mengecil
- **Game over screen** proper dengan skor & high score
- **Responsive** + touch support untuk mobile
- **Keyboard support** (Space / ArrowUp)

### Code Highlights

#### Physics-based Jump

**Sebelum (CSS animation, kaku):**
```css
@keyframes lompat {
  0% { top: 100px } 20% { top: 70px } 40% { top: 60px } ...
}
```

**Sesudah (JS physics, smooth):**
```javascript
const GRAVITY = 0.7;
const JUMP_VELOCITY = 11.5;
const DOUBLE_JUMP_VELOCITY = 10;
const MAX_HEIGHT = 160;

let karakterY = 0;
let velocityY = 0;
let jumpsLeft = 2;

function jump() {
  if (!isPlaying || jumpsLeft <= 0) return;
  velocityY = (jumpsLeft === 2) ? JUMP_VELOCITY : DOUBLE_JUMP_VELOCITY;
  jumpsLeft--;
}

// Inside game loop (60fps via requestAnimationFrame)
function gameLoop(now) {
  if (karakterY > 0 || velocityY > 0) {
    velocityY -= GRAVITY * dt;
    karakterY += velocityY * dt;
    if (karakterY > MAX_HEIGHT) { karakterY = MAX_HEIGHT; velocityY = 0; }
    if (karakterY <= 0) {
      karakterY = 0; velocityY = 0;
      jumpsLeft = 2;  // reset saat mendarat
    }
  }
  karakter.style.transform = `translateY(${-karakterY}px)`;
  // ... obstacle update, collision check
}
```

**Kenapa lebih bagus:**
- Smooth karena setiap frame dihitung, bukan keyframe interpolation
- Bisa double jump dengan reset velocity di tengah udara
- Collision detection lebih akurat karena posisi exact diketahui setiap frame

#### Random Obstacle Spawn

```javascript
function spawnObstacle() {
  if (!isPlaying) return;
  // Hindari spawn terlalu dekat
  if (obstacles.length > 0) {
    const last = obstacles[obstacles.length - 1];
    if (last.x > game.offsetWidth - 220) return;
  }

  const type = Math.random() < 0.65 ? 'ground' : 'air';
  const el = document.createElement('div');
  el.className = 'rintangan ' + type;
  game.appendChild(el);

  obstacles.push({
    el, type,
    x: game.offsetWidth + 50,
    hitTop:    type === 'air' ? 80 : 0,
    hitHeight: type === 'air' ? 50 : 55,
    width:     type === 'air' ? 50 : 55,
  });
}
```

Rintangan air spawn di y=80 (tinggi single jump) → memaksa pemain pakai double jump untuk lewatinya.

#### Bug yang sempat ada: CSS Animation Conflict

Awalnya pakai 2 CSS animation dengan property `animation` yang sama, conflict:

```css
/* DULU - CONFLICT! */
.animasiJalan { animation: jalan 0.5s steps(8) infinite; }
.animasiLompat { animation: lompat 600ms cubic-bezier(...); }
/* Add both classes? animasiJalan menimpa animasiLompat! */
```

**Solusi:** Kombinasi keduanya dalam satu class — animation `jalan` (background-position) + `lompat` (transform). Property berbeda → tidak konflik.

```css
.animasiLompat {
  animation:
    jalan 0.5s steps(8) infinite,
    lompat 600ms cubic-bezier(0.33, 1, 0.68, 1);
}
@keyframes lompat {
  0%   { transform: translateY(0); }
  45%  { transform: translateY(-110px); }
  100% { transform: translateY(0); }
}
```

---

## 7. Infrastructure & Security

### GitHub Setup

| Repo | URL |
|---|---|
| Portfolio | [JerrelAdriel.github.io](https://github.com/JerrelAdriel/JerrelAdriel.github.io) |
| Agent-JR | [agent-jr](https://github.com/JerrelAdriel/agent-jr) |
| Brain Tumor | [brain-tumor-classification](https://github.com/JerrelAdriel/brain-tumor-classification) |
| Lelang Binar | [lelang-binar](https://github.com/JerrelAdriel/lelang-binar) |
| Stockop | [jstockop-teknik](https://github.com/JerrelAdriel/jstockop-teknik) |

### Deploy

- **Portfolio:** GitHub Pages (otomatis dari branch `main` → `https://jerreladriel.github.io`)

### Security Cleanup

#### Yang dilakukan:
1. **Revoke PAT lama** — Token `ghp_V7Jpy...` yang terexpose di chat → dihapus dari `github.com/settings/tokens`
2. **Generate token baru** — `Claude MCP Jerrel v2` dengan scope sama (repo, read:org, read:user)
3. **Update di 2 tempat:**
   - File `C:\Users\jerre\.claude\.mcp.json` (Claude MCP config)
   - Windows User Environment Variable `GITHUB_PERSONAL_ACCESS_TOKEN`
4. **Remote URLs cleanup** — Semua repo remote URL yang sebelumnya embed token sekarang plain HTTPS:
   ```
   # Before: https://JerrelAdriel:ghp_V7Jpy...@github.com/user/repo.git
   # After:  https://github.com/user/repo.git
   ```
5. **gh CLI auth** — Setup `gh auth setup-git` jadi credential helper → git operations tetap jalan tanpa token URL

### Benefit Setup Baru

- 🔑 **Token tidak pernah ke disk lagi** untuk git operations (sebelumnya tersimpan di `.git/config` tiap repo)
- 💻 **Multi-laptop friendly** — tinggal `gh auth login` di laptop lain, langsung bisa push
- 🔄 **Easier rotation** — kalau token compromised, revoke + buat baru via web UI, no need untuk hunt down `.git/config` di mana-mana

---

## 📊 Summary Statistics

| Metric | Count |
|---|---|
| Total project diupdate | 5 + portfolio = 6 |
| Bug fixed | 10+ |
| File baru dibuat | 25+ |
| Total commits | 15+ |
| Bahasa dipakai | JavaScript, TypeScript, Python, HTML, CSS |
| Frameworks | React, Next.js, FastAPI, Flask, Electron, react-bootstrap, NextUI, Tailwind |
| Tools | Puppeteer (screenshots), rembg (BG removal), gh CLI, GitHub MCP |

---

## 📝 Lessons Learned

1. **CSS Modules tidak scope element selectors** — Hindari `p { ... }`, `div { ... }`, `* { ... }` di file `*.module.css`. Selalu wrap dalam class parent supaya tidak leak ke seluruh app.

2. **Fallback patterns** — Untuk aplikasi yang depend ke external API/backend, selalu siapkan dummy data fallback. Membedakan production vs demo mode dengan special token (`dummy-admin-token-preview`) is a clean approach.

3. **Physics-based animation > CSS keyframes** untuk game-like interaction. Lebih kompleks tapi:
   - Smoother (60fps loop)
   - Collision detection lebih akurat
   - Bisa interrupt/modify mid-animation (e.g. double jump)

4. **Multi-platform AI deployment** — Satu backend serving multiple frontend (web, WhatsApp, desktop) lebih maintainable daripada 3 codebase terpisah. Streaming response (SSE) bikin UX terasa fast & responsive.

5. **Security best practice: rotate tokens, don't embed in URL.** Pakai credential helper (gh CLI / SSH key) supaya token tidak pernah ke-leak ke `.git/config`, history terminal, atau backup file.

---

**End of Documentation** · *Jerrel Adriel A Hutahaean* · *Juni 2026*

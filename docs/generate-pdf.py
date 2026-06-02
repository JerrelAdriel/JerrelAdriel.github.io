"""Generate PDF profesional dari DOCUMENTATION.md."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Preformatted,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = Path(__file__).parent / "Portfolio-Documentation.pdf"

# Colors
PURPLE = colors.HexColor("#7c3aed")
PURPLE_LIGHT = colors.HexColor("#a78bfa")
PURPLE_DIM = colors.HexColor("#ede9fe")
DARK = colors.HexColor("#1a1a2e")
GRAY = colors.HexColor("#6b7280")
LIGHT_GRAY = colors.HexColor("#f3f4f6")
CODE_BG = colors.HexColor("#1e1e2e")
CODE_TEXT = colors.HexColor("#e4e4e7")
GREEN = colors.HexColor("#10b981")
RED = colors.HexColor("#ef4444")
WHITE = colors.white

# ── Styles ─────────────────────────────────────────
def make_styles():
    return {
        'cover_title': ParagraphStyle('cover_title', fontSize=36, textColor=PURPLE,
            fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=8, leading=42),
        'cover_subtitle': ParagraphStyle('cover_subtitle', fontSize=15, textColor=GRAY,
            fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4, leading=22),
        'h1': ParagraphStyle('h1', fontSize=22, textColor=WHITE,
            fontName="Helvetica-Bold", spaceBefore=24, spaceAfter=12,
            backColor=PURPLE, leftIndent=-1*cm, rightIndent=-1*cm,
            borderPad=10, leading=28),
        'h2': ParagraphStyle('h2', fontSize=16, textColor=PURPLE,
            fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=10, leading=22),
        'h3': ParagraphStyle('h3', fontSize=13, textColor=DARK,
            fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6, leading=18),
        'body': ParagraphStyle('body', fontSize=10, textColor=DARK,
            fontName="Helvetica", spaceAfter=6, leading=16, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', fontSize=10, textColor=DARK,
            fontName="Helvetica", spaceAfter=4, leading=15,
            leftIndent=18, bulletIndent=2),
        'code': ParagraphStyle('code', fontSize=8.5, textColor=CODE_TEXT,
            fontName="Courier", spaceAfter=4, leading=12,
            backColor=CODE_BG, leftIndent=10, rightIndent=10, borderPad=8,
            spaceBefore=4),
        'note': ParagraphStyle('note', fontSize=9.5, textColor=DARK,
            fontName="Helvetica-Oblique", spaceAfter=8, leading=14,
            leftIndent=14, rightIndent=14, backColor=PURPLE_DIM, borderPad=8),
        'caption': ParagraphStyle('caption', fontSize=9, textColor=GRAY,
            fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=10),
    }

S = make_styles()

# ── Helpers ────────────────────────────────────────
def section_header(text):
    return [
        Spacer(1, 0.3*cm),
        Table([[Paragraph(f"&nbsp; {text}",
            ParagraphStyle('sh', fontSize=15, textColor=WHITE,
                fontName="Helvetica-Bold", leading=20))]],
            colWidths=[17*cm],
            style=TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), PURPLE),
                ("TOPPADDING", (0,0), (-1,-1), 10),
                ("BOTTOMPADDING", (0,0), (-1,-1), 10),
                ("LEFTPADDING", (0,0), (-1,-1), 14),
            ])
        ),
        Spacer(1, 0.3*cm),
    ]

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S['bullet'])

def body(text):
    return Paragraph(text, S['body'])

def note(text):
    return Paragraph(f"💡 <b>Note:</b> {text}", S['note'])

def code_block(text, lang='js'):
    """Block of code with monospace + background."""
    # Escape XML-like chars
    safe = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    safe = safe.replace(' ', '&nbsp;').replace('\n', '<br/>')
    return Paragraph(safe, S['code'])

def info_table(rows):
    """Two-column info table."""
    t = Table(rows, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("TEXTCOLOR", (0,0), (0,-1), PURPLE),
        ("TEXTCOLOR", (1,0), (1,-1), DARK),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [PURPLE_DIM, WHITE]),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    return t

def compare_table(before_after_rows):
    """Before vs After comparison table."""
    rows = [["Before", "After"]] + before_after_rows
    t = Table(rows, colWidths=[8.5*cm, 8.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), RED),
        ("BACKGROUND", (1,0), (1,0), GREEN),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
    ]))
    return t

# ── Document ───────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

story = []

# ── COVER ──────────────────────────────────────────
story.append(Spacer(1, 4*cm))
story.append(Paragraph("📚", ParagraphStyle('emoji', fontSize=64,
    alignment=TA_CENTER, leading=72)))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Portfolio & Projects", S['cover_title']))
story.append(Paragraph("Update Documentation", S['cover_subtitle']))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="40%", thickness=2, color=PURPLE,
    hAlign='CENTER'))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Jerrel Adriel A Hutahaean", S['cover_subtitle']))
story.append(Paragraph("Fullstack Developer · Jakarta, Indonesia", S['cover_subtitle']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Juni 2026", S['cover_subtitle']))
story.append(Spacer(1, 3*cm))

story.append(info_table([
    ["Email", "jerreladriel@gmail.com"],
    ["WhatsApp", "+62 812-6205-9002"],
    ["LinkedIn", "linkedin.com/in/jerrelhutahaean"],
    ["GitHub", "github.com/JerrelAdriel"],
    ["Portfolio Live", "https://jerreladriel.github.io"],
]))
story.append(PageBreak())

# ── TOC ────────────────────────────────────────────
story += section_header("Table of Contents")
toc_data = [
    ["1.", "Portfolio Website", "3"],
    ["2.", "Agent-JR — Multi-Platform AI Assistant", "5"],
    ["3.", "Brain Tumor Classification", "7"],
    ["4.", "Lelang Binar (Second Hand)", "9"],
    ["5.", "Stockop / jStock", "12"],
    ["6.", "Jump Game", "14"],
    ["7.", "Infrastructure & Security", "16"],
    ["", "Summary & Lessons Learned", "17"],
]
toc_t = Table(toc_data, colWidths=[1.5*cm, 13*cm, 2*cm])
toc_t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 11),
    ("TEXTCOLOR", (0,0), (0,-1), PURPLE),
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("TEXTCOLOR", (2,0), (2,-1), GRAY),
    ("ALIGN", (2,0), (2,-1), "RIGHT"),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LINEBELOW", (0,0), (-1,-2), 0.3, colors.HexColor("#e5e7eb")),
]))
story.append(toc_t)
story.append(PageBreak())

# ── 1. PORTFOLIO ───────────────────────────────────
story += section_header("1. Portfolio Website")
story.append(info_table([
    ["Repo", "JerrelAdriel/JerrelAdriel.github.io"],
    ["Live", "https://jerreladriel.github.io"],
    ["Tech Stack", "HTML5, CSS3, Vanilla JavaScript"],
    ["Total Sections", "Hero, About, Experience, Projects, Skills, Contact"],
]))

story.append(Paragraph("Apa yang Dibangun", S['h2']))
story.append(body(
    "Single-page portfolio dengan 6 section utama. Bilingual EN/ID dengan toggle, "
    "responsive untuk desktop & mobile, dark-mode, dengan animasi smooth. "
    "Lightbox gallery untuk preview screenshot tiap project."))

story.append(Paragraph("Key Features", S['h2']))
features = [
    ("Bilingual EN/ID toggle", "i18n.js — localStorage persistence, default EN"),
    ("Project lightbox gallery", "portfolio.js — keyboard nav, ESC close"),
    ("Smooth scroll navigation", "Anchor links + IntersectionObserver fade-in"),
    ("Photo transparent BG", "AI-processed via rembg (U²-Net model)"),
    ("Work Experience timeline", "Pulsing dot animation untuk current job"),
]
for name, desc in features:
    story.append(Table([[
        Paragraph(f"<b>{name}</b>", ParagraphStyle('fn', fontSize=10,
            textColor=PURPLE, fontName="Helvetica-Bold")),
        Paragraph(desc, ParagraphStyle('fd', fontSize=10,
            textColor=DARK, fontName="Helvetica")),
    ]], colWidths=[5*cm, 12*cm],
    style=TableStyle([
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("LINEBELOW", (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
    ])))

story.append(Paragraph("Code Highlight: Bilingual System", S['h2']))
story.append(body(
    "Pattern yang dipakai: <b>HTML attribute-based translation</b>. Element ditandai "
    "dengan <font name='Courier'>data-i=\"key\"</font>, lalu JavaScript replace innerHTML "
    "saat user toggle bahasa."))
story.append(code_block("""const TRANSLATIONS = {
  en: { 'about.title': 'About', /* ... */ },
  id: { 'about.title': 'Tentang', /* ... */ },
};

function applyLanguage(lang) {
  const dict = TRANSLATIONS[lang];
  document.querySelectorAll('[data-i]').forEach(el => {
    if (dict[el.dataset.i]) el.innerHTML = dict[el.dataset.i];
  });
  localStorage.setItem('portfolio_lang', lang);
}"""))
story.append(note(
    "Default English terlihat dari HTML asli → SEO-friendly. Vanilla JS tanpa framework. "
    "Tambah element baru? Cukup tambah data-i + key di dictionary."))

story.append(Paragraph("Code Highlight: Responsive Avatar Blur", S['h2']))
story.append(body(
    "Bug yang sempat terjadi: blur ungu di belakang foto profil tidak ikut foto "
    "saat resize. <b>Solusi:</b> pakai pseudo-element <font name='Courier'>::before</font> "
    "dengan padding-bottom trick untuk maintain aspect ratio square."))
story.append(code_block(""".avatar::before {
  content: '';
  position: absolute;
  width: 92%;
  padding-bottom: 92%;        /* bikin selalu square */
  top: 5%;
  left: 50%;
  transform: translateX(-50%);   /* centered horizontal */
  background: radial-gradient(circle at 50% 50%,
    rgba(124,58,237,0.4), transparent 65%);
  border-radius: 50%;
  z-index: -1;                /* di belakang foto */
}"""))
story.append(PageBreak())

# ── 2. AGENT-JR ────────────────────────────────────
story += section_header("2. Agent-JR — Multi-Platform AI Assistant")
story.append(info_table([
    ["Repo", "JerrelAdriel/agent-jr"],
    ["Tech Stack", "Python FastAPI, Node.js, Electron, HTML/JS"],
    ["AI Engine", "Claude (Anthropic) → Groq fallback"],
    ["Platforms", "Web · WhatsApp Bot · Desktop App"],
]))

story.append(Paragraph("Apa Itu?", S['h2']))
story.append(body(
    "AI assistant pribadi yang berjalan di <b>3 platform sekaligus</b> dengan satu backend "
    "FastAPI. Powered by Claude dengan fallback otomatis ke Groq Llama 3.1 kalau Claude "
    "tidak tersedia. Cocok sebagai showcase kemampuan integrasi multi-platform + AI API."))

story.append(Paragraph("Arsitektur", S['h2']))
story.append(code_block("""                   +----------------------+
                   |  Backend FastAPI     |
                   |  Claude -> Groq      |
                   +-+--------+--------+--+
                     |        |        |
              +------+        |        +------+
              v               v               v
        +----------+   +-----------+   +----------+
        | Web Chat |   | WhatsApp  |   | Desktop  |
        | (HTML/JS)|   | Bot (Node)|   |(Electron)|
        +----------+   +-----------+   +----------+"""))

story.append(Paragraph("Code Highlight: Fallback Claude → Groq", S['h2']))
story.append(code_block("""@app.post(\"/api/chat\")
async def chat(request: ChatRequest):
    # Coba Claude dulu (lebih bagus tapi berbayar)
    if anthropic_client:
        try:
            response = anthropic_client.messages.create(
                model=\"claude-haiku-4-5\",
                system=SYSTEM_PROMPT,
                messages=to_messages(request.messages)
            )
            return {\"reply\": response.content[0].text, \"source\": \"claude\"}
        except Exception as e:
            print(f\"[Claude gagal] {e} -> Groq...\")

    # Fallback ke Groq (gratis 14k req/hari)
    if groq_client:
        response = groq_client.chat.completions.create(
            model=\"llama-3.1-8b-instant\",
            messages=msgs
        )
        return {\"reply\": response.choices[0].message.content, \"source\": \"groq\"}"""))
story.append(note(
    "Try-catch + fallback = graceful degradation. Field <font name='Courier'>source</font> "
    "di response biar frontend tahu API mana yang dipakai (debug)."))

story.append(Paragraph("Code Highlight: WhatsApp Mention Detection", S['h2']))
story.append(body(
    "Di grup, bot hanya merespon kalau (a) di-tag, atau (b) pesannya di-reply. "
    "<b>Tricky:</b> WhatsApp Web sekarang punya 2 format ID (<font name='Courier'>"
    "@c.us</font> legacy + <font name='Courier'>@lid</font> baru). Solusi: pakai "
    "<font name='Courier'>msg.getMentions()</font> (resolved contacts) bukan raw IDs."))
story.append(code_block("""client.on(\"message\", async (msg) => {
  if (msg.from.endsWith(\"@g.us\")) {
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
  // ... proses pesan
});"""))

story.append(Paragraph("Code Highlight: Streaming Response (SSE)", S['h2']))
story.append(body(
    "Efek typing seperti ChatGPT — text muncul token-per-token. Backend pakai "
    "<b>Server-Sent Events</b>, frontend pakai ReadableStream."))
story.append(code_block("""const res = await fetch(`${API_URL}/chat/stream`, { /* ... */ });
const reader = res.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const chunk = decoder.decode(value);
  for (const line of chunk.split(\"\\n\")) {
    if (line.startsWith(\"data: \")) {
      const { text } = JSON.parse(line.slice(6));
      fullReply += text;
      bubble.innerHTML = renderMarkdown(fullReply);
    }
  }
}"""))
story.append(PageBreak())

# ── 3. BRAIN TUMOR ─────────────────────────────────
story += section_header("3. Brain Tumor Classification")
story.append(info_table([
    ["Repo", "JerrelAdriel/brain-tumor-classification"],
    ["Tech Stack", "Python Flask, TensorFlow, VGG16 CNN"],
    ["Akurasi Model", "95%+"],
    ["Origin", "Thesis S1 — Universitas Sriwijaya"],
]))

story.append(Paragraph("Apa yang Dilakukan", S['h2']))
story.append(body(
    "Aplikasi klasifikasi <b>tumor otak dari gambar MRI</b> menggunakan deep learning. "
    "Model VGG16 dengan transfer learning, akurasi >95%. Ini dari penelitian thesis S1 di "
    "Universitas Sriwijaya (IPK 3.55)."))

story.append(Paragraph("Updates Major", S['h2']))
story.append(compare_table([
    ["UI Bootstrap default, look kuno", "Dark theme modern dengan cyan accent"],
    ["Form upload simple <input type='file'>", "Drag & drop zone dengan file preview"],
    ["Landing page minimal", "Hero + stats cards + features grid"],
    ["Hasil text biasa", "Color-coded badge (red/green)"],
]))

story.append(Paragraph("Code Highlight: Drag & Drop Upload", S['h2']))
story.append(code_block("""['dragover','dragenter'].forEach(ev =>
  dropZone.addEventListener(ev, e => {
    e.preventDefault();
    dropZone.classList.add('dragover');   // highlight saat hover
  })
);

dropZone.addEventListener('drop', e => {
  const f = e.dataTransfer.files[0];
  if (f) {
    fileInput.files = e.dataTransfer.files;
    showFile(f);   // preview + enable submit
  }
});"""))

story.append(Paragraph("UX Flow", S['h2']))
for step in [
    "User drag file → drop zone highlight cyan",
    "Drop → file preview muncul (thumbnail + nama + size)",
    "Button \"Analisis Sekarang\" enabled",
    "Submit → POST ke /predict Flask endpoint",
    "Hasil ditampilkan dengan badge color-coded",
]:
    story.append(bullet(step))
story.append(PageBreak())

# ── 4. LELANG BINAR ────────────────────────────────
story += section_header("4. Lelang Binar (Second Hand)")
story.append(info_table([
    ["Repo", "JerrelAdriel/lelang-binar"],
    ["Tech Stack", "React.js, React Bootstrap, Node.js, JWT"],
    ["Origin", "Final Project Binar Academy (2022)"],
    ["Repo Type", "Monorepo (frontend + backend)"],
]))

story.append(Paragraph("Bugs yang Diperbaiki", S['h2']))

story.append(Paragraph("Bug 1: CardComponent crash saat belum login", S['h3']))
story.append(body("<font name='Courier'>jwt-decode</font> throw error kalau input null."))
story.append(code_block("""// BEFORE — crash
const token = localStorage.getItem('token');
const decode = jwt(token);   // crash kalau token null

// AFTER — safe
const token = localStorage.getItem('token');
let decode = null;
try { if (token) decode = jwt(token); } catch (e) { /* ignore */ }"""))

story.append(Paragraph("Bug 2: Halaman gak bisa di-scroll", S['h3']))
story.append(code_block("""/* BEFORE — overflow blocked semua scroll */
body { overflow: hidden; }

/* AFTER — horizontal hidden saja */
body { overflow-x: hidden; overflow-y: auto; }"""))

story.append(Paragraph("Bug 3: p { height: 20px } leak ke semua &lt;p&gt;", S['h3']))
story.append(body(
    "<b>Root cause:</b> CSS Modules <b>hanya scope class selector</b>, bukan element selector. "
    "Aturan <font name='Courier'>p { ... }</font> di file <font name='Courier'>*.module.css</font> "
    "apapun, akan <b>leak ke seluruh app</b>."))
story.append(code_block("""/* BEFORE — leak global */
p { height: 20px; }

/* AFTER — scoped ke parent class */
.button p { height: 20px; }"""))
story.append(note(
    "Ini bug yang menyebabkan text overlap di success modal nego. Setelah fix, "
    "semua &lt;p&gt; di app render proper dengan natural height."))

story.append(Paragraph("Fitur Baru: Dummy Data Fallback", S['h2']))
story.append(body(
    "Backend hosted di Vercel free tier sering sleep. Solusi: <b>auto fallback ke dummy data</b>. "
    "File <font name='Courier'>src/dummyProducts.js</font> berisi 12 produk lengkap "
    "dengan nama, harga IDR, kategori, deskripsi panjang, profile penjual, "
    "1-3 gambar produk dari Unsplash."))
story.append(code_block("""const getProducts = async () => {
  try {
    const res = await axios.get(url, { timeout: 3000 });
    if (res?.data?.data?.product?.length) {
      setItems(res.data.data.product);
    } else {
      setItems(DUMMY_PRODUCTS);
    }
  } catch (error) {
    setItems(DUMMY_PRODUCTS);   // backend down -> dummy
  }
};"""))

story.append(Paragraph("UI Refactor: Card Grid", S['h2']))
story.append(body(
    "Cards di-refactor pakai Bootstrap Row + Col dengan g-3 gap → uniform size, "
    "centered, responsive (xs=2 → sm=3 → md=4 → lg=5 columns). Hover lift effect, "
    "image aspect-ratio 1:1 cover, price warna merah."))
story.append(PageBreak())

# ── 5. STOCKOP ─────────────────────────────────────
story += section_header("5. Stockop / jStock — Gudang Teknik")
story.append(info_table([
    ["Repo", "JerrelAdriel/jstockop-teknik"],
    ["Tech Stack", "Next.js 14, React, TypeScript, Tailwind, NextUI"],
    ["Origin", "Internship Magenta MSIB di PT Pelindo (2023-2024)"],
    ["Architecture", "Monorepo: client (Next.js) + server"],
]))

story.append(Paragraph("Apa Itu?", S['h2']))
story.append(body(
    "Sistem manajemen stok untuk <b>Gudang Teknik Pelabuhan Belawan</b> "
    "(PT Pelindo Multi Terminal). Multi-user role (admin/user), CRUD barang, "
    "sistem peminjaman & pengambilan barang."))

story.append(Paragraph("Updates", S['h2']))

story.append(Paragraph("1. Login Page — Responsive + Modern", S['h3']))
story.append(compare_table([
    ["Fixed grid-cols-2 (tidak responsive)", "Mobile-first: grid-cols-1 lg:grid-cols-2"],
    ["Inline class numbers (ml-40, w-9/12)", "Responsive padding & font sizes"],
    ["Standard form", "Modern gradient bg, hero image overlay"],
]))

story.append(Paragraph("2. Demo Mode Login (tanpa backend)", S['h3']))
story.append(code_block("""const handleLogin = async (event) => {
  event.preventDefault();
  if ((username === 'admin' && password === 'admin123') ||
      (username === 'user'  && password === 'user123')) {
    localStorage.setItem('token', 'dummy-admin-token-preview');
    router.push(username === 'admin'
      ? '/pages/admin/dashboard'
      : '/pages/users/home');
    return;
  }
  // ... try real API
};"""))

story.append(Paragraph("3. Dummy Data 12 Peminjaman + 11 Pengambilan", S['h3']))
story.append(body(
    "File <font name='Courier'>client/app/dummyData.ts</font> berisi data realistis: "
    "Bor Listrik Bosch, Welding Machine Lakoni, Tang Kombinasi Tekiro, Helm Safety MSA, "
    "dst — dengan info peminjam, spek alat, jumlah, lokasi proyek, waktu, status."))
story.append(code_block("""const handleDataLoan = async () => {
  const token = localStorage.getItem('token');
  if (isDummyToken(token)) {
    setDataLoan(DUMMY_LOANS);
    return;
  }
  try {
    const response = await axios.get(API_URL, { headers: { ... } });
    // ...
  } catch (error) {
    setDataLoan(DUMMY_LOANS);   // fallback
  }
};"""))

story.append(Paragraph("4. UI Beautification", S['h3']))
story.append(compare_table([
    ["Sidebar putih, area utama biru, banyak ruang kosong",
     "Gradient slate sidebar, tabel di card putih"],
    ["NextUI Badge overflow ke main content",
     "Custom inline Counter — clean placement"],
    ["Tidak ada stats overview",
     "3 stats cards: Total/In Progress/Selesai"],
]))
story.append(PageBreak())

# ── 6. JUMP GAME ───────────────────────────────────
story += section_header("6. Jump Game")
story.append(info_table([
    ["Repo", "JerrelAdriel.github.io (in main repo)"],
    ["Tech Stack", "HTML5, CSS3, Vanilla JavaScript"],
    ["Type", "Browser game (no framework)"],
]))

story.append(Paragraph("Updates Major", S['h2']))
story.append(compare_table([
    ["Single jump pakai CSS animation", "Physics-based jumping (gravity + velocity)"],
    ["Tidak ada double jump", "Double jump (2x sebelum mendarat)"],
    ["Rintangan statis terus-menerus", "Random: 65% darat, 35% udara (need double jump)"],
    ["Game over alert() popup", "Proper game over screen dengan skor"],
    ["Tidak ada skor", "Score + high score di localStorage"],
    ["Tidak responsive", "Responsive + touch support mobile"],
]))

story.append(Paragraph("Code Highlight: Physics-based Jump", S['h2']))
story.append(code_block("""const GRAVITY = 0.7;
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
    if (karakterY <= 0) {
      karakterY = 0;
      jumpsLeft = 2;   // reset saat mendarat
    }
  }
  karakter.style.transform = `translateY(${-karakterY}px)`;
}"""))
story.append(note(
    "Kenapa physics > CSS animation? Smooth karena per-frame calculation, "
    "collision detection lebih akurat, bisa interrupt mid-air untuk double jump."))

story.append(Paragraph("Code Highlight: Random Obstacles", S['h2']))
story.append(code_block("""function spawnObstacle() {
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
    el, type, x: game.offsetWidth + 50,
    hitTop:    type === 'air' ? 80 : 0,   // air = di tinggi single jump
    hitHeight: type === 'air' ? 50 : 55,
    width:     type === 'air' ? 50 : 55,
  });
}"""))
story.append(body(
    "Rintangan <b>air</b> spawn di y=80 (tinggi single jump) → memaksa pemain "
    "pakai double jump untuk lewatinya."))
story.append(PageBreak())

# ── 7. INFRASTRUCTURE ──────────────────────────────
story += section_header("7. Infrastructure & Security")

story.append(Paragraph("GitHub Repositories", S['h2']))
story.append(info_table([
    ["Portfolio", "github.com/JerrelAdriel/JerrelAdriel.github.io"],
    ["Agent-JR", "github.com/JerrelAdriel/agent-jr"],
    ["Brain Tumor", "github.com/JerrelAdriel/brain-tumor-classification"],
    ["Lelang Binar", "github.com/JerrelAdriel/lelang-binar"],
    ["Stockop", "github.com/JerrelAdriel/jstockop-teknik"],
]))

story.append(Paragraph("Security Cleanup", S['h2']))
story.append(body(
    "Token <font name='Courier'>ghp_V7Jpy...</font> awalnya tertulis di chat (terexpose). "
    "Cleanup yang dilakukan:"))
for step in [
    "Revoke PAT lama di github.com/settings/tokens",
    "Generate token baru \"Claude MCP Jerrel v2\" dengan scope sama (repo, read:org, read:user)",
    "Update token di 2 tempat: <font name='Courier'>.mcp.json</font> + Windows User Env Var",
    "Bersihkan remote URL semua repo (sebelumnya embed token dalam URL)",
    "Setup <font name='Courier'>gh CLI</font> sebagai git credential helper",
]:
    story.append(bullet(step))

story.append(Paragraph("Benefit Setup Baru", S['h2']))
story.append(bullet("Token <b>tidak pernah ke disk lagi</b> untuk git operations"))
story.append(bullet("<b>Multi-laptop friendly</b> — tinggal <font name='Courier'>gh auth login</font> di laptop lain"))
story.append(bullet("<b>Easier rotation</b> — revoke + buat baru via web UI, no need hunt down .git/config"))

# ── SUMMARY ────────────────────────────────────────
story += section_header("Summary & Lessons Learned")

story.append(Paragraph("Statistics", S['h2']))
stats_t = Table([
    ["Project diupdate", "5 + portfolio = 6"],
    ["Bug fixed", "10+"],
    ["File baru dibuat", "25+"],
    ["Total commits", "15+"],
    ["Languages", "JavaScript, TypeScript, Python, HTML, CSS"],
    ["Frameworks", "React, Next.js, FastAPI, Flask, Electron, Bootstrap, NextUI, Tailwind"],
    ["Tools", "Puppeteer, rembg, gh CLI, GitHub MCP"],
], colWidths=[5*cm, 12*cm])
stats_t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("TEXTCOLOR", (0,0), (0,-1), PURPLE),
    ("TEXTCOLOR", (1,0), (1,-1), DARK),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [PURPLE_DIM, WHITE]),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
]))
story.append(stats_t)

story.append(Paragraph("Lessons Learned", S['h2']))

lessons = [
    ("CSS Modules tidak scope element selectors",
     "Hindari <font name='Courier'>p { ... }</font>, <font name='Courier'>div { ... }</font>, "
     "<font name='Courier'>* { ... }</font> di file <font name='Courier'>*.module.css</font>. "
     "Selalu wrap dalam class parent supaya tidak leak ke seluruh app."),
    ("Fallback patterns untuk demo",
     "Untuk aplikasi yang depend ke external API/backend, selalu siapkan dummy data "
     "fallback. Special token (<font name='Courier'>dummy-admin-token-preview</font>) "
     "untuk distinguish demo vs production mode."),
    ("Physics-based animation > CSS keyframes",
     "Untuk game-like interaction: lebih kompleks tapi smoother (60fps), collision "
     "detection lebih akurat, bisa interrupt mid-animation (e.g. double jump)."),
    ("Multi-platform AI deployment",
     "Satu backend serving multiple frontend (web, WhatsApp, desktop) lebih maintainable "
     "daripada 3 codebase terpisah. SSE streaming bikin UX terasa fast."),
    ("Security best practice",
     "Pakai credential helper (gh CLI / SSH key) supaya token tidak pernah ter-leak "
     "ke <font name='Courier'>.git/config</font>, terminal history, atau backup."),
]
for i, (title, desc) in enumerate(lessons, 1):
    story.append(Paragraph(f"{i}. {title}", S['h3']))
    story.append(body(desc))

# Footer
story.append(Spacer(1, 1*cm))
story.append(HRFlowable(width="100%", thickness=1, color=PURPLE))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "End of Documentation &nbsp;·&nbsp; Jerrel Adriel A Hutahaean &nbsp;·&nbsp; Juni 2026",
    ParagraphStyle('footer', fontSize=9, textColor=GRAY,
        fontName="Helvetica", alignment=TA_CENTER)))

doc.build(story)
print(f"PDF berhasil dibuat: {OUTPUT}")
print(f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB")

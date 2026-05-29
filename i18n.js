// ── BILINGUAL SUPPORT ─────────────────────────
// Default: English. Toggle in nav switches to Indonesian.
// Translations saved in localStorage.

const TRANSLATIONS = {
  en: {
    // Nav
    'nav.about':       'About',
    'nav.experience':  'Experience',
    'nav.projects':    'Projects',
    'nav.skills':      'Skills',
    'nav.contact':     'Contact',

    // Hero
    'hero.badge':       'Available for work',
    'hero.tagline':     'Fullstack Developer & AI Enthusiast',
    'hero.desc':        "Building modern web applications, intelligent bots, and AI systems that run across multiple platforms. Passionate about technology that delivers real impact.",
    'hero.btnProjects': 'View Projects',
    'hero.btnContact':  'Contact Me',

    // About
    'about.tag':      'About Me',
    'about.title':    'About',
    'about.badge2':   '💼 Fullstack @ Huawei',
    'about.greeting': "Hi, I'm Jerrel Adriel 👋",
    'about.p1':       "Jakarta-based Fullstack Developer with over a year of professional experience building and maintaining web & mobile applications. Currently contributing to the <b>Surge</b> project at PT Huawei Tech Investment as part of XL Axiata's transformation into XLSMART.",
    'about.p2':       "Graduate of <b>Informatics Engineering at Universitas Sriwijaya</b> (GPA 3.55) with research experience in deep learning–based brain tumor image classification. Skilled in JavaScript, React, Node.js, Express, Java, and Python — with strong interests in web development, system integration, and machine learning.",
    'about.stat1':    'Year Experience',
    'about.stat2':    'Projects',
    'about.stat3':    'GPA / 4.00',

    // Experience
    'exp.tag':              'Career Journey',
    'exp.title':            'Work Experience',
    'exp.subtitle':         'My professional career path',
    'exp.surge.period':     'Apr 2026 — Present',
    'exp.surge.desc':       'Developing an internal JavaScript-based application for the NOC (Network Operations Center) for monitoring & operational response.',
    'exp.surge.list':       '<li>Enhance the <b>Incident Ticket</b> feature to auto-generate when an alarm goes down</li><li>Implemented <b>WhatsApp auto notification</b> for Incident Tickets — faster response time</li><li>Built a dynamic <b>Excel Reporting</b> feature filtered per user data</li>',
    'exp.xlsmart.period':   'Aug 2024 — Mar 2026',
    'exp.xlsmart.desc':     'Key contributor on the revamp of XL Axiata web & mobile into XLSMART, improving UX and integration with external systems.',
    'exp.xlsmart.list':     '<li>Led the revamp of <b>XLHome</b> web & mobile — UX & UI overhaul</li><li>Revamped <b>XLDrive</b> web & mobile for the XL sales team</li><li>Developed <b>Campaign Management</b> (pop-ups, banners, push notifications) for sales</li><li>Led <b>API integration</b> with OCR & the Indonesian Tax Directorate (DJP) for NPWP validation</li><li>Developed <b>Points Management</b> integrated with banks & e-wallets</li><li>Designed & implemented a <b>Development Tracking System</b> for documentation management</li><li>Enhanced the <b>Trouble Ticketing System</b> & provided application troubleshooting support</li>',
    'exp.intern.title':     'IT Operation Support — Internship (Magenta)',
    'exp.intern.period':    'Oct 2023 — Aug 2024',
    'exp.intern.desc':      'Internship under the <b>Magenta</b> program in the IT division — operational support and internal application development for the Engineering Warehouse.',
    'exp.intern.list':      '<li>Provided technical support for troubleshooting internal software & hardware</li><li>Developed a web-based application <b>(Stockop / jStock)</b> for asset monitoring & utilization in Gudang Teknik</li>',

    // Projects
    'proj.tag':         'Portfolio',
    'proj.title':       'Projects',
    'proj.subtitle':    "Some of the projects I've built",
    'proj.featured':    'Featured',
    'proj.viewPreview': '🔍 View Preview',
    'proj.preview':     'Preview',
    'proj.playNow':     '🎮 Play Now',
    'proj.agentjr.desc': 'Multi-platform personal AI assistant with automatic fallback from Claude → Groq. Available as a website, WhatsApp bot, and desktop app.',
    'proj.brain.desc':   'Web app for brain tumor classification from MRI images using deep learning (VGG16). High accuracy in detecting tumor types.',
    'proj.lelang.desc':  'A second-hand auction e-commerce app. Users can list products, place bids, and manage transactions. Final project at Binar Academy.',
    'proj.stockop.desc': 'Stock management system for Gudang Teknik Branch Belawan. Inventory dashboard, reports, Excel export, and multi-user roles.',
    'proj.game.desc':    'HTML5 browser game with physics-based jumping, double jump, random obstacles (ground/air), and localStorage high score.',

    // Skills
    'skills.tag':      'Expertise',
    'skills.title':    'Skills',
    'skills.subtitle': 'Technologies I work with',

    // Contact
    'contact.tag':      'Get in Touch',
    'contact.title':    'Contact',
    'contact.subtitle': "Let's collaborate or just have a chat",
    'contact.btn':      'Send Email',

    // Footer
    'footer.text': '© 2026 Jerrel Adriel · Fullstack Developer & AI Enthusiast',
    'footer.sub':  'Built with ❤️ and lots of ☕',
  },

  id: {
    // Nav
    'nav.about':       'Tentang',
    'nav.experience':  'Pengalaman',
    'nav.projects':    'Proyek',
    'nav.skills':      'Keahlian',
    'nav.contact':     'Kontak',

    // Hero
    'hero.badge':       'Tersedia untuk bekerja',
    'hero.tagline':     'Fullstack Developer & AI Enthusiast',
    'hero.desc':        'Membangun aplikasi web modern, bot cerdas, dan sistem AI yang berjalan di berbagai platform. Passionate tentang teknologi yang memberikan dampak nyata.',
    'hero.btnProjects': 'Lihat Proyek',
    'hero.btnContact':  'Hubungi Saya',

    // About
    'about.tag':      'Tentang Saya',
    'about.title':    'Tentang',
    'about.badge2':   '💼 Fullstack @ Huawei',
    'about.greeting': 'Halo, saya Jerrel Adriel 👋',
    'about.p1':       'Fullstack Developer berbasis di Jakarta dengan pengalaman lebih dari satu tahun membangun dan memelihara aplikasi web & mobile. Saat ini saya berkontribusi di proyek <b>Surge</b> (PT Huawei Tech Investment) sebagai bagian dari transformasi XL Axiata menjadi XLSMART.',
    'about.p2':       'Lulusan <b>Teknik Informatika Universitas Sriwijaya</b> (IPK 3.55) dengan riset deep learning untuk klasifikasi citra tumor otak. Saya skilled di JavaScript, React, Node.js, Express, Java, dan Python — dengan minat kuat di web development, system integration, dan ML.',
    'about.stat1':    'Tahun Pengalaman',
    'about.stat2':    'Proyek',
    'about.stat3':    'IPK / 4.00',

    // Experience
    'exp.tag':              'Perjalanan Karir',
    'exp.title':            'Pengalaman Kerja',
    'exp.subtitle':         'Perjalanan karir profesional saya',
    'exp.surge.period':     'Apr 2026 — Sekarang',
    'exp.surge.desc':       'Mengembangkan aplikasi internal berbasis JavaScript di area NOC (Network Operations Center) untuk monitoring & response operasional.',
    'exp.surge.list':       '<li>Enhance fitur <b>Incident Ticket</b> agar otomatis ter-generate saat alarm down</li><li>Implementasi <b>auto notification WhatsApp</b> untuk Incident Ticket — response time lebih cepat</li><li>Build fitur <b>Reporting Excel</b> dinamis sesuai filter data user</li>',
    'exp.xlsmart.period':   'Agu 2024 — Mar 2026',
    'exp.xlsmart.desc':     'Kontributor utama pada revamp web & mobile XL Axiata menjadi XLSMART, meningkatkan UX dan integrasi dengan sistem eksternal.',
    'exp.xlsmart.list':     '<li>Lead revamp <b>XLHome</b> web & mobile — UX & UI overhaul</li><li>Revamp <b>XLDrive</b> web & mobile untuk tim sales XL</li><li>Develop <b>Campaign Management</b> (pop-up, banner, push notification) untuk sales</li><li>Lead <b>API integration</b> dengan OCR & Direktorat Jenderal Pajak (DJP) untuk validasi NPWP</li><li>Develop <b>Points Management</b> integrasi dengan bank & e-wallet</li><li>Design & implement <b>Development Tracking System</b> untuk manajemen dokumentasi</li><li>Enhance <b>Trouble Ticketing System</b> & support troubleshooting aplikasi</li>',
    'exp.intern.title':     'IT Operation Support — Magang (Magenta)',
    'exp.intern.period':    'Okt 2023 — Agu 2024',
    'exp.intern.desc':      'Magang program <b>Magenta</b> di divisi IT — support operasional dan development aplikasi internal untuk Gudang Teknik.',
    'exp.intern.list':      '<li>Memberikan technical support untuk troubleshoot software & hardware internal</li><li>Develop web-based application <b>(Stockop / jStock)</b> untuk monitoring & utilisasi aset Gudang Teknik</li>',

    // Projects
    'proj.tag':         'Portofolio',
    'proj.title':       'Proyek',
    'proj.subtitle':    'Beberapa proyek yang telah saya bangun',
    'proj.featured':    'Unggulan',
    'proj.viewPreview': '🔍 Lihat Preview',
    'proj.preview':     'Preview',
    'proj.playNow':     '🎮 Main Sekarang',
    'proj.agentjr.desc': 'AI asisten pribadi multi-platform dengan fallback otomatis Claude → Groq. Tersedia sebagai website, WhatsApp bot, dan desktop app.',
    'proj.brain.desc':   'Aplikasi web untuk klasifikasi tumor otak dari gambar MRI menggunakan deep learning (VGG16). Akurasi tinggi untuk deteksi jenis tumor.',
    'proj.lelang.desc':  'Aplikasi e-commerce lelang barang bekas. Pengguna bisa list produk, melakukan penawaran, dan kelola transaksi. Final project Binar Academy.',
    'proj.stockop.desc': 'Sistem manajemen stok untuk Gudang Teknik Branch Belawan. Dashboard inventori, laporan, ekspor Excel, dan multi-user role.',
    'proj.game.desc':    'Browser game HTML5 dengan physics-based jumping, double jump, rintangan random (darat/terbang), dan high score localStorage.',

    // Skills
    'skills.tag':      'Keahlian',
    'skills.title':    'Keahlian',
    'skills.subtitle': 'Teknologi yang saya gunakan',

    // Contact
    'contact.tag':      'Hubungi Saya',
    'contact.title':    'Kontak',
    'contact.subtitle': 'Mari berkolaborasi atau sekedar ngobrol',
    'contact.btn':      'Kirim Email',

    // Footer
    'footer.text': '© 2026 Jerrel Adriel · Fullstack Developer & AI Enthusiast',
    'footer.sub':  'Dibuat dengan ❤️ dan banyak ☕',
  },
};

// ── APPLY LANGUAGE ──────────────────────────
function applyLanguage(lang) {
  const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;

  // Text content
  document.querySelectorAll('[data-i]').forEach(el => {
    const key = el.dataset.i;
    if (dict[key] != null) el.innerHTML = dict[key];
  });

  // HTML lists (with <li> nested)
  document.querySelectorAll('[data-i-html]').forEach(el => {
    const key = el.dataset.iHtml;
    if (dict[key] != null) el.innerHTML = dict[key];
  });

  // Update <html lang="">
  document.documentElement.lang = lang;

  // Update toggle button: highlight current language
  const cur = document.querySelector('.lang-current');
  const oth = document.querySelector('.lang-other');
  if (cur && oth) {
    cur.textContent = lang.toUpperCase();
    oth.textContent = (lang === 'en' ? 'id' : 'en').toUpperCase();
  }

  localStorage.setItem('portfolio_lang', lang);
}

// ── INIT ────────────────────────────────────
const savedLang = localStorage.getItem('portfolio_lang') || 'en';
applyLanguage(savedLang);

document.addEventListener('DOMContentLoaded', () => {
  // Re-apply in case some elements weren't ready
  applyLanguage(localStorage.getItem('portfolio_lang') || 'en');

  const toggle = document.getElementById('lang-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = localStorage.getItem('portfolio_lang') || 'en';
      applyLanguage(current === 'en' ? 'id' : 'en');
    });
  }
});

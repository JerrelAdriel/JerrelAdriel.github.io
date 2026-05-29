// Safety guard — only run on jump-game page
if (!document.getElementById('game') || !document.getElementById('karakter')) {
  // Not on game page, do nothing
} else { (() => {

// ── ELEMENTS ─────────────────────────────────────
const game         = document.getElementById('game');
const karakter     = document.getElementById('karakter');
const overlay      = document.getElementById('overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayInfo  = document.getElementById('overlay-info');
const startBtn     = document.getElementById('start-btn');
const scoreEl      = document.getElementById('score-val');
const highEl       = document.getElementById('high-val');
const sound        = document.getElementById('sound');

// ── STATE ────────────────────────────────────────
let isPlaying     = false;
let score         = 0;
let highScore     = parseInt(localStorage.getItem('jumpgame_high') || '0');
let speed         = 4.5;            // px per frame, increase over time
let obstacles     = [];             // active obstacles
let lastObstacleTime = 0;
let lastFrameTime = 0;

// Karakter physics
let karakterY    = 0;               // vertical position (0 = ground)
let velocityY    = 0;
let jumpsLeft    = 2;               // double jump!
const GRAVITY      = 0.7;
const JUMP_VELOCITY = 11.5;
const DOUBLE_JUMP_VELOCITY = 10;
const MAX_HEIGHT = 160;

highEl.textContent = highScore;

// ── GAME LOOP ────────────────────────────────────
function gameLoop(now) {
  if (!isPlaying) return;

  const dt = lastFrameTime ? (now - lastFrameTime) / 16.67 : 1;
  lastFrameTime = now;

  // ── Physics karakter ──
  if (karakterY > 0 || velocityY > 0) {
    velocityY -= GRAVITY * dt;
    karakterY += velocityY * dt;
    if (karakterY > MAX_HEIGHT) {
      karakterY = MAX_HEIGHT;
      velocityY = 0;
    }
    if (karakterY <= 0) {
      karakterY = 0;
      velocityY = 0;
      jumpsLeft = 2; // reset on landing
    }
  }
  karakter.style.transform = `translateY(${-karakterY}px)`;

  // ── Spawn obstacle ──
  const spawnInterval = Math.max(900, 1800 - score * 3);
  if (now - lastObstacleTime > spawnInterval) {
    spawnObstacle();
    lastObstacleTime = now;
  }

  // ── Update obstacles ──
  const gameWidth = game.offsetWidth;
  for (let i = obstacles.length - 1; i >= 0; i--) {
    const ob = obstacles[i];
    ob.x -= speed * dt;
    ob.el.style.transform = `translateX(${ob.x}px)`;

    // Remove off-screen
    if (ob.x < -100) {
      ob.el.remove();
      obstacles.splice(i, 1);
      continue;
    }

    // Collision detection
    if (checkCollision(ob)) {
      gameOver();
      return;
    }
  }

  // ── Score + difficulty ──
  if (Math.floor(now / 100) % 2 === 0 && !window._scoredThisTick) {
    score++;
    scoreEl.textContent = score;
    speed = Math.min(11, 4.5 + score * 0.02);
    window._scoredThisTick = true;
  } else if (Math.floor(now / 100) % 2 !== 0) {
    window._scoredThisTick = false;
  }

  requestAnimationFrame(gameLoop);
}

// ── OBSTACLE SPAWNING ────────────────────────────
function spawnObstacle() {
  const type = Math.random() < 0.65 ? 'ground' : 'air';

  // If last obstacle is too close, skip
  if (obstacles.length > 0) {
    const last = obstacles[obstacles.length - 1];
    if (last.x > game.offsetWidth - 220) return;
  }

  const el = document.createElement('div');
  el.className = 'rintangan ' + type;
  game.appendChild(el);

  obstacles.push({
    el,
    type,
    x: game.offsetWidth + 50,
    // For ground: hit zone is bottom 55px. For air: hit zone is at jump height
    hitTop: type === 'air' ? 80 : 0,
    hitHeight: type === 'air' ? 50 : 55,
    width: type === 'air' ? 50 : 55,
  });
}

// ── COLLISION ────────────────────────────────────
function checkCollision(ob) {
  const margin = 10;
  const karakterX = 60;        // fixed left position
  const karakterW = 50;
  const karakterH = 80;

  // Karakter X range
  const kLeft  = karakterX + margin;
  const kRight = karakterX + karakterW - margin;

  // Obstacle X range (relative to game)
  const oLeft  = ob.x;
  const oRight = ob.x + ob.width;

  // X overlap?
  if (kRight < oLeft || kLeft > oRight) return false;

  // Karakter Y range (from ground): 0 to karakterH
  // After jump: karakterY to karakterY + karakterH
  const kBottom = karakterY;
  const kTop    = karakterY + karakterH;

  // Obstacle Y range (from ground)
  const oBottom = ob.hitTop;
  const oTop    = ob.hitTop + ob.hitHeight;

  // Y overlap?
  if (kTop - margin < oBottom || kBottom + margin > oTop) return false;

  return true;
}

// ── ACTIONS ──────────────────────────────────────
function jump() {
  if (!isPlaying || jumpsLeft <= 0) return;
  // First jump: full power. Double jump: refresh momentum (smaller boost)
  velocityY = (jumpsLeft === 2) ? JUMP_VELOCITY : DOUBLE_JUMP_VELOCITY;
  jumpsLeft--;
}

function startGame() {
  if (isPlaying) return;
  isPlaying = true;
  score = 0;
  speed = 4.5;
  karakterY = 0;
  velocityY = 0;
  jumpsLeft = 2;
  lastObstacleTime = performance.now();
  lastFrameTime = 0;

  // Clear obstacles
  obstacles.forEach(o => o.el.remove());
  obstacles = [];

  scoreEl.textContent = '0';
  karakter.classList.add('animasiJalan');
  karakter.style.transform = 'translateY(0)';
  overlay.classList.add('hidden');

  try { sound.currentTime = 0; sound.play(); } catch(e) {}
  requestAnimationFrame(gameLoop);
}

function gameOver() {
  isPlaying = false;
  karakter.classList.remove('animasiJalan');
  try { sound.pause(); } catch(e) {}

  if (score > highScore) {
    highScore = score;
    localStorage.setItem('jumpgame_high', highScore);
    highEl.textContent = highScore;
  }

  overlayTitle.textContent = '💀 Game Over!';
  overlayInfo.innerHTML = `<div class="final-score">Skor: ${score}</div>` +
    `<div>High Score: ${highScore}</div>`;
  startBtn.textContent = 'Main Lagi';
  overlay.classList.remove('hidden');
}

// ── EVENT LISTENERS ──────────────────────────────
startBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  startGame();
});

document.addEventListener('keydown', (e) => {
  if (e.code === 'Space' || e.code === 'ArrowUp') {
    e.preventDefault();
    if (!isPlaying) startGame();
    else jump();
  }
});

game.addEventListener('click', (e) => {
  if (e.target.closest('#overlay')) return;
  if (isPlaying) jump();
});

game.addEventListener('touchstart', (e) => {
  if (e.target.closest('#overlay')) return;
  e.preventDefault();
  if (isPlaying) jump();
}, { passive: false });

})(); }

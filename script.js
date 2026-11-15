/**
 * ============================================================================
 * 💖 FOREVER & ALWAYS • ROMANTIC COUPLE PORTRAIT & LIVING ENVIRONMENT 💖
 * ============================================================================
 */

(function () {
  'use strict';

  // DOM Elements
  const photoCanvas = document.getElementById('photo-canvas');
  const penCanvas = document.getElementById('pen-canvas');
  const ambientCanvas = document.getElementById('ambient-canvas');
  const artistCursor = document.getElementById('artist-cursor');
  const statusText = document.getElementById('status-text');
  const portraitCard = document.getElementById('portrait-card');

  // Control Buttons
  const btnReplay = document.getElementById('btn-replay');
  const btnPause = document.getElementById('btn-pause');
  const btnSpeed = document.getElementById('btn-speed');
  const btnMusic = document.getElementById('btn-music');
  const btnDownload = document.getElementById('btn-download');
  const pauseIcon = document.getElementById('pause-icon');
  const pauseText = document.getElementById('pause-text');
  const speedText = document.getElementById('speed-text');
  const musicText = document.getElementById('music-text');

  // Canvas Contexts
  const pCtx = photoCanvas.getContext('2d');
  const penCtx = penCanvas.getContext('2d');
  const aCtx = ambientCanvas.getContext('2d');

  // Offscreen Mask Canvas for photographic reveal
  const maskCanvas = document.createElement('canvas');
  const maskCtx = maskCanvas.getContext('2d');

  const WIDTH = 620;
  const HEIGHT = 452;
  photoCanvas.width = WIDTH;
  photoCanvas.height = HEIGHT;
  penCanvas.width = WIDTH;
  penCanvas.height = HEIGHT;
  maskCanvas.width = WIDTH;
  maskCanvas.height = HEIGHT;

  // Load Images
  const imgOrig = new Image();
  imgOrig.src = 'portrait.jpg';

  const imgSketch = new Image();
  imgSketch.src = 'portrait_sketch.jpg';

  let imagesLoaded = 0;
  function onImageLoad() {
    imagesLoaded++;
    if (imagesLoaded === 2) {
      initApp();
    }
  }
  imgOrig.onload = onImageLoad;
  imgSketch.onload = onImageLoad;

  // Animation State
  const state = {
    act: 1,              // 1: Sketch, 2: Color Bloom, 3: Living Romantic Mode
    paused: false,
    speedMultiplier: 1,  // 1x or 2x
    pathIndex: 0,
    pointIndex: 0,
    spiralIndex: 0,
    spiralTheta: 0,
    spiralFaceIdx: 0,
    sweepIndex: 0,
    musicPlaying: false
  };

  // Romantic Floating Hearts & Fairy Lights
  const floatingHearts = [];
  const fairyLights = [];
  const burstHearts = [];

  const ROMANTIC_COLORS = [
    { fill: '#ff2a85', stroke: '#e11d48' },
    { fill: '#fb7185', stroke: '#f43f5e' },
    { fill: '#ff758f', stroke: '#ff4d6d' },
    { fill: '#e11d48', stroke: '#9f1239' },
    { fill: '#fbbf24', stroke: '#f59e0b' },
    { fill: '#c084fc', stroke: '#9333ea' },
    { fill: '#ffffff', stroke: '#f43f5e' }
  ];

  // Resize Ambient Canvas with Device Pixel Ratio Support
  function resizeAmbientCanvas() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    ambientCanvas.width = window.innerWidth * dpr;
    ambientCanvas.height = window.innerHeight * dpr;
    aCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener('resize', resizeAmbientCanvas);
  window.addEventListener('orientationchange', () => setTimeout(resizeAmbientCanvas, 150));
  resizeAmbientCanvas();

  // Initialize Fairy Lights
  for (let i = 0; i < 45; i++) {
    fairyLights.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      r: 1.5 + Math.random() * 2.5,
      phase: Math.random() * Math.PI * 2,
      speed: 0.03 + Math.random() * 0.05,
      color: ['#fef08a', '#fde047', '#fed7aa', '#f472b6', '#e0e7ff'][Math.floor(Math.random() * 5)]
    });
  }

  // Initialize 35 Floating Hearts in Background
  for (let i = 0; i < 35; i++) {
    floatingHearts.push(createFloatingHeart(true));
  }

  function createFloatingHeart(randomY = false) {
    const pal = ROMANTIC_COLORS[Math.floor(Math.random() * ROMANTIC_COLORS.length)];
    return {
      x: Math.random() * window.innerWidth,
      y: randomY ? Math.random() * window.innerHeight : window.innerHeight + 30,
      size: 0.45 + Math.random() * 0.65,
      angle: (Math.random() - 0.5) * 35,
      vy: 1.2 + Math.random() * 2.2,
      swayAmp: 15 + Math.random() * 25,
      swayFreq: 0.02 + Math.random() * 0.04,
      phase: Math.random() * Math.PI * 2,
      fill: pal.fill,
      stroke: pal.stroke
    };
  }

  // Draw Heart Path on Canvas
  function drawHeartPath(ctx, cx, cy, size, angleDeg = 0) {
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate((angleDeg * Math.PI) / 180);
    ctx.beginPath();
    for (let deg = 0; deg < 360; deg += 12) {
      const rad = (deg * Math.PI) / 180;
      const hx = size * 16 * Math.pow(Math.sin(rad), 3);
      const hy = -size * (13 * Math.cos(rad) - 5 * Math.cos(2 * rad) - 2 * Math.cos(3 * rad) - Math.cos(4 * rad));
      if (deg === 0) {
        ctx.moveTo(hx, hy);
      } else {
        ctx.lineTo(hx, hy);
      }
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }

  // Position the virtual artist cursor
  function setCursor(x, y, visible = true, mode = 'pen') {
    if (!visible) {
      artistCursor.style.display = 'none';
      return;
    }
    artistCursor.style.display = 'block';
    const rect = photoCanvas.getBoundingClientRect();
    const scaleX = rect.width / WIDTH;
    const scaleY = rect.height / HEIGHT;

    artistCursor.style.left = `${x * scaleX}px`;
    artistCursor.style.top = `${y * scaleY}px`;

    const nib = artistCursor.querySelector('.cursor-nib');
    if (mode === 'brush') {
      nib.style.background = '#fbbf24';
      nib.style.borderRadius = '50%';
      nib.style.transform = 'scale(1.2)';
    } else {
      nib.style.background = '#e11d48';
      nib.style.borderRadius = '50% 50% 50% 0';
      nib.style.transform = 'rotate(-45deg)';
    }
  }

  // =========================================================================
  // ACT 1: VECTOR SILHOUETTE SKETCH
  // =========================================================================
  function renderPhotoComposite() {
    pCtx.clearRect(0, 0, WIDTH, HEIGHT);
    // Draw sketch as underlayer
    pCtx.drawImage(imgSketch, 0, 0, WIDTH, HEIGHT);

    if (state.act >= 2) {
      // Composite color image using reveal mask
      pCtx.save();
      pCtx.globalCompositeOperation = 'source-over';

      // Draw revealed parts of color image
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = WIDTH;
      tempCanvas.height = HEIGHT;
      const tCtx = tempCanvas.getContext('2d');

      tCtx.drawImage(imgOrig, 0, 0, WIDTH, HEIGHT);
      tCtx.globalCompositeOperation = 'destination-in';
      tCtx.drawImage(maskCanvas, 0, 0, WIDTH, HEIGHT);

      pCtx.drawImage(tempCanvas, 0, 0, WIDTH, HEIGHT);
      pCtx.restore();
    }
  }

  function startAct1() {
    state.act = 1;
    state.pathIndex = 0;
    state.pointIndex = 0;
    statusText.innerText = 'Act 1/3: Sketching Facial Silhouettes & Romantic Outlines...';

    // Clear canvases
    penCtx.clearRect(0, 0, WIDTH, HEIGHT);
    maskCtx.clearRect(0, 0, WIDTH, HEIGHT);
    renderPhotoComposite();
  }

  function stepAct1() {
    const paths = window.SKETCH_DATA ? window.SKETCH_DATA.paths : [];
    if (!paths || paths.length === 0) {
      startAct2();
      return;
    }

    const stepsPerFrame = 3 * state.speedMultiplier;

    penCtx.lineWidth = 1.3;
    penCtx.lineCap = 'round';
    penCtx.lineJoin = 'round';
    penCtx.strokeStyle = '#2d3748';

    for (let s = 0; s < stepsPerFrame; s++) {
      if (state.pathIndex >= paths.length) {
        startAct2();
        return;
      }

      const path = paths[state.pathIndex];
      if (!path || path.length < 2) {
        state.pathIndex++;
        state.pointIndex = 0;
        continue;
      }

      if (state.pointIndex === 0) {
        state.pointIndex = 1;
      }

      const p0 = path[state.pointIndex - 1];
      const p1 = path[state.pointIndex];

      penCtx.beginPath();
      penCtx.moveTo(p0[0], p0[1]);
      penCtx.lineTo(p1[0], p1[1]);
      penCtx.stroke();

      setCursor(p1[0], p1[1], true, 'pen');

      state.pointIndex++;
      if (state.pointIndex >= path.length) {
        state.pathIndex++;
        state.pointIndex = 0;
      }
    }
  }

  // =========================================================================
  // ACT 2: MAGIC WATERCOLOR COLOR BLOOM
  // =========================================================================
  let sweepList = [];

  function startAct2() {
    state.act = 2;
    state.spiralIndex = 0;
    state.spiralTheta = 0;
    state.spiralFaceIdx = 0;
    state.sweepIndex = 0;
    statusText.innerText = '🎨 Act 2/3: Magic Color Paintbrush — Revealing 100% Crystal-Clear Photo...';

    // Completely clear preliminary sketch lines so faces remain 100% clean!
    penCtx.clearRect(0, 0, WIDTH, HEIGHT);

    // Prepare sweep points across attire and background
    sweepList = [];
    for (let y = Math.floor(HEIGHT * 0.65); y < HEIGHT; y += 36) {
      const isEven = Math.floor(y / 36) % 2 === 0;
      if (isEven) {
        for (let x = 20; x < WIDTH - 20; x += 45) sweepList.push({ x, y });
      } else {
        for (let x = WIDTH - 20; x > 20; x -= 45) sweepList.push({ x, y });
      }
    }
    for (let x = 30; x < WIDTH - 30; x += 50) {
      sweepList.push({ x, y: 30 });
    }
  }

  function applyDab(x, y, radius = 46) {
    const radGrad = maskCtx.createRadialGradient(x, y, radius * 0.3, x, y, radius);
    radGrad.addColorStop(0, 'rgba(255,255,255,1)');
    radGrad.addColorStop(1, 'rgba(255,255,255,1)');

    maskCtx.fillStyle = radGrad;
    maskCtx.beginPath();
    maskCtx.arc(x, y, radius, 0, Math.PI * 2);
    maskCtx.fill();

    renderPhotoComposite();
    setCursor(x, y, true, 'brush');
  }

  function stepAct2() {
    const faces = window.SKETCH_DATA ? window.SKETCH_DATA.face_centers : [];

    // Spiral 1 & 2: Faces
    if (state.spiralFaceIdx < faces.length) {
      const face = faces[state.spiralFaceIdx];
      const maxTheta = 5.5 * Math.PI;
      const dTheta = 0.35 * state.speedMultiplier;

      state.spiralTheta += dTheta;
      const r = (state.spiralTheta / maxTheta) * (face.radius + 20);
      const bx = face.cx + r * Math.cos(state.spiralTheta);
      const by = face.cy + r * Math.sin(state.spiralTheta);

      applyDab(bx, by, 48);

      if (state.spiralTheta >= maxTheta) {
        state.spiralFaceIdx++;
        state.spiralTheta = 0;
      }
      return;
    }

    // Sweep: Attire & Background
    if (state.sweepIndex < sweepList.length) {
      const sweepsPerFrame = Math.max(1, Math.round(2 * state.speedMultiplier));
      for (let i = 0; i < sweepsPerFrame; i++) {
        if (state.sweepIndex < sweepList.length) {
          const pt = sweepList[state.sweepIndex];
          applyDab(pt.x, pt.y, 65);
          state.sweepIndex++;
        }
      }
      return;
    }

    // Finish Act 2: Complete 100% Photographic Clarity
    maskCtx.fillStyle = '#ffffff';
    maskCtx.fillRect(0, 0, WIDTH, HEIGHT);
    renderPhotoComposite();
    setCursor(0, 0, false);
    startAct3();
  }

  // =========================================================================
  // ACT 3: LIVING ROMANTIC ENVIRONMENT
  // =========================================================================
  function startAct3() {
    state.act = 3;
    statusText.innerText = '💖 Forever & Always • Pure Photographic Clarity & Living Hearts 💖';

    // Clear pen canvas just in case
    penCtx.clearRect(0, 0, WIDTH, HEIGHT);
    setCursor(0, 0, false);
  }

  // =========================================================================
  // INTERACTIVE BURST HEARTS (CLICK / TOUCH)
  // =========================================================================
  function triggerHeartBurst(clientX, clientY) {
    const numHearts = 10;
    for (let i = 0; i < numHearts; i++) {
      const pal = ROMANTIC_COLORS[Math.floor(Math.random() * ROMANTIC_COLORS.length)];
      burstHearts.push({
        x: clientX,
        y: clientY,
        vx: (Math.random() - 0.5) * 6,
        vy: -3.0 - Math.random() * 5.0,
        size: 0.5 + Math.random() * 0.7,
        angle: (Math.random() - 0.5) * 45,
        rotSpeed: (Math.random() - 0.5) * 4,
        life: 50,
        maxLife: 50,
        fill: pal.fill,
        stroke: pal.stroke
      });
    }

    // Play subtle soft chime if music active
    playChime();
  }

  window.addEventListener('click', (e) => {
    // Ignore button clicks
    if (e.target.closest('.controls-bar')) return;
    triggerHeartBurst(e.clientX, e.clientY);
  });

  window.addEventListener('touchstart', (e) => {
    if (e.target.closest('.controls-bar')) return;
    if (e.touches && e.touches[0]) {
      triggerHeartBurst(e.touches[0].clientX, e.touches[0].clientY);
    }
  }, { passive: true });

  // =========================================================================
  // ROMANTIC AMBIENT HARP / CHIME SYNTHESIZER (WEB AUDIO API)
  // =========================================================================
  let audioCtx = null;
  const CHORD_NOTES = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99, 1046.50]; // C Major Romantic Pentatonic

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playChime(freq = null) {
    if (!state.musicPlaying) return;
    try {
      const ctx = getAudioContext();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      const note = freq || CHORD_NOTES[Math.floor(Math.random() * CHORD_NOTES.length)];
      osc.type = 'sine';
      osc.frequency.setValueAtTime(note, ctx.currentTime);

      gain.gain.setValueAtTime(0.001, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.08, ctx.currentTime + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.2);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 1.25);
    } catch (e) {
      // Audio error ignored
    }
  }

  let musicInterval = null;
  function toggleMusic() {
    state.musicPlaying = !state.musicPlaying;
    if (state.musicPlaying) {
      musicText.innerText = 'Music: On 🎵';
      btnMusic.classList.add('btn-primary');
      getAudioContext();

      // Play soft arpeggio chords
      let noteIdx = 0;
      musicInterval = setInterval(() => {
        if (!state.musicPlaying) return;
        playChime(CHORD_NOTES[noteIdx % CHORD_NOTES.length]);
        noteIdx++;
      }, 700);
    } else {
      musicText.innerText = 'Music: Off';
      btnMusic.classList.remove('btn-primary');
      if (musicInterval) {
        clearInterval(musicInterval);
        musicInterval = null;
      }
    }
  }

  // =========================================================================
  // MAIN ANIMATION LOOP
  // =========================================================================
  function renderAmbient() {
    aCtx.clearRect(0, 0, window.innerWidth, window.innerHeight);

    // 1. Draw Twinkling Fairy Lights
    fairyLights.forEach((fl) => {
      fl.phase += fl.speed;
      const r = fl.r * (0.75 + 0.35 * Math.sin(fl.phase));
      aCtx.fillStyle = fl.color;
      aCtx.beginPath();
      aCtx.arc(fl.x, fl.y, r, 0, Math.PI * 2);
      aCtx.fill();
    });

    // 2. Draw Floating Romantic Hearts
    floatingHearts.forEach((fh) => {
      if (!state.paused) {
        fh.y -= fh.vy;
        fh.phase += fh.swayFreq;
        if (fh.y < -40) {
          fh.y = window.innerHeight + 40;
          fh.x = Math.random() * window.innerWidth;
        }
      }
      const curX = fh.x + fh.swayAmp * Math.sin(fh.phase);
      aCtx.fillStyle = fh.fill;
      aCtx.strokeStyle = fh.stroke;
      aCtx.lineWidth = 1.2;
      drawHeartPath(aCtx, curX, fh.y, fh.size, fh.angle);
    });

    // 3. Draw Click Burst Hearts
    for (let i = burstHearts.length - 1; i >= 0; i--) {
      const bh = burstHearts[i];
      if (!state.paused) {
        bh.x += bh.vx;
        bh.y += bh.vy;
        bh.vy += 0.08; // gentle gravity
        bh.angle += bh.rotSpeed;
        bh.life--;
      }

      const alpha = Math.max(0, bh.life / bh.maxLife);
      aCtx.save();
      aCtx.globalAlpha = alpha;
      aCtx.fillStyle = bh.fill;
      aCtx.strokeStyle = bh.stroke;
      aCtx.lineWidth = 1.5;
      drawHeartPath(aCtx, bh.x, bh.y, bh.size, bh.angle);
      aCtx.restore();

      if (bh.life <= 0 || bh.y > window.innerHeight + 50) {
        burstHearts.splice(i, 1);
      }
    }
  }

  function animationLoop() {
    renderAmbient();

    if (!state.paused) {
      if (state.act === 1) {
        stepAct1();
      } else if (state.act === 2) {
        stepAct2();
      }
    }

    requestAnimationFrame(animationLoop);
  }

  // =========================================================================
  // BUTTON HANDLERS
  // =========================================================================
  btnReplay.addEventListener('click', () => {
    startAct1();
  });

  btnPause.addEventListener('click', () => {
    state.paused = !state.paused;
    if (state.paused) {
      pauseText.innerText = 'Resume';
      pauseIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"/>';
    } else {
      pauseText.innerText = 'Pause';
      pauseIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
    }
  });

  btnSpeed.addEventListener('click', () => {
    if (state.speedMultiplier === 1) {
      state.speedMultiplier = 2.2;
      speedText.innerText = '2x Speed';
      btnSpeed.classList.add('btn-primary');
    } else {
      state.speedMultiplier = 1;
      speedText.innerText = '1x Speed';
      btnSpeed.classList.remove('btn-primary');
    }
  });

  btnMusic.addEventListener('click', toggleMusic);

  btnDownload.addEventListener('click', () => {
    // Save crystal clear original image
    const link = document.createElement('a');
    link.download = 'Forever_and_Always_Portrait.jpg';
    link.href = 'portrait.jpg';
    link.click();
  });

  // Start the entire experience
  function initApp() {
    startAct1();
    requestAnimationFrame(animationLoop);
  }

})();

## 🎨 Particle-Inspired Animation (SVG + foreignObject)

<div align="center">

<!-- Particle system SVG (foreignObject + CSS animations) -->
<svg xmlns="http://www.w3.org/2000/svg" width="880" height="180" viewBox="0 0 880 180" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Particle animation">
  <style>
    /* Particle keyframes (varias amplitudes para variedad) */
    @keyframes floatA { 0% { transform: translateY(0); } 50% { transform: translateY(-22px); } 100% { transform: translateY(0); } }
    @keyframes floatB { 0% { transform: translateY(0); } 50% { transform: translateY(-14px); } 100% { transform: translateY(0); } }
    @keyframes floatC { 0% { transform: translateY(0); } 50% { transform: translateY(-28px); } 100% { transform: translateY(0); } }
    @keyframes floatD { 0% { transform: translateY(0); } 50% { transform: translateY(-18px); } 100% { transform: translateY(0); } }
    @keyframes flicker { 0% { opacity: .85; } 50% { opacity: .5; } 100% { opacity: .85; } }

    /* Base particle style (applied to inner divs) */
    .p {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      box-shadow: 0 0 10px rgba(255,255,255,0.06), 0 0 18px currentColor;
      display: block;
      transform-origin: center;
      will-change: transform, opacity;
    }
  </style>

  <!-- Partículas: x positions across the canvas. Each foreignObject contains an XHTML div. -->
  <!-- 1 -->
  <foreignObject x="30" y="80" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#FF6B6B;color:#FF6B6B; animation: floatA 3.4s ease-in-out infinite alternate; animation-delay: 0.0s;"></div>
    </div>
  </foreignObject>

  <!-- 2 -->
  <foreignObject x="90" y="90" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="width:10px;height:10px;background:#FFD93D;color:#FFD93D; opacity:.95; animation: floatB 2.6s ease-in-out infinite alternate; animation-delay: 0.15s;"></div>
    </div>
  </foreignObject>

  <!-- 3 -->
  <foreignObject x="150" y="75" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#6BCB77;color:#6BCB77; animation: floatC 4.0s ease-in-out infinite alternate; animation-delay: 0.05s;"></div>
    </div>
  </foreignObject>

  <!-- 4 -->
  <foreignObject x="210" y="88" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="width:14px;height:14px;background:#4D96FF;color:#4D96FF; opacity:.9; animation: floatD 2.9s ease-in-out infinite alternate; animation-delay: 0.25s;"></div>
    </div>
  </foreignObject>

  <!-- 5 -->
  <foreignObject x="270" y="82" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#C77DFF;color:#C77DFF; animation: floatA 3.6s ease-in-out infinite alternate; animation-delay: 0.4s;"></div>
    </div>
  </foreignObject>

  <!-- 6 -->
  <foreignObject x="330" y="95" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="width:9px;height:9px;background:#FF9F1C;color:#FF9F1C; opacity:.85; animation: floatB 2.4s ease-in-out infinite alternate; animation-delay: 0.1s;"></div>
    </div>
  </foreignObject>

  <!-- 7 -->
  <foreignObject x="390" y="72" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#6EE7B7;color:#6EE7B7; animation: floatC 3.8s ease-in-out infinite alternate; animation-delay: 0.3s;"></div>
    </div>
  </foreignObject>

  <!-- 8 -->
  <foreignObject x="450" y="86" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#7C83FD;color:#7C83FD; animation: floatD 2.7s ease-in-out infinite alternate; animation-delay: 0.18s;"></div>
    </div>
  </foreignObject>

  <!-- 9 -->
  <foreignObject x="510" y="92" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="width:11px;height:11px;background:#FFD3A5;color:#FFD3A5; opacity:.9; animation: floatA 3.2s ease-in-out infinite alternate; animation-delay: 0.08s;"></div>
    </div>
  </foreignObject>

  <!-- 10 -->
  <foreignObject x="570" y="78" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#9BE7FF;color:#9BE7FF; animation: floatB 2.5s ease-in-out infinite alternate; animation-delay: 0.22s;"></div>
    </div>
  </foreignObject>

  <!-- 11 -->
  <foreignObject x="630" y="84" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="width:13px;height:13px;background:#FF7AA2;color:#FF7AA2; animation: floatC 3.9s ease-in-out infinite alternate; animation-delay: 0.12s;"></div>
    </div>
  </foreignObject>

  <!-- 12 -->
  <foreignObject x="690" y="90" width="16" height="16">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="background:#B7FF9F;color:#B7FF9F; animation: floatD 2.8s ease-in-out infinite alternate; animation-delay: 0.28s;"></div>
    </div>
  </foreignObject>

  <!-- Optional subtle twinkle layer on top -->
  <foreignObject x="760" y="70" width="20" height="20">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div class="p" style="width:6px;height:6px;background:#FFF;color:#FFF; box-shadow:0 0 12px rgba(255,255,255,0.9); animation: flicker 1.8s linear infinite; animation-delay: 0.05s;"></div>
    </div>
  </foreignObject>

</svg>

</div>

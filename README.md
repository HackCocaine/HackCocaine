## 🎨 Particle-Inspired Animation (SVG — listo para GitHub)

<div align="center">

<!-- SVG particle system: SMIL animations (altamente compatible en README) -->
<svg xmlns="http://www.w3.org/2000/svg"
     width="880" height="180" viewBox="0 0 880 180"
     preserveAspectRatio="xMidYMid meet"
     role="img" aria-label="Smooth particle animation">

  <defs>
    <!-- subtle radial gradient for particles -->
    <radialGradient id="g1" cx="50%" cy="35%" r="60%">
      <stop offset="0%" stop-color="#fff" stop-opacity="1"/>
      <stop offset="35%" stop-color="#fff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </radialGradient>

    <!-- glow filter -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- easing helper via keySplines will be used in animate elements via calcMode="spline" -->
  </defs>

  <!-- Background (very subtle) -->
  <rect x="0" y="0" width="880" height="180" fill="transparent"></rect>

  <!-- Particles: circles with vertical float + slight horizontal drift, staggered -->
  <!-- 1 -->
  <circle cx="40" cy="92" r="6" fill="#FF6B6B" filter="url(#glow)">
    <animate attributeName="cy" values="92;64;92" dur="3.6s" begin="0s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="40;48;40" dur="10s" begin="0s" repeatCount="indefinite" />
  </circle>

  <!-- 2 -->
  <circle cx="110" cy="98" r="5" fill="#FFD93D" filter="url(#glow)" opacity="0.95">
    <animate attributeName="cy" values="98;84;98" dur="2.9s" begin="0.12s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="110;116;110" dur="9.5s" begin="0.12s" repeatCount="indefinite" />
  </circle>

  <!-- 3 -->
  <circle cx="180" cy="86" r="6.5" fill="#6BCB77" filter="url(#glow)">
    <animate attributeName="cy" values="86;58;86" dur="4.2s" begin="0.05s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="180;174;180" dur="11s" begin="0.05s" repeatCount="indefinite" />
  </circle>

  <!-- 4 -->
  <circle cx="250" cy="100" r="7" fill="#4D96FF" filter="url(#glow)" opacity="0.9">
    <animate attributeName="cy" values="100;82;100" dur="3.1s" begin="0.2s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="250;260;250" dur="8.8s" begin="0.2s" repeatCount="indefinite" />
  </circle>

  <!-- 5 -->
  <circle cx="320" cy="88" r="5.5" fill="#C77DFF" filter="url(#glow)" opacity="0.95">
    <animate attributeName="cy" values="88;60;88" dur="3.8s" begin="0.38s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="320;328;320" dur="10.6s" begin="0.38s" repeatCount="indefinite" />
  </circle>

  <!-- 6 -->
  <circle cx="390" cy="96" r="4.5" fill="#FF9F1C" filter="url(#glow)" opacity="0.85">
    <animate attributeName="cy" values="96;82;96" dur="2.6s" begin="0.15s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="390;384;390" dur="7.8s" begin="0.15s" repeatCount="indefinite" />
  </circle>

  <!-- 7 -->
  <circle cx="460" cy="74" r="6.2" fill="#6EE7B7" filter="url(#glow)">
    <animate attributeName="cy" values="74;48;74" dur="3.9s" begin="0.33s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="460;468;460" dur="12s" begin="0.33s" repeatCount="indefinite" />
  </circle>

  <!-- 8 -->
  <circle cx="530" cy="90" r="5.8" fill="#7C83FD" filter="url(#glow)">
    <animate attributeName="cy" values="90;72;90" dur="2.75s" begin="0.18s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="530;526;530" dur="9.2s" begin="0.18s" repeatCount="indefinite" />
  </circle>

  <!-- 9 -->
  <circle cx="600" cy="94" r="6" fill="#FFD3A5" filter="url(#glow)" opacity="0.9">
    <animate attributeName="cy" values="94;66;94" dur="3.2s" begin="0.08s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="600;608;600" dur="10.2s" begin="0.08s" repeatCount="indefinite" />
  </circle>

  <!-- 10 -->
  <circle cx="670" cy="80" r="5.2" fill="#9BE7FF" filter="url(#glow)" opacity="0.95">
    <animate attributeName="cy" values="80;64;80" dur="2.5s" begin="0.22s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="670;662;670" dur="8.6s" begin="0.22s" repeatCount="indefinite" />
  </circle>

  <!-- 11 -->
  <circle cx="740" cy="86" r="6.6" fill="#FF7AA2" filter="url(#glow)">
    <animate attributeName="cy" values="86;60;86" dur="3.95s" begin="0.12s" repeatCount="indefinite" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>
    <animate attributeName="cx" values="740;748;740" dur="11.8s" begin="0.12s" repeatCount="indefinite" />
  </circle>

  <!-- subtle twinkle -->
  <circle cx="820" cy="68" r="3" fill="#FFF" opacity="0.95" filter="url(#glow)">
    <animate attributeName="opacity" values="0.95;0.15;0.95" dur="1.8s" begin="0.05s" repeatCount="indefinite" />
    <animate attributeName="cy" values="68;60;68" dur="2.0s" begin="0.05s" repeatCount="indefinite"/>
  </circle>

</svg>

</div>

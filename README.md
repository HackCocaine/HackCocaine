## 🎨 Particle-Inspired Animation

<div align="center">

<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">

  <!-- Particle 1 -->
  <foreignObject x="0" y="40" width="10" height="10">
    <div xmlns="http://www.w3.org/1999/xhtml" style="
      width:10px; height:10px; border-radius:50%; background:#FF6B6B;
      animation: move1 3s ease-in-out infinite alternate;">
    </div>
  </foreignObject>

  <!-- Particle 2 -->
  <foreignObject x="50" y="40" width="10" height="10">
    <div xmlns="http://www.w3.org/1999/xhtml" style="
      width:10px; height:10px; border-radius:50%; background:#FFD93D;
      animation: move2 2.5s ease-in-out infinite alternate;">
    </div>
  </foreignObject>

  <!-- Particle 3 -->
  <foreignObject x="100" y="40" width="10" height="10">
    <div xmlns="http://www.w3.org/1999/xhtml" style="
      width:10px; height:10px; border-radius:50%; background:#6BCB77;
      animation: move3 3.2s ease-in-out infinite alternate;">
    </div>
  </foreignObject>

  <!-- Particle 4 -->
  <foreignObject x="150" y="40" width="10" height="10">
    <div xmlns="http://www.w3.org/1999/xhtml" style="
      width:10px; height:10px; border-radius:50%; background:#4D96FF;
      animation: move4 2.8s ease-in-out infinite alternate;">
    </div>
  </foreignObject>

  <style>
    @keyframes move1 { 0% {transform: translateY(0);} 50% {transform: translateY(-20px);} 100% {transform: translateY(0);} }
    @keyframes move2 { 0% {transform: translateY(0);} 50% {transform: translateY(-15px);} 100% {transform: translateY(0);} }
    @keyframes move3 { 0% {transform: translateY(0);} 50% {transform: translateY(-25px);} 100% {transform: translateY(0);} }
    @keyframes move4 { 0% {transform: translateY(0);} 50% {transform: translateY(-18px);} 100% {transform: translateY(0);} }
  </style>

</svg>

</div>

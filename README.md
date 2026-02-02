<!-- hackcocaine | Minimal Particle Animation Profile -->
<div align="center">

# ✨ hackcocaine

**Creative Developer | Particle Enthusiast | Minimalist Coder**

---

## 🎨 Live Particle Animation

<div id="particle-container" style="position:relative; height:300px; width:100%; max-width:800px; margin:0 auto; border:1px solid #2d2d2d; border-radius:8px; overflow:hidden; background:#0d1117;">
  <canvas id="particle-canvas"></canvas>
</div>

---

## 🛠️ Technologies & Tools

![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![Canvas API](https://img.shields.io/badge/-Canvas_API-FF6F61?style=flat&logo=html5&logoColor=white)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white)

---

## 📊 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=hackcocaine&show_icons=true&theme=radical&hide_border=true)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=hackcocaine&layout=compact&theme=radical&hide_border=true)

---

## 🔗 Connect With Me

[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/hackcocaine)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/hackcocaine)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/hackcocaine)

</div>

<!-- Particle Animation Script - No Dependencies Required -->
<script>
  // Canvas setup
  const canvas = document.getElementById('particle-canvas');
  const ctx = canvas.getContext('2d');
  const container = document.getElementById('particle-container');
  
  // Set canvas dimensions
  function resizeCanvas() {
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
  }
  
  // Initial resize
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  
  // Particle system
  const particles = [];
  const particleCount = 80;
  const mouse = { x: 0, y: 0, radius: 100 };
  
  // Track mouse position
  container.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });
  
  // Particle class
  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = Math.random() * 1 - 0.5;
      this.speedY = Math.random() * 1 - 0.5;
      this.color = `hsl(${Math.random() * 60 + 180}, 100%, 70%)`;
      this.originalSize = this.size;
    }
    
    update() {
      // Move particle
      this.x += this.speedX;
      this.y += this.speedY;
      
      // Mouse interaction
      const dx = mouse.x - this.x;
      const dy = mouse.y - this.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < mouse.radius) {
        const force = (mouse.radius - distance) / mouse.radius;
        const angle = Math.atan2(dy, dx);
        this.x -= Math.cos(angle) * force * 5;
        this.y -= Math.sin(angle) * force * 5;
        this.size = this.originalSize * 2;
      } else {
        this.size = Math.max(this.size * 0.95, this.originalSize);
      }
      
      // Bounce off edges
      if (this.x <= 0 || this.x >= canvas.width) this.speedX *= -1;
      if (this.y <= 0 || this.y >= canvas.height) this.speedY *= -1;
      
      // Keep within bounds
      this.x = Math.max(0, Math.min(canvas.width, this.x));
      this.y = Math.max(0, Math.min(canvas.height, this.y));
    }
    
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
    }
  }
  
  // Create particles
  function initParticles() {
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }
  }
  
  // Connect particles with lines
  function connectParticles() {
    const maxDistance = 100;
    
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < maxDistance) {
          const opacity = 1 - (distance / maxDistance);
          ctx.beginPath();
          ctx.strokeStyle = `rgba(100, 200, 255, ${opacity * 0.3})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }
  
  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Update and draw particles
    particles.forEach(particle => {
      particle.update();
      particle.draw();
    });
    
    // Connect particles
    connectParticles();
    
    requestAnimationFrame(animate);
  }
  
  // Initialize and start animation
  initParticles();
  animate();
</script>

<!-- Minimal CSS for better appearance -->
<style>
  #particle-container {
    transition: border-color 0.3s ease;
  }
  
  #particle-container:hover {
    border-color: #58a6ff;
  }
  
  #particle-canvas {
    display: block;
  }
</style>

---

*Particle animation inspired by Scalar's interactive elements. No dependencies required - works directly in GitHub README!*

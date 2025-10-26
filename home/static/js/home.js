const STAR_COLOR = '#fff';
const STAR_SIZE = 3;
const STAR_MIN_SCALE = 0.2;
const STAR_COUNT = (window.innerWidth + window.innerHeight) / 8;

// Global variables for default canvas
let defaultCanvas, defaultContext;
let scale = 1, width, height;
let stars = [];

// Initialize with default canvas (for backward compatibility)
function initDefault() {
  defaultCanvas = document.querySelector('canvas');
  if (defaultCanvas) {
    defaultContext = defaultCanvas.getContext('2d');
    generate();
    resize();
    step();
    window.onresize = resize;
  }
}

// Initialize with specific canvas (for dashboard)
function initStarField(canvas) {
  if (!canvas) return;
  
  const context = canvas.getContext('2d');
  const starField = createStarField(canvas, context);
  starField.start();
  
  // Resize handler for this specific canvas
  window.addEventListener('resize', () => starField.resize());
}

// Create a star field for a specific canvas
function createStarField(canvas, context) {
  let localStars = [];
  let animationId;
  
  return {
    start() {
      this.generateStars();
      this.resize();
      this.animate();
    },
    
    generateStars() {
      localStars = [];
      const starCount = Math.min(100, (canvas.width + canvas.height) / 8); // Limit stars for performance
      for (let i = 0; i < starCount; i++) {
        localStars.push({
          x: 0,
          y: 0,
          z: STAR_MIN_SCALE + Math.random() * (1 - STAR_MIN_SCALE),
          vx: (Math.random() - 0.5) * 0.1,
          vy: (Math.random() - 0.5) * 0.1
        });
      }
    },
    
    placeStar(star) {
      star.x = Math.random() * canvas.width;
      star.y = Math.random() * canvas.height;
    },
    
    resize() {
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
      localStars.forEach(star => this.placeStar(star));
    },
    
    animate() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      this.update();
      this.render();
      animationId = requestAnimationFrame(() => this.animate());
    },
    
    update() {
      localStars.forEach((star) => {
        star.x += star.vx;
        star.y += star.vy;

        // Wrap the stars around the screen edges
        if (star.x < 0) star.x = canvas.width;
        if (star.x > canvas.width) star.x = 0;
        if (star.y < 0) star.y = canvas.height;
        if (star.y > canvas.height) star.y = 0;
      });
    },
    
    render() {
      localStars.forEach((star) => {
        context.beginPath();
        context.lineCap = 'round';
        context.lineWidth = STAR_SIZE * star.z;
        context.globalAlpha = 0.5 + 0.5 * Math.random();
        context.strokeStyle = STAR_COLOR;

        context.moveTo(star.x, star.y);
        context.lineTo(star.x, star.y);

        context.stroke();
      });
    },
    
    stop() {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    }
  };
}

// Original functions for backward compatibility
function generate() {
   stars = [];
   for (let i = 0; i < STAR_COUNT; i++) {
       stars.push({
           x: 0,
           y: 0,
           z: STAR_MIN_SCALE + Math.random() * (1 - STAR_MIN_SCALE),
           vx: (Math.random() - 0.5) * 0.1,
           vy: (Math.random() - 0.5) * 0.1
       });
   }
}

function placeStar(star) {
   star.x = Math.random() * width;
   star.y = Math.random() * height;
}

function resize() {
   if (!defaultCanvas || !defaultContext) return;
   
   scale = window.devicePixelRatio || 1;
   width = window.innerWidth * scale;
   height = window.innerHeight * scale;

   defaultCanvas.width = width;
   defaultCanvas.height = height;

   stars.forEach(placeStar);
}

function step() {
   if (!defaultCanvas || !defaultContext) return;
   
   defaultContext.clearRect(0, 0, width, height);
   update();
   render();
   requestAnimationFrame(step);
}

function update() {
   stars.forEach((star) => {
       star.x += star.vx;
       star.y += star.vy;

       // Wrap the stars around the screen edges
       if (star.x < 0) star.x = width;
       if (star.x > width) star.x = 0;
       if (star.y < 0) star.y = height;
       if (star.y > height) star.y = 0;
   });
}

function render() {
   if (!defaultContext) return;
   
   stars.forEach((star) => {
       defaultContext.beginPath();
       defaultContext.lineCap = 'round';
       defaultContext.lineWidth = STAR_SIZE * star.z * scale;
       defaultContext.globalAlpha = 0.5 + 0.5 * Math.random();
       defaultContext.strokeStyle = STAR_COLOR;

       defaultContext.moveTo(star.x, star.y);
       defaultContext.lineTo(star.x, star.y);

       defaultContext.stroke();
   });
}

// Auto-initialize if there's a canvas on page load
document.addEventListener('DOMContentLoaded', initDefault);



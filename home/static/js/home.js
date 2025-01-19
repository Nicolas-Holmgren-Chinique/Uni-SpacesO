const STAR_COLOR = '#fff';
const STAR_SIZE = 3;
const STAR_MIN_SCALE = 0.2;
const STAR_COUNT = (window.innerWidth + window.innerHeight) / 8;

const canvas = document.querySelector('canvas'),
      context = canvas.getContext('2d');

let scale = 1, // device pixel ratio
    width,
    height;

let stars = [];

generate();
resize();
step();

window.onresize = resize;

function generate() {
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
   scale = window.devicePixelRatio || 1;

   width = window.innerWidth * scale;
   height = window.innerHeight * scale;

   canvas.width = width;
   canvas.height = height;

   stars.forEach(placeStar);
}

function step() {
   context.clearRect(0, 0, width, height);

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
   stars.forEach((star) => {
       context.beginPath();
       context.lineCap = 'round';
       context.lineWidth = STAR_SIZE * star.z * scale;
       context.globalAlpha = 0.5 + 0.5 * Math.random();
       context.strokeStyle = STAR_COLOR;

       context.moveTo(star.x, star.y);
       context.lineTo(star.x, star.y);

       context.stroke();
   });
}

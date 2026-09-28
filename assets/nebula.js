/* Merkorn: the nebula behind every page.
   A single full-screen fragment shader, rendered at native resolution.
   Each page sets data-seed on <body> so it sits in its own region of the cloud. */
(() => {
  const canvas = document.getElementById('sky');
  if (!canvas) return;
  const gl = canvas.getContext('webgl', { antialias: false, alpha: false, powerPreference: 'high-performance' });
  if (!gl) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const seed = parseFloat(document.body.dataset.seed || '0');

  const vs = `attribute vec2 p; void main(){ gl_Position = vec4(p, 0., 1.); }`;
  const fs = `
  precision highp float;
  uniform vec2 R; uniform float T, Z, V, C, S, W; uniform vec2 M;
  float h31(vec3 p){ p = fract(p * .1031); p += dot(p, p.yzx + 33.33); return fract((p.x + p.y) * p.z); }
  float h21(vec2 p){ vec3 q = fract(vec3(p.xyx) * .1031); q += dot(q, q.yzx + 33.33); return fract((q.x + q.y) * q.z); }
  float noise(vec3 x){
    vec3 i = floor(x), f = fract(x); f = f * f * (3. - 2. * f);
    return mix(mix(mix(h31(i), h31(i + vec3(1,0,0)), f.x), mix(h31(i + vec3(0,1,0)), h31(i + vec3(1,1,0)), f.x), f.y),
               mix(mix(h31(i + vec3(0,0,1)), h31(i + vec3(1,0,1)), f.x), mix(h31(i + vec3(0,1,1)), h31(i + vec3(1,1,1)), f.x), f.y), f.z);
  }
  float fbm(vec3 p){ float a = .5, s = 0.; for (int k = 0; k < 6; k++) { s += a * noise(p); p = p * 2.03 + vec3(1.7, 9.2, 3.1); a *= .5; } return s; }

  // stars streaming toward the viewer, three depth layers
  float stars(vec2 uv, float travel){
    float s = 0.;
    for (int L = 0; L < 3; L++) {
      float fl = float(L);
      float z = fract(fl / 3. + travel);
      float scale = mix(26., 1.2, z);
      vec2 g = uv * scale + fl * 17.3;
      vec2 id = floor(g), f = fract(g) - .5;
      float r = h21(id);
      vec2 o = vec2(h21(id + 3.1), h21(id + 7.7)) - .5;
      vec2 dp = f - o * .7;
      vec2 rd = normalize(uv + 1e-4);
      float d = length(vec2(dot(dp, rd) / (1. + W * 9. * z), dot(dp, vec2(-rd.y, rd.x))));
      float size = .018 + .05 * z * z;
      float fade = smoothstep(0., .25, z) * smoothstep(1., .75, z);
      float tw = .6 + .4 * sin(T * (1. + r * 3.) + r * 40.);
      s += step(.72, r) * smoothstep(size, 0., d) * fade * tw;
    }
    return s;
  }

  // a thin shooting star crosses the sky every few seconds
  float comet(vec2 uv){
    float slot = floor(T / 4.5), k = fract(T / 4.5);
    float r1 = h21(vec2(slot, 1.7)), r2 = h21(vec2(slot, 8.3)), r3 = h21(vec2(slot, 4.1));
    if (r3 < .35) return 0.;
    vec2 a = vec2(mix(-.9, .9, r1), mix(.1, .55, r2));
    vec2 dir = normalize(vec2(r1 > .5 ? -1. : 1., -.45 - r2 * .3));
    float life = smoothstep(0., .08, k) * smoothstep(.45, .2, k);
    vec2 head = a + dir * k * 1.6;
    vec2 pa = uv - head;
    float along = dot(pa, -dir), across = abs(dot(pa, vec2(-dir.y, dir.x)));
    float tail = smoothstep(.28, 0., along) * step(0., along);
    return tail * smoothstep(.0035, 0., across) * life;
  }

  void main(){
    vec2 uv = (gl_FragCoord.xy - .5 * R) / R.y;
    // forward travel: the field zooms slowly toward us, faster while scrolling
    float zoom = 1.25 - .12 * sin(Z * .35);
    vec2 q2 = uv * zoom + M * .12;
    float t = T * .035;
    vec3 p = vec3(q2 * 1.5 + vec2(S * 3.7, S * 1.9), Z * .55 + t + S * 11.);
    vec3 w = vec3(fbm(p + vec3(0., 0., t)), fbm(p + vec3(5.2, 1.3, -t)), 0.);
    float n = fbm(p + 1.9 * w + vec3(M * .25, 0.));
    float lanes = fbm(p * 2.2 + 4.0 * w.yxz);

    float dens = smoothstep(.38, .92, n + C * .22);
    dens *= .55 + .45 * smoothstep(.25, .7, lanes);

    vec3 bg   = vec3(.031, .027, .043);   // #08070B
    vec3 deep = vec3(.26, .10, .52);      // toward #6D28D9, dimmed
    vec3 acc  = vec3(.59, .28, 1.);       // #9747FF
    vec3 dust = vec3(.95, .94, .92);      // #F2EFEA

    vec3 col = bg;
    col = mix(col, deep, dens * .85);
    col = mix(col, acc, smoothstep(.62, 1., n + .15 * w.x) * .55 * (.4 + .6 * dens));
    col += dust * pow(smoothstep(.55, 1., lanes * n * 1.6), 3.) * .35;

    // crossing a cloud bank between sections: brighter, denser, then clear
    col = mix(col, mix(deep, dust, .25), C * .35 * smoothstep(.3, .9, n));

    col += dust * stars(uv, Z * .25 + T * .01 + V) * (.55 + .45 * (1. - dens));
    col += mix(dust, acc, .3) * comet(uv) * .9;

    // keep it quiet behind reading areas
    col *= .78;

    // sub-pixel dither, invisible, only to avoid banding in the dark gradients
    col += (h21(gl_FragCoord.xy) - .5) / 255.;
    gl_FragColor = vec4(col, 1.);
  }`;
  function sh(type, src) { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw gl.getShaderInfoLog(s); return s; }
  const prog = gl.createProgram();
  try { gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs)); } catch (e) { console.warn(e); return; }
  gl.linkProgram(prog); gl.useProgram(prog);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const U = n => gl.getUniformLocation(prog, n);
  const uR = U('R'), uT = U('T'), uZ = U('Z'), uV = U('V'), uC = U('C'), uM = U('M'), uS = U('S'), uW = U('W');

  // native resolution (up to 2x on retina screens); lowered step by step only if the device struggles
  let scale = 1;
  function size() {
    const d = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(innerWidth * d * scale); canvas.height = Math.round(innerHeight * d * scale);
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  size(); addEventListener('resize', size);

  let z = 0, lastY = scrollY, vel = 0, mx = 0, my = 0, tmx = 0, tmy = 0, cloud = 0, warp = 0, warpTo = 0;
  addEventListener('pointermove', e => { tmx = e.clientX / innerWidth - .5; tmy = .5 - e.clientY / innerHeight; }, { passive: true });
  // the page script calls this when leaving, so the stars speed up during the page change
  window.merkornWarp = (v = 1) => { warpTo = v; };

  // cloud banks sit in the gaps between sections
  const sections = [...document.querySelectorAll('main > section')];
  let banks = [];
  const measure = () => { banks = sections.slice(1).map(s => s.offsetTop); };
  measure(); addEventListener('resize', measure); addEventListener('load', measure);

  const t0 = performance.now(); let frames = 0, tCheck = t0, travel = 0;
  function frame(now) {
    const T = (now - t0) / 1000 * (reduce ? .15 : 1);
    const y = scrollY;
    vel += ((y - lastY) - vel) * .1; lastY = y;
    z += (y / innerHeight * .9 - z) * .06;
    mx += (tmx - mx) * .04; my += (tmy - my) * .04;
    const mid = y + innerHeight * .5;
    let c = 0; banks.forEach(b => { const d = (mid - b) / (innerHeight * .32); c = Math.max(c, Math.exp(-d * d)); });
    warp += (warpTo - warp) * .08;
    cloud += (Math.max(c, warp) - cloud) * .1;
    travel += (Math.abs(vel) * .0004 + warp * .02) * (reduce ? 0 : 1);

    gl.uniform2f(uR, canvas.width, canvas.height);
    gl.uniform1f(uT, T); gl.uniform1f(uZ, z + warp * 2); gl.uniform1f(uV, travel); gl.uniform1f(uC, cloud);
    gl.uniform1f(uS, seed); gl.uniform2f(uM, mx, my);
    gl.uniform1f(uW, Math.min(1, Math.abs(vel) / 60 + warp));
    window.merkornSpeed = vel;
    gl.drawArrays(gl.TRIANGLES, 0, 3);

    frames++;
    if (now - tCheck > 2000) { const fps = frames * 1000 / (now - tCheck); if (fps < 45 && scale > .55) { scale = Math.max(.55, scale - .15); size(); } frames = 0; tCheck = now; }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

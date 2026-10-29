// Content pulled from youtube.com/@PistonOrigins. Newest first.
const EPISODES = [
  { id: "OHUYDjP9DVQ", n: 9, title: "Toyota vs FIA: The Illegal Turbo That Got Them Banned", car: "Celica GT-Four", tag: "Rally" },
  { id: "YPdVXp1ca0c", n: 8, title: "Ferrari vs Lamborghini: The Insult That Started It All", car: "Lamborghini", tag: "Rivalry" },
  { id: "u6lgliMatSk", n: 7, title: "Porsche Bought a Nissan to Prove It Cheated. It Backfired.", car: "GT-R R35", tag: "Rivalry" },
  { id: "NJSd2W415nA", n: 6, title: "Toyota Threw Away 5 Years of Work to Build This Lexus", car: "Lexus LFA", tag: "Origin" },
  { id: "LjII0wBnJHA", n: 5, title: "Why Ferrari Feared This Honda", car: "Honda NSX", tag: "Origin" },
  { id: "flQ66uxn0DM", n: 4, title: "The AE86 Wasn't Fast. So Why Is It a Legend?", car: "AE86", tag: "Legend" },
  { id: "R9jLpyg8-3A", n: 3, title: "Mazda's Rotary Engine Should Never Have Worked", car: "RX-7 & 787B", tag: "Engine" },
  { id: "_QTVeqC9ARM", n: 2, title: "Why the Skyline GT-R R34 Was Banned in America", car: "Skyline R34", tag: "Ban" },
  { id: "18hr_2O-4cg", n: 1, title: "The Toyota Supra Mk4: How Toyota Built a Legend", car: "Supra Mk4", tag: "Origin" },
];

// [id, title, views, make]
const SHORTS = [
  ["5ykQZttm47c", "Toyota's 5mm Rally Cheat Erased Its Own Evidence", "125", "Toyota"],
  ["9E6Utm3EymU", "Lamborghini Sold for $3 Million. Then $110 Million.", "292", "Lamborghini"],
  ["cRhiMRwTN5E", "A Tractor Company Built This Supercar", "1K", "Lamborghini"],
  ["WM6R9qzpf44", "Lamborghini's First Car Had No Engine", "1K", "Lamborghini"],
  ["XE_0LPD8-XI", "Enzo Ferrari Mocked a Tractor Maker. Big Mistake.", "1.2K", "Lamborghini"],
  ["pLDrefGsOtg", "Only 9 People Ever Built This Engine", "1.4K", "Lexus"],
  ["z3S1gPWU51g", "This $70K Nissan Embarrassed Porsche", "1.5K", "Nissan"],
  ["BbuAO2BmedA", "Porsche Was Scared of This $70K Nissan", "1.2K", "Nissan"],
  ["EcLN9OM8u-4", "Porsche Paid $77,000 to Expose Nissan. It Backfired", "1.2K", "Nissan"],
  ["sqj8J2LYI9o", "Nissan Told Porsche to Take Driving Lessons", "3.6K", "Nissan"],
  ["vw1Tkt2-R9I", "Why Honda Built the NSX Like an F-16 Fighter Jet", "1.2K", "Honda"],
  ["_pI1xDjmBR4", "This $60,000 Supercar Now Sells for $155,000", "700", "Honda"],
  ["PdQfFF-KN6Q", "Ayrton Senna Called Honda's Supercar \"Fragile\"", "159", "Honda"],
  ["bpgbDRwNTXg", "The Toyota Engine That Loved to Rev: the 4A-GE", "537", "Toyota"],
  ["fm3Tq5WR8fk", "The Corolla That Made the Drift King Famous", "961", "Toyota"],
  ["kn3tZTTS-gw", "Why Is the Toyota AE86 Called the \"86\"?", "152", "Toyota"],
  ["Zqdk-iFualQ", "Was the Toyota AE86 Actually Fast? Myth or Fact", "129", "Toyota"],
  ["fBe3nkaKAdA", "This Cheap Corolla Now Sells for $40,000", "1K", "Toyota"],
  ["46RwhPl4_bo", "This 1993 Toyota Engine Makes 1,000 HP", "1.1K", "Toyota"],
  ["txshOEi3vDM", "Paul Walker's R34 GT-R Sold for $1.3 Million", "1.3K", "Nissan"],
  ["iFjWHcsU8Nk", "This Mazda RX-7 Is Worth More Than It Cost New", "1.2K", "Mazda"],
  ["FGkrFcXQwSQ", "Does Every Rotary Need a Rebuild at 50,000 Miles?", "145", "Mazda"],
  ["wT5YnKhLHlE", "Mazda's Last Chance at Le Mans: The 787B Story", "1.3K", "Mazda"],
  ["J6SvnwiotMU", "This Engine Kept Destroying Itself (Devil's Nail Marks)", "265", "Mazda"],
  ["wRsPy3LiiDw", "This Engine Has No Pistons (How a Rotary Works)", "220", "Mazda"],
  ["_5NUpGSIjRY", "USA Banned This Nissan Skyline R34 for 25 Years", "40", "Nissan"],
  ["Ie3tcGUmurM", "This Nissan Had a Display Screen in 1999", "42", "Nissan"],
  ["jVt6k6vA_Vw", "Godzilla Was Named by Australians?", "56", "Nissan"],
  ["LjrRBnlZC2g", "Nissan Lied About the R34's Horsepower? (The 276 HP Secret)", "96", "Nissan"],
  ["QoNAWytQrgw", "What Does \"Supra\" Actually Mean?", "27", "Toyota"],
  ["XsglmM71UAA", "Why a Mk4 Toyota Supra Sold for $550,000", "681", "Toyota"],
  ["zhTAJGiXwFQ", "Toyota Used Hollow Carpet to Make the Mk4 Supra Lighter?", "824", "Toyota"],
  ["O35wjZkQRkY", "2JZ-GTE Explained: The Engine That Made the Supra a Legend", "65", "Toyota"],
];

const GARAGE = [
  { name: "Supra Mk4", code: "JZA80", engine: "2JZ-GTE · 3.0 L I6 twin-turbo", era: "1993–2002", ep: "18hr_2O-4cg" },
  { name: "Skyline GT-R", code: "BNR34", engine: "RB26DETT · 2.6 L I6 twin-turbo", era: "1999–2002", ep: "_QTVeqC9ARM" },
  { name: "RX-7", code: "FD3S", engine: "13B-REW · twin-rotor, sequential turbo", era: "1992–2002", ep: "R9jLpyg8-3A" },
  { name: "787B", code: "Le Mans 1991", engine: "R26B · four-rotor", era: "1991", ep: "R9jLpyg8-3A" },
  { name: "NSX", code: "NA1", engine: "C30A · 3.0 L V6 VTEC", era: "1990–2005", ep: "LjII0wBnJHA" },
  { name: "Corolla AE86", code: "Levin / Trueno", engine: "4A-GE · 1.6 L I4", era: "1983–1987", ep: "flQ66uxn0DM" },
  { name: "Lexus LFA", code: "LFA10", engine: "1LR-GUE · 4.8 L V10", era: "2010–2012", ep: "NJSd2W415nA" },
  { name: "GT-R", code: "R35", engine: "VR38DETT · 3.8 L V6 twin-turbo", era: "2007–", ep: "u6lgliMatSk" },
  { name: "Celica GT-Four", code: "ST205", engine: "3S-GTE · 2.0 L I4 turbo", era: "1994–1999", ep: "OHUYDjP9DVQ" },
  { name: "Lamborghini", code: "350 GTV → 350 GT", engine: "3.5 L V12", era: "1963–1966", ep: "YPdVXp1ca0c" },
];

const TICKER_1 = ["2JZ-GTE", "RB26DETT", "13B-REW", "4A-GE", "C30A", "1LR-GUE", "VR38DETT", "R26B", "3S-GTE"];
const TICKER_2 = ["Banned", "Rivalry", "Comeback", "Near-failure", "The insult", "Le Mans 1991", "Godzilla", "Hachi-Roku"];

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const thumb = (id, q = "hqdefault") => `https://i.ytimg.com/vi/${id}/${q}.jpg`;
const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const pad = n => String(n).padStart(2, "0");
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
const hasGsap = typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined" && !calm;

/* ---------- Render ---------- */

const wallIds = [...EPISODES.map(e => e.id), ...SHORTS.slice(0, 6).map(s => s[0])];
$("#wall").innerHTML = [...wallIds, ...wallIds, ...wallIds]
  .map(id => `<img src="${thumb(id, "mqdefault")}" alt="">`).join("");

const tickerHTML = words => Array(4).fill(words).flat().map(w => `<span>${w}</span>`).join("");
$("#ticker1").innerHTML = tickerHTML(TICKER_1);
$("#ticker2").innerHTML = tickerHTML(TICKER_2);

$("#hTrack").insertAdjacentHTML("beforeend", EPISODES.map((e, i) => `
  <article class="case${i === 0 ? " latest" : ""}" data-play="${e.id}" tabindex="0">
    <div class="thumb"><img src="${thumb(e.id, "maxresdefault")}" onerror="this.onerror=null;this.src='${thumb(e.id)}'" alt="" loading="lazy"><span class="play">▶</span></div>
    <div class="c-body">
      <span class="c-num">${pad(e.n)}</span>
      <div class="meta"><b>EP ${pad(e.n)}</b><span>${e.tag}</span><span>${e.car}</span></div>
      <h3>${esc(e.title)}</h3>
    </div>
  </article>`).join(""));

// Shorts rail with make filters
const makes = ["All", ...new Set(SHORTS.map(s => s[3]))];
const filters = $("#filters");
const rail = $("#shorts");
filters.innerHTML = makes.map((m, i) => {
  const count = m === "All" ? SHORTS.length : SHORTS.filter(s => s[3] === m).length;
  return `<button role="tab" aria-selected="${i === 0}" data-make="${m}">${m} <span class="muted">${count}</span></button>`;
}).join("");

function renderShorts(make) {
  const list = make === "All" ? SHORTS : SHORTS.filter(s => s[3] === make);
  rail.innerHTML = list.map(([id, t, v]) => `
    <article class="short" data-play="${id}" data-vertical tabindex="0">
      <div class="s-img"><img src="${thumb(id, "oar2")}" onerror="this.onerror=null;this.src='${thumb(id)}'" alt="" loading="lazy" draggable="false"><span class="views">▶ ${v} views</span></div>
      <p>${esc(t)}</p>
    </article>`).join("");
  rail.scrollTo({ left: 0 });
  if (hasGsap) gsap.from(".short", { y: 60, opacity: 0, duration: .6, stagger: .035, ease: "power3.out", clearProps: "transform,opacity" });
}
filters.addEventListener("click", e => {
  const b = e.target.closest("button");
  if (!b) return;
  filters.querySelectorAll("button").forEach(x => x.setAttribute("aria-selected", x === b));
  renderShorts(b.dataset.make);
});
renderShorts("All");
$(".rail-btn.prev").onclick = () => rail.scrollBy({ left: -rail.clientWidth * .8, behavior: "smooth" });
$(".rail-btn.next").onclick = () => rail.scrollBy({ left: rail.clientWidth * .8, behavior: "smooth" });

// Drag to scroll the Shorts rail
let drag = null;
rail.addEventListener("pointerdown", e => { if (e.pointerType === "mouse") drag = { x: e.clientX, left: rail.scrollLeft, moved: false }; });
addEventListener("pointermove", e => {
  if (!drag) return;
  const dx = e.clientX - drag.x;
  if (Math.abs(dx) > 5) { drag.moved = true; rail.classList.add("dragging"); }
  rail.scrollLeft = drag.left - dx;
});
addEventListener("pointerup", () => { setTimeout(() => rail.classList.remove("dragging"), 0); drag = null; });

$("#plates").innerHTML = GARAGE.map(g => `
  <article class="plate tilt" data-play="${g.ep}" tabindex="0">
    <div class="bg"><img src="${thumb(g.ep, "mqdefault")}" alt="" loading="lazy"></div>
    <span class="code">${g.code}</span>
    <h3>${g.name}</h3>
    <dl><dt>Engine</dt><dd>${g.engine}</dd><dt>Built</dt><dd>${g.era}</dd></dl>
    <span class="watch">▶ Watch the story</span>
  </article>`).join("");

$("#igGrid").innerHTML = EPISODES.slice(0, 6)
  .map(e => `<img src="${thumb(e.id, "mqdefault")}" alt="" loading="lazy">`).join("");

// Total Shorts views, from the (rounded) counts above
const parseViews = v => v.endsWith("K") ? parseFloat(v) * 1000 : +v;
const totalK = Math.floor(SHORTS.reduce((a, s) => a + parseViews(s[2]), 0) / 1000);
$("#viewsStat").dataset.to = totalK;

// Statement: one span per word
const big = $("#bigWords");
const HOT = ["ban,", "insult,", "near-failure,", "comeback."];
big.innerHTML = big.textContent.trim().split(/\s+/)
  .map(w => `<span class="w${HOT.includes(w) ? " hot" : ""}">${w}</span>`).join(" ");

/* ---------- Player ---------- */

const dlg = $("#player");
const frame = dlg.querySelector(".frame");
let lenis = null;
function play(id, vertical) {
  dlg.classList.toggle("vertical", vertical);
  frame.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen title="Piston Origins video"></iframe>`;
  dlg.showModal();
  lenis?.stop();
}
document.addEventListener("click", e => {
  if (rail.classList.contains("dragging")) return;
  const t = e.target.closest("[data-play]");
  if (t) play(t.dataset.play, t.hasAttribute("data-vertical"));
});
document.addEventListener("keydown", e => {
  const t = e.target.closest?.("[data-play]");
  if (t && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); play(t.dataset.play, t.hasAttribute("data-vertical")); }
});
dlg.querySelector(".close").onclick = () => dlg.close();
dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
dlg.addEventListener("close", () => { frame.innerHTML = ""; lenis?.start(); });

/* ---------- Pointer effects (no GSAP needed) ---------- */

const finePointer = matchMedia("(pointer: fine)").matches;
if (finePointer && !calm) {
  $$(".tilt").forEach(el => {
    el.addEventListener("mousemove", e => {
      const r = el.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      el.style.setProperty("--mx", px * 100 + "%");
      el.style.setProperty("--my", py * 100 + "%");
      el.style.transform = `rotateX(${(.5 - py) * 8}deg) rotateY(${(px - .5) * 10}deg)`;
    });
    el.addEventListener("mouseleave", () => { el.style.transform = ""; });
  });
  $$(".magnetic").forEach(el => {
    el.addEventListener("mousemove", e => {
      const r = el.getBoundingClientRect();
      el.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .25}px, ${(e.clientY - r.top - r.height / 2) * .35}px)`;
    });
    el.addEventListener("mouseleave", () => { el.style.transform = ""; });
  });
}

/* ---------- Motion ---------- */

const loader = $("#loader");
if (!hasGsap) {
  loader.remove();
  $$("#bigWords .w").forEach(w => (w.style.opacity = 1));
  $$("[data-to]").forEach(d => (d.textContent = d.dataset.to + (d.dataset.suffix || "")));
  $("#steps").style.setProperty("--p", 1);
  $$(".steps li").forEach(li => li.classList.add("on"));
} else {
  gsap.registerPlugin(ScrollTrigger);

  if (typeof Lenis !== "undefined") {
    lenis = new Lenis({ lerp: .1 });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(a => a.addEventListener("click", e => {
      const target = a.getAttribute("href");
      if (target.length < 2 && target !== "#") return;
      e.preventDefault();
      lenis.scrollTo(target === "#top" || target === "#" ? 0 : target, { offset: -60, duration: 1.4 });
    }));
  }

  // Intro: rev to redline, then reveal the hero
  let seen = false;
  try { seen = sessionStorage.getItem("po-intro") === "1"; sessionStorage.setItem("po-intro", "1"); } catch {}
  const rpm = { v: 0 };
  const rpmEl = $("#rpm");
  const intro = gsap.timeline();
  if (!seen) {
    document.body.classList.add("loading");
    lenis?.stop();
    const needle = loader.querySelector(".needle");
    const step = (to, d, ease, at) => intro
      .to(needle, { rotation: -80 + (to / 9000) * 160, duration: d, ease, svgOrigin: "100 110" }, at)
      .to(rpm, { v: to, duration: d, ease, onUpdate: () => (rpmEl.textContent = Math.round(rpm.v / 100) * 100) }, "<");
    gsap.set(needle, { rotation: -80, svgOrigin: "100 110" });
    intro.from(".ld-name", { y: 30, opacity: 0, duration: .5 });
    step(5200, .45, "power2.in", "<");
    step(2800, .35, "power2.out", ">");
    step(8600, .55, "power3.in", ">");
    intro.to(loader, { yPercent: -100, duration: .8, ease: "expo.inOut" }, "+=.15")
      .add(() => { loader.remove(); document.body.classList.remove("loading"); lenis?.start(); });
  } else {
    loader.remove();
  }
  intro.from(".split .ln > span", { yPercent: 110, duration: 1, stagger: .1, ease: "expo.out" }, seen ? 0 : "-=.35")
    .from(".hero-fade", { y: 24, opacity: 0, duration: .8, stagger: .08, ease: "power3.out" }, "-=.6")
    .from(".wall", { opacity: 0, scale: 1.1, duration: 1.6, ease: "power2.out" }, "<-.6");

  // Hero: the wall drifts, follows the mouse, and the copy lifts away on scroll
  const wall = $("#wall");
  gsap.set(wall, { rotation: -9 });
  gsap.to(wall, { yPercent: -16, duration: 40, ease: "none", repeat: -1, yoyo: true });
  if (finePointer) {
    const wx = gsap.quickTo(wall, "x", { duration: 1.2, ease: "power3" });
    const wy = gsap.quickTo(wall, "y", { duration: 1.2, ease: "power3" });
    $(".hero").addEventListener("mousemove", e => { wx((e.clientX / innerWidth - .5) * -60); wy((e.clientY / innerHeight - .5) * -40); });
  }
  gsap.to(".hero-inner", { y: -140, opacity: 0, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });
  gsap.to(".hero-bg", { scale: 1.15, opacity: .4, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });

  // Progress bar + nav hide on scroll down
  gsap.to("#progress", { scaleX: 1, ease: "none", scrollTrigger: { start: 0, end: "max", scrub: .3 } });
  const nav = $(".nav");
  ScrollTrigger.create({ start: 200, end: "max", onUpdate: s => nav.classList.toggle("hide", s.direction === 1 && s.scroll() > 400) });

  // Tickers: constant drift, scroll speeds them up and flips direction
  const tracks = $$(".ticker-track").map((el, i) => ({ el, x: i ? -el.scrollWidth / 4 : 0, base: i ? -1 : 1 }));
  let dir = 1, boost = 1;
  gsap.ticker.add((t, dt) => {
    boost += (1 - boost) * .06;
    tracks.forEach(tr => {
      const half = tr.el.scrollWidth / 2;
      tr.x -= tr.base * dir * boost * dt * .07;
      if (tr.x <= -half) tr.x += half;
      if (tr.x > 0) tr.x -= half;
      tr.el.style.transform = `translate3d(${tr.x}px,0,0)`;
    });
  });
  ScrollTrigger.create({
    onUpdate: s => {
      const v = s.getVelocity();
      if (Math.abs(v) < 20) return;
      dir = v > 0 ? 1 : -1;
      boost = Math.max(boost, 1 + Math.min(Math.abs(v) / 250, 8));
    },
  });

  // Statement lights up word by word
  gsap.to("#bigWords .w", {
    opacity: 1, stagger: .1, ease: "none",
    scrollTrigger: { trigger: "#bigWords", start: "top 80%", end: "bottom 45%", scrub: true },
  });

  // Pillars rise in
  gsap.from(".pillar", {
    y: 100, rotationX: 25, opacity: 0, duration: 1, stagger: .12, ease: "power3.out",
    scrollTrigger: { trigger: ".pillars", start: "top 85%" },
  });

  // Section headings
  $$(".reveal-up").forEach(h => gsap.from(h, { y: 70, opacity: 0, duration: 1, ease: "expo.out", scrollTrigger: { trigger: h, start: "top 88%" } }));

  // Stories: pinned horizontal run on wide screens
  ScrollTrigger.matchMedia({
    "(min-width: 901px)": () => {
      const track = $("#hTrack");
      const dist = () => track.scrollWidth - innerWidth;
      const run = gsap.to(track, {
        x: () => -dist(), ease: "none",
        scrollTrigger: { trigger: ".hscroll", pin: true, scrub: 1, end: () => "+=" + dist(), invalidateOnRefresh: true },
      });
      $$(".case").forEach(c => {
        gsap.fromTo(c.querySelector(".thumb img"), { xPercent: -8, scale: 1.18 }, {
          xPercent: 8, ease: "none",
          scrollTrigger: { trigger: c, containerAnimation: run, start: "left right", end: "right left", scrub: true },
        });
        gsap.from(c, {
          rotate: 4, y: 80, opacity: .3, ease: "power2.out",
          scrollTrigger: { trigger: c, containerAnimation: run, start: "left 95%", end: "left 55%", scrub: true },
        });
      });
    },
  });

  // Stats count up
  $$("[data-to]").forEach(d => {
    const o = { v: 0 };
    gsap.to(o, {
      v: +d.dataset.to, duration: 1.8, ease: "power2.out",
      onUpdate: () => (d.textContent = Math.round(o.v) + (d.dataset.suffix || "")),
      scrollTrigger: { trigger: d, start: "top 85%" },
    });
  });

  // Garage plates flip up in batches
  gsap.set(".plate", { opacity: 0 });
  ScrollTrigger.batch(".plate", {
    start: "top 90%",
    onEnter: els => gsap.fromTo(els, { y: 70, rotationX: -35, opacity: 0 }, { y: 0, rotationX: 0, opacity: 1, duration: .9, stagger: .07, ease: "power3.out", overwrite: true, clearProps: "transform" }),
  });

  // Method: the road fills and each stop lights up
  gsap.to("#steps", { "--p": 1, ease: "none", scrollTrigger: { trigger: "#steps", start: "top 65%", end: "bottom 65%", scrub: true } });
  $$(".steps li").forEach(li => {
    ScrollTrigger.create({ trigger: li, start: "top 62%", end: "max", toggleClass: { targets: li, className: "on" } });
    gsap.from(li, { x: 60, opacity: 0, duration: .8, ease: "power3.out", scrollTrigger: { trigger: li, start: "top 85%" } });
  });

  // Community + outro
  gsap.from(".ask, .ig", { y: 80, opacity: 0, duration: 1, stagger: .15, ease: "power3.out", scrollTrigger: { trigger: ".community", start: "top 80%" } });
  gsap.fromTo("#outroWord", { xPercent: 25, scale: .8 }, { xPercent: -5, scale: 1, ease: "none", scrollTrigger: { trigger: ".outro", start: "top bottom", end: "bottom bottom", scrub: true } });

  addEventListener("load", () => ScrollTrigger.refresh());
}

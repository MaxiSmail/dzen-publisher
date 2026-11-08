---
name: gsap
description: >-
  Expert guidance and patterns for GreenSock Animation Platform (GSAP 3). Use when creating complex timelines, ScrollTrigger pin/scrub effects, SVG morphing, Flip animations, smooth text transitions, and high-performance React animations with useGSAP.
---

# GSAP (GreenSock Animation Platform) Engineering & Motion Skill

This skill provides production-ready recipes, architectural patterns, and performance standards for implementing GSAP 3 in modern web applications (React / Vite / Vanilla).

---

## 1. Core Principles & Architecture

- **Hardware Acceleration**: Always animate `x`, `y`, `scale`, `rotation`, and `opacity` (transforms) rather than `top`, `left`, `width`, or `height`.
- **Cleanup & Context in React**: Always use `useGSAP()` from `@gsap/react` or `gsap.context()` to safely clean up timelines and prevent duplicate ScrollTriggers on hot-reload or unmount.
- **Single Source of Truth**: Group related animations into a master `gsap.timeline()` rather than firing isolated tweens.

---

## 2. Standard Setup & Plugin Registration

```javascript
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Flip } from 'gsap/Flip'
import { TextPlugin } from 'gsap/TextPlugin'
import { useGSAP } from '@gsap/react'

// Register plugins once
gsap.registerPlugin(ScrollTrigger, Flip, TextPlugin, useGSAP)
```

---

## 3. React Integration Patterns

### A. Basic Timeline with `useGSAP`
```jsx
import React, { useRef } from 'react'
import gsap from 'gsap'
import { useGSAP } from '@gsap/react'

export default function HeroAnimated() {
  const containerRef = useRef(null)

  useGSAP(() => {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 1 } })

    tl.from('.hero-badge', { y: -20, opacity: 0, duration: 0.6 })
      .from('.hero-title span', { y: 60, opacity: 0, stagger: 0.15 }, '-=0.3')
      .from('.hero-desc', { y: 30, opacity: 0, duration: 0.8 }, '-=0.4')
      .from('.hero-cta', { scale: 0.9, opacity: 0, stagger: 0.1 }, '-=0.4')
  }, { scope: containerRef })

  return (
    <section ref={containerRef} className="hero">
      <div className="hero-badge">Industrial Tech</div>
      <h1 className="hero-title">
        <span>Engineering</span> <span>Safety</span> <span>Systems</span>
      </h1>
      <p className="hero-desc">Turnkey industrial automation and monitoring.</p>
      <div className="hero-cta">
        <button className="btn btn-primary">Get Started</button>
      </div>
    </section>
  )
}
```

### B. ScrollTrigger Scrub & Pinning
```jsx
useGSAP(() => {
  gsap.to('.track-container', {
    xPercent: -100 * (sections.length - 1),
    ease: 'none',
    scrollTrigger: {
      trigger: '.horizontal-section',
      pin: true,
      scrub: 1,
      snap: 1 / (sections.length - 1),
      end: () => '+=' + document.querySelector('.track-container').offsetWidth
    }
  })
}, { scope: containerRef })
```

---

## 4. High-Performance Best Practices

1. **`will-change` vs `force3D`**: GSAP enables 3D transforms by default (`force3D: "auto"`). Avoid manually spamming CSS `will-change: transform` on dozens of elements.
2. **ScrollTrigger Refresh**: When dynamic content loads (e.g. async images or API data), call `ScrollTrigger.refresh()`.
3. **Responsive Breakpoints**: Use `ScrollTrigger.matchMedia()` for device-specific animations.

```javascript
ScrollTrigger.matchMedia({
  // Desktop
  "(min-width: 800px)": function() {
    gsap.to(".sidebar", { scrollTrigger: { trigger: ".content", pin: ".sidebar" } })
  },
  // Mobile
  "(max-width: 799px)": function() {
    gsap.set(".sidebar", { clearProps: "all" })
  }
})
```

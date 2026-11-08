---
name: parallax-landings
description: >-
  Architecture, design tokens, and implementation guidelines for high-impact Parallax Landing pages. Use when building multi-layer depth scroll experiences, mouse-tracking 2.5D card tilts, speed-differentiated background/foreground layers, floating badge dynamics, and cinematic parallax storytelling.
---

# Parallax Landings (Depth & Motion Choreography) Skill

This skill outlines production patterns for building high-conversion, modern **Parallax Landing Pages** using multi-layer depth, velocity-responsive scrolling, and interactive cursor tilt effects.

---

## 1. Core Parallax Dimensions

A high-tier parallax landing operates across three coordinate dimensions:

1. **Scroll-Driven Z/Y Depth (Vertical Parallax)**:
   - Background layers move slowest (`speed: 0.2` – `0.5`).
   - Content / text layer moves at standard speed (`speed: 1.0`).
   - Floating badges, accents, and foreground particles move faster (`speed: 1.3` – `1.8`), creating an authentic 3D sense of depth.

2. **Pointer / Cursor Reaction (2.5D Mouse Parallax)**:
   - Subtle `perspective(1000px) rotateX(...) rotateY(...)` on hero containers and floating technical badges based on normalized cursor position `(x - center) / width`.

3. **Scale & Blur Morphing on Scroll**:
   - Background grid scales up slightly (`scale: 1.0 -> 1.15`) while blurring out as the user enters detailed content sections.

---

## 2. High-Performance GSAP ScrollTrigger Parallax

```javascript
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export function initLayerParallax() {
  // Select all elements with data-parallax-speed attribute
  const parallaxLayers = document.querySelectorAll('[data-parallax-speed]')

  parallaxLayers.forEach((layer) => {
    const speed = parseFloat(layer.getAttribute('data-parallax-speed')) || 0.5
    const movement = -(speed * 100)

    gsap.to(layer, {
      y: movement,
      ease: 'none',
      scrollTrigger: {
        trigger: layer.closest('section') || layer,
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1.2
      }
    })
  })
}
```

---

## 3. 2.5D Mouse Interactive Card Tilt (React Hook)

```jsx
import React, { useRef } from 'react'

export function useParallaxTilt(intensity = 15) {
  const cardRef = useRef(null)

  const handleMouseMove = (e) => {
    const card = cardRef.current
    if (!card) return

    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left - rect.width / 2
    const y = e.clientY - rect.top - rect.height / 2

    const rotateX = -(y / (rect.height / 2)) * intensity
    const rotateY = (x / (rect.width / 2)) * intensity

    card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`
    card.style.transition = 'transform 0.1s ease-out'
  }

  const handleMouseLeave = () => {
    const card = cardRef.current
    if (!card) return
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
    card.style.transition = 'transform 0.5s ease-out'
  }

  return { cardRef, handleMouseMove, handleMouseLeave }
}
```

---

## 4. Multi-Layer Parallax Hero Component Recipe

```jsx
import React, { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { useParallaxTilt } from './useParallaxTilt'

gsap.registerPlugin(ScrollTrigger)

export default function ParallaxHero() {
  const heroRef = useRef(null)
  const { cardRef, handleMouseMove, handleMouseLeave } = useParallaxTilt(10)

  useEffect(() => {
    const ctx = gsap.context(() => {
      // 1. Background Grid Parallax (slow)
      gsap.to('.parallax-bg', {
        yPercent: 30,
        ease: 'none',
        scrollTrigger: { trigger: heroRef.current, start: 'top top', end: 'bottom top', scrub: true }
      })

      // 2. Blueprint 3D Graphic (medium)
      gsap.to('.parallax-graphic', {
        yPercent: -20,
        scale: 1.08,
        ease: 'none',
        scrollTrigger: { trigger: heroRef.current, start: 'top top', end: 'bottom top', scrub: 1 }
      })

      // 3. Floating Indicator Badges (fast)
      gsap.to('.parallax-badge-fast', {
        yPercent: -50,
        rotation: 6,
        ease: 'none',
        scrollTrigger: { trigger: heroRef.current, start: 'top top', end: 'bottom top', scrub: 1.5 }
      })
    }, heroRef)

    return () => ctx.revert()
  }, [])

  return (
    <section ref={heroRef} className="parallax-hero-section">
      <div className="parallax-bg bg-grid" data-parallax-speed="0.3" />

      <div className="container hero-layout">
        <div className="hero-text-layer">
          <h1 className="hero-title">High-Precision Industrial Engineering</h1>
          <p className="hero-desc">Autonomous safety and turnkey infrastructure systems.</p>
        </div>

        <div 
          ref={cardRef} 
          onMouseMove={handleMouseMove} 
          onMouseLeave={handleMouseLeave} 
          className="parallax-graphic visual-card glass"
        >
          <div className="blueprint-visual" />
          <div className="parallax-badge-fast floating-badge">
            <span>🛡️ SRO & MCHS Certified</span>
          </div>
        </div>
      </div>
    </section>
  )
}
```

---

## 5. Mobile & Performance Safeguards

1. **Disable on Touch Devices**: On touch screens (`@media (hover: none)`), disable continuous mousemove calculations and rely solely on smooth vertical scrub.
2. **GPU Layers**: Apply `transform: translate3d(0, 0, 0)` or `backface-visibility: hidden` to avoid repainting entire DOM trees on scroll.
3. **Respect Reduced Motion**:
```css
@media (prefers-reduced-motion: reduce) {
  .parallax-bg, .parallax-graphic, [data-parallax-speed] {
    transform: none !important;
    transition: none !important;
  }
}
```

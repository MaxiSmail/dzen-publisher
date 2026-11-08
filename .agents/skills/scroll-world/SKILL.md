---
name: scroll-world
description: >-
  Architectural patterns and implementation guidelines for 3D Scroll World experiences. Use when integrating Smooth Scroll (Lenis), GSAP ScrollTrigger, and Three.js / WebGL to create scroll-driven camera paths, pinned 3D narrative checkpoints, interactive spatial storytelling, and synced 3D/DOM layers.
---

# Scroll World (3D Scroll & Spatial Storytelling) Skill

This skill defines the industry standard for creating **Scroll Worlds** — interactive web experiences where user scrolling orchestrates smooth camera movements, spatial 3D transitions, and coordinated DOM content overlays.

---

## 1. The 3-Layer Scroll World Architecture

A world-class Scroll World combines three synchronized layers:

```
┌───────────────────────────────────────────────────────────┐
│ 1. Smooth Scroll Layer (Lenis / RAF)                      │
│    Provides momentum, normalized delta, and lerped scroll │
├───────────────────────────────────────────────────────────┤
│ 2. GSAP ScrollTrigger Choreography                        │
│    Binds scroll progress (0.0 -> 1.0) to camera / meshes  │
├───────────────────────────────────────────────────────────┤
│ 3. Three.js / WebGL Spatial World                         │
│    Renders 3D models, shaders, particle clouds, lighting  │
└───────────────────────────────────────────────────────────┘
```

---

## 2. Lenis + GSAP ScrollTrigger Synchronization

To prevent frame jitter and desynchronization between HTML elements and the 3D WebGL Canvas:

```javascript
import Lenis from 'lenis'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

// 1. Initialize Lenis
export function setupSmoothScrollWorld() {
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true
  })

  // 2. Synchronize Lenis with ScrollTrigger
  lenis.on('scroll', ScrollTrigger.update)

  // 3. Connect to GSAP ticker
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000)
  })

  gsap.ticker.lagSmoothing(0)

  return lenis
}
```

---

## 3. Scroll-Driven 3D Camera Choreography Pattern

Binding 3D Camera position, rotation, and target along a multi-section narrative:

```jsx
import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

export default function ScrollWorldHero() {
  const canvasRef = useRef(null)
  const containerRef = useRef(null)

  useEffect(() => {
    // Three.js Scene Setup
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100)
    camera.position.set(0, 2, 8)

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      alpha: true,
      antialias: true
    })
    renderer.setSize(window.innerWidth, window.innerHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

    // 3D Object / World Center
    const targetObj = { x: 0, y: 0, z: 0 }
    
    // GSAP ScrollTrigger Timeline
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1.5,
        pin: '.canvas-pin-wrapper'
      }
    })

    // Section 1 -> Section 2: Fly-in & Rotate
    tl.to(camera.position, { x: 3, y: 4, z: 5, ease: 'power2.inOut' }, 0)
      .to(targetObj, { x: 1, y: 0, z: 0, ease: 'power2.inOut' }, 0)
    
    // Section 2 -> Section 3: Deep Dive into Model
    tl.to(camera.position, { x: -2, y: 1, z: 2, ease: 'power2.inOut' }, 1)
      .to(targetObj, { x: 0, y: 0.5, z: 0, ease: 'power2.inOut' }, 1)

    // Render loop with lookAt tracking
    let frameId
    const render = () => {
      camera.lookAt(targetObj.x, targetObj.y, targetObj.z)
      renderer.render(scene, camera)
      frameId = requestAnimationFrame(render)
    }
    render()

    return () => {
      cancelAnimationFrame(frameId)
      ScrollTrigger.getAll().forEach(t => t.kill())
      renderer.dispose()
    }
  }, [])

  return (
    <div ref={containerRef} className="scroll-world-container">
      <div className="canvas-pin-wrapper">
        <canvas ref={canvasRef} className="webgl-canvas" />
      </div>

      <section className="world-section step-1">
        <h2>01. Intelligent Engineering</h2>
      </section>

      <section className="world-section step-2">
        <h2>02. Security & Control Infrastructure</h2>
      </section>

      <section className="world-section step-3">
        <h2>03. Automated Manufacturing Networks</h2>
      </section>
    </div>
  )
}
```

---

## 4. Key Rules for Scroll Worlds

1. **Scrub Easing**: Use `scrub: 1` to `scrub: 2` for a fluid, physical feeling rather than instant snap-to-scroll.
2. **Fixed Pinning**: Pin the canvas container (`position: fixed` or `ScrollTrigger.pin`) while the narrative HTML cards scroll naturally over/beside the 3D scene.
3. **Graceful Degradation**: On low-end mobile devices or reduced motion preferences (`prefers-reduced-motion: reduce`), gracefully disable heavy post-processing and freeze complex camera sweeps.

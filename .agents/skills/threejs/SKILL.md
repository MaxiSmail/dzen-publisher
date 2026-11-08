---
name: threejs
description: >-
  Expert patterns and architectural guidelines for Three.js, React Three Fiber (R3F), and Drei. Use when building WebGL 3D scenes, particle systems, interactive 3D blueprints, custom shaders, GLTF/GLB asset loading, post-processing, and 3D UI canvases.
---

# Three.js & WebGL 3D Engineering Skill

Comprehensive guide and patterns for crafting high-performance, immersive 3D scenes using Vanilla Three.js and React Three Fiber (R3F) + Drei.

---

## 1. Core Architecture (Vanilla Three.js in React)

```jsx
import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function ThreeBlueprintScene() {
  const mountRef = useRef(null)

  useEffect(() => {
    const currentMount = mountRef.current
    if (!currentMount) return

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(
      60,
      currentMount.clientWidth / currentMount.clientHeight,
      0.1,
      1000
    )
    camera.position.set(0, 0, 5)

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(currentMount.clientWidth, currentMount.clientHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    currentMount.appendChild(renderer.domElement)

    // 2. Geometry & Material (e.g. Glowing Tech Grid / Particle Sphere)
    const geometry = new THREE.IcosahedronGeometry(2, 2)
    const material = new THREE.MeshStandardMaterial({
      color: 0x00f2fe,
      wireframe: true,
      emissive: 0x0066ff,
      emissiveIntensity: 0.4
    })
    const mesh = new THREE.Mesh(geometry, material)
    scene.add(mesh)

    // 3. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8)
    scene.add(ambientLight)

    const pointLight = new THREE.PointLight(0x00f2fe, 2, 50)
    pointLight.position.set(5, 5, 5)
    scene.add(pointLight)

    // 4. Animation Loop
    let animationFrameId
    const clock = new THREE.Clock()

    const animate = () => {
      const elapsedTime = clock.getElapsedTime()
      mesh.rotation.x = elapsedTime * 0.2
      mesh.rotation.y = elapsedTime * 0.3
      renderer.render(scene, camera)
      animationFrameId = requestAnimationFrame(animate)
    }
    animate()

    // 5. Resize Handler
    const handleResize = () => {
      if (!currentMount) return
      camera.aspect = currentMount.clientWidth / currentMount.clientHeight
      camera.updateProjectionMatrix()
      renderer.setSize(currentMount.clientWidth, currentMount.clientHeight)
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    }
    window.addEventListener('resize', handleResize)

    // 6. Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      cancelAnimationFrame(animationFrameId)
      if (currentMount && renderer.domElement) {
        currentMount.removeChild(renderer.domElement)
      }
      geometry.dispose()
      material.dispose()
      renderer.dispose()
    }
  }, [])

  return <div ref={mountRef} style={{ width: '100%', height: '100%' }} />
}
```

---

## 2. Performance & Memory Management Standards

1. **Geometry & Material Disposal**: Always dispose of geometries, materials, and textures on unmount to prevent WebGL memory leaks.
2. **Device Pixel Ratio**: Cap `setPixelRatio` at `Math.min(window.devicePixelRatio, 2)`. Unlimited DPR on Retina/4K screens causes severe GPU lag.
3. **InstancedMesh**: When rendering hundreds or thousands of repetitive objects (e.g. data points, building modules, industrial nodes), use `THREE.InstancedMesh` instead of creating multiple individual meshes.
4. **Draw Calls & Alpha**: Avoid stacking overlapping transparent full-screen planes (overdraw kills mobile framerates).

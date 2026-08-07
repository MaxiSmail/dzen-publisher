import React, { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Services from './components/Services'
import Calculator from './components/Calculator'
import About from './components/About'
import Clients from './components/Clients'
import Licenses from './components/Licenses'
import Contacts from './components/Contacts'
import Footer from './components/Footer'
import Modal from './components/Modal'
import ManagementDashboard from './components/ManagementDashboard'

export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isDashOpen, setIsDashOpen] = useState(false)

  const handleOpenModal = () => {
    setIsModalOpen(true)
    document.body.style.overflow = 'hidden'
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    document.body.style.overflow = 'auto'
  }

  const handleOpenDash = () => {
    setIsDashOpen(true)
    document.body.style.overflow = 'hidden'
  }

  const handleCloseDash = () => {
    setIsDashOpen(false)
    document.body.style.overflow = 'auto'
  }

  // Scroll-reveal observer: activates .reveal and .reveal-scale on scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
          }
        })
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    )

    const targets = document.querySelectorAll('.reveal, .reveal-scale')
    targets.forEach((el) => observer.observe(el))

    return () => {
      targets.forEach((el) => observer.unobserve(el))
    }
  }, [])

  return (
    <div className="app-wrapper">
      <Navbar onContactClick={handleOpenModal} onManagementClick={handleOpenDash} />
      <main>
        <Hero onContactClick={handleOpenModal} onManagementClick={handleOpenDash} />
        <Services />
        <Calculator onOrderClick={handleOpenModal} />
        <About />
        <Clients />
        <Licenses />
        <Contacts />
      </main>
      <Footer />
      
      {/* Modals */}
      <Modal isOpen={isModalOpen} onClose={handleCloseModal} />
      <ManagementDashboard isOpen={isDashOpen} onClose={handleCloseDash} />
      
      <style>{`
        .app-wrapper {
          position: relative;
          width: 100%;
          min-height: 100vh;
          overflow-x: hidden;
          background-color: var(--bg-main, #0b1120);
        }
      `}</style>
    </div>
  )
}

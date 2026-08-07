import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Phone, Menu, X, Activity, Calculator } from 'lucide-react'

export default function Navbar({ onContactClick, onManagementClick }) {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true)
      } else {
        setScrolled(false)
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navLinks = [
    { name: 'Услуги', href: '#services' },
    { name: 'Калькулятор', href: '#calculator' },
    { name: 'О компании', href: '#about' },
    { name: 'Лицензии', href: '#licenses' },
    { name: 'Клиенты', href: '#clients' },
    { name: 'Контакты', href: '#contacts' }
  ]

  return (
    <>
      <motion.nav 
        className={`navbar ${scrolled ? 'navbar-scrolled' : ''}`}
        initial={{ y: -60, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="container nav-container">
          <a href="#" className="nav-logo">
            <img src="https://bmk-company.ru/files/110/logo0.svg" alt="БМК" className="logo-img" />
            <div className="logo-text">
              <span className="logo-title">БМК</span>
              <span className="logo-sub">Строительно-монтажная компания</span>
            </div>
          </a>

          <div className="nav-menu">
            {navLinks.map((link) => (
              <a key={link.name} href={link.href} className="nav-item">
                {link.name}
              </a>
            ))}
          </div>

          <div className="nav-actions">
            <button 
              className="btn btn-management"
              onClick={onManagementClick}
              title="Панель мониторинга объектов"
            >
              <Activity size={16} className="pulse-icon" />
              <span>БМК Управление</span>
            </button>

            <a href="tel:+79803239999" className="nav-phone">
              <Phone size={18} className="phone-icon" />
              <span>8 (980) 323-99-99</span>
            </a>

            <button className="btn btn-primary nav-btn" onClick={onContactClick}>
              Заказать услугу
            </button>

            <button className="mobile-toggle" onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </motion.nav>

      {/* Mobile Drawer with Framer Motion */}
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            className="mobile-drawer drawer-open"
            initial={{ opacity: 0, x: '100%' }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          >
            <div className="drawer-content">
              <div className="drawer-links">
                {navLinks.map((link) => (
                  <a
                    key={link.name}
                    href={link.href}
                    className="drawer-item"
                    onClick={() => setIsOpen(false)}
                  >
                    {link.name}
                  </a>
                ))}
              </div>
              <div className="drawer-footer">
                <button
                  className="btn btn-management w-full mb-3"
                  onClick={() => {
                    setIsOpen(false)
                    onManagementClick()
                  }}
                >
                  <Activity size={18} /> БМК Управление
                </button>

                <a href="tel:+79803239999" className="drawer-phone mb-3">
                  <Phone size={20} />
                  <span>8 (980) 323-99-99</span>
                </a>

                <button
                  className="btn btn-primary w-full"
                  onClick={() => {
                    setIsOpen(false)
                    onContactClick()
                  }}
                >
                  Заказать услугу
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .navbar {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          padding: 20px 0;
          transition: all 0.3s ease;
          background: transparent;
        }
        .navbar-scrolled {
          padding: 12px 0;
          background: rgba(10, 15, 30, 0.85);
          backdrop-filter: blur(12px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }
        .nav-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .nav-logo {
          display: flex;
          align-items: center;
          gap: 12px;
          text-decoration: none;
        }
        .logo-img {
          height: 36px;
          width: auto;
        }
        .logo-text {
          display: flex;
          flex-direction: column;
        }
        .logo-title {
          font-size: 1.3rem;
          font-weight: 800;
          letter-spacing: 1px;
          color: #fff;
        }
        .logo-sub {
          font-size: 0.68rem;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .nav-menu {
          display: flex;
          align-items: center;
          gap: 24px;
        }
        .nav-item {
          color: #cbd5e1;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 500;
          transition: color 0.2s;
        }
        .nav-item:hover {
          color: #00f2fe;
        }
        .nav-actions {
          display: flex;
          align-items: center;
          gap: 16px;
        }
        .btn-management {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 16px;
          border-radius: 10px;
          background: rgba(0, 242, 254, 0.1);
          border: 1px solid rgba(0, 242, 254, 0.3);
          color: #00f2fe;
          font-size: 0.85rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .btn-management:hover {
          background: rgba(0, 242, 254, 0.2);
          box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }
        .pulse-icon {
          animation: pulse 2s infinite;
        }
        @keyframes pulse {
          0% { opacity: 0.6; transform: scale(0.95); }
          50% { opacity: 1; transform: scale(1.1); }
          100% { opacity: 0.6; transform: scale(0.95); }
        }
        .nav-phone {
          display: flex;
          align-items: center;
          gap: 8px;
          color: #fff;
          text-decoration: none;
          font-weight: 600;
          font-size: 0.9rem;
        }
        .phone-icon {
          color: #00f2fe;
        }
        .mobile-toggle {
          display: none;
          background: none;
          border: none;
          color: #fff;
          cursor: pointer;
        }
        .mobile-drawer {
          position: fixed;
          inset: 0;
          z-index: 999;
          background: rgba(10, 15, 30, 0.98);
          padding: 80px 24px 30px;
        }
        .drawer-content {
          height: 100%;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        .drawer-links {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .drawer-item {
          font-size: 1.2rem;
          color: #f1f5f9;
          text-decoration: none;
          font-weight: 600;
        }
        .drawer-phone {
          display: flex;
          align-items: center;
          gap: 10px;
          color: #00f2fe;
          text-decoration: none;
          font-size: 1.1rem;
          font-weight: 700;
        }
        .mb-3 { margin-bottom: 12px; }
        @media (max-width: 992px) {
          .nav-menu, .nav-phone, .btn-management {
            display: none;
          }
          .mobile-toggle {
            display: block;
          }
        }
      `}</style>
    </>
  )
}

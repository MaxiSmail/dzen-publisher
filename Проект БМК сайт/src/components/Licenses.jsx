import React, { useState } from 'react'
import { siteData } from '../data/siteData'
import { ZoomIn, X, ChevronLeft, ChevronRight } from 'lucide-react'

export default function Licenses() {
  const [lightboxIndex, setLightboxIndex] = useState(null)

  const handleOpenLightbox = (index) => {
    setLightboxIndex(index)
    document.body.style.overflow = 'hidden'
  }

  const handleCloseLightbox = () => {
    setLightboxIndex(null)
    document.body.style.overflow = 'auto'
  }

  const handlePrev = (e) => {
    e.stopPropagation()
    setLightboxIndex((prev) => (prev - 1 + siteData.licenses.length) % siteData.licenses.length)
  }

  const handleNext = (e) => {
    e.stopPropagation()
    setLightboxIndex((prev) => (prev + 1) % siteData.licenses.length)
  }

  return (
    <section id="licenses" className="licenses-section">
      <div className="bg-grid"></div>
      
      <div className="container">
        <h2 className="section-title">
          <span className="gradient-text">Лицензии и сертификаты</span>
        </h2>
        <p className="section-subtitle">
          ООО «БМК» является членом СРО в области проектирования и строительства, а также обладает государственной лицензией МЧС.
        </p>

        <div className="licenses-grid">
          {siteData.licenses.map((license, idx) => (
            <div 
              key={idx} 
              className="license-card glass"
              onClick={() => handleOpenLightbox(idx)}
            >
              <div className="license-img-wrapper">
                <img src={license.img} alt={license.title} className="license-img" />
                <div className="license-hover-overlay">
                  <ZoomIn size={32} className="zoom-icon" />
                  <span>Увеличить</span>
                </div>
              </div>
              <div className="license-info">
                <h4 className="license-card-title">{license.title}</h4>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lightbox Modal */}
      {lightboxIndex !== null && (
        <div className="lightbox-overlay" onClick={handleCloseLightbox}>
          <button className="lightbox-close" onClick={handleCloseLightbox}>
            <X size={24} />
          </button>
          
          <button className="lightbox-nav-btn prev-btn" onClick={handlePrev}>
            <ChevronLeft size={36} />
          </button>
          
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <img 
              src={siteData.licenses[lightboxIndex].img} 
              alt={siteData.licenses[lightboxIndex].title} 
              className="lightbox-image" 
            />
            <div className="lightbox-caption">
              {siteData.licenses[lightboxIndex].title}
            </div>
          </div>
          
          <button className="lightbox-nav-btn next-btn" onClick={handleNext}>
            <ChevronRight size={36} />
          </button>
        </div>
      )}

      <style>{`
        .licenses-section {
          background-color: var(--bg-main);
          position: relative;
          border-bottom: 1px solid var(--border-color);
        }

        .licenses-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
          gap: 1.25rem;
        }

        .license-card {
          cursor: pointer;
          overflow: hidden;
          display: flex;
          flex-direction: column;
          border-radius: var(--radius-md);
        }

        .license-img-wrapper {
          position: relative;
          width: 100%;
          aspect-ratio: 0.72;
          background: rgba(255, 255, 255, 0.02);
          overflow: hidden;
          border-bottom: 1px solid var(--border-color);
        }

        .license-img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          object-position: top;
          transition: transform var(--transition-normal);
        }

        .license-hover-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(10, 13, 22, 0.85);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 0.8rem;
          opacity: 0;
          transition: all var(--transition-fast);
          backdrop-filter: blur(4px);
        }

        .license-card:hover .license-hover-overlay {
          opacity: 1;
        }

        .license-card:hover .license-img {
          transform: scale(1.03);
        }

        .zoom-icon {
          color: var(--accent);
          transform: scale(0.8);
          transition: transform var(--transition-fast);
        }

        .license-card:hover .zoom-icon {
          transform: scale(1);
        }

        .license-info {
          padding: 0.75rem 1rem;
          text-align: center;
        }

        .license-card-title {
          font-size: 0.9rem;
          font-weight: 600;
          color: var(--text-main);
          line-height: 1.4;
        }

        /* Lightbox styling */
        .lightbox-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(4, 6, 12, 0.95);
          backdrop-filter: blur(8px);
          z-index: 1100;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 2rem;
          animation: fade-in 0.3s forwards;
        }

        .lightbox-close {
          position: absolute;
          top: 1.5rem;
          right: 1.5rem;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--border-color);
          color: var(--text-main);
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all var(--transition-fast);
          z-index: 12;
        }

        .lightbox-close:hover {
          background: rgba(255, 255, 255, 0.1);
          border-color: var(--accent);
          transform: rotate(90deg);
        }

        .lightbox-nav-btn {
          background: none;
          border: none;
          color: var(--text-muted);
          cursor: pointer;
          transition: color var(--transition-fast);
          padding: 1rem;
          z-index: 10;
        }

        .lightbox-nav-btn:hover {
          color: var(--accent);
        }

        .lightbox-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          max-width: 80%;
          max-height: 85vh;
          position: relative;
        }

        .lightbox-image {
          max-width: 100%;
          max-height: 75vh;
          object-fit: contain;
          border: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
        }

        .lightbox-caption {
          margin-top: 1.5rem;
          font-family: var(--font-family-title);
          font-weight: 700;
          font-size: 1.1rem;
          color: var(--text-main);
          text-align: center;
        }

        @media (max-width: 768px) {
          .lightbox-overlay {
            padding: 1rem;
          }
          .lightbox-content {
            max-width: 100%;
          }
          .lightbox-nav-btn {
            display: none;
          }
        }
      `}</style>
    </section>
  )
}

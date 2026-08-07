import React, { useState } from 'react'
import { siteData } from '../data/siteData'
import { 
  Briefcase, FileText, Cpu, Zap, Bell, Flame, 
  Network, Lock, Eye, ShieldAlert, Wind, Droplet, Fan, X, Info 
} from 'lucide-react'

// Icon mapping dictionary
const iconMap = {
  Briefcase: Briefcase,
  FileText: FileText,
  Cpu: Cpu,
  Zap: Zap,
  Bell: Bell,
  Flame: Flame,
  Network: Network,
  Lock: Lock,
  Eye: Eye,
  ShieldAlert: ShieldAlert,
  Wind: Wind,
  Droplet: Droplet,
  Fan: Fan
}

export default function Services() {
  const [activeService, setActiveService] = useState(null)

  const handleOpenDetail = (key) => {
    setActiveService({
      key,
      ...siteData.services[key]
    })
    document.body.style.overflow = 'hidden' // Lock background scroll
  }

  const handleCloseDetail = () => {
    setActiveService(null)
    document.body.style.overflow = 'auto' // Restore scroll
  }

  return (
    <section id="services" className="services-section">
      <div className="bg-grid"></div>
      
      <div className="container">
        <h2 className="section-title reveal">
          <span className="gradient-text">Направления деятельности</span>
        </h2>
        <p className="section-subtitle reveal reveal-delay-1">
          Мы осуществляем полный спектр проектных, строительно-монтажных и пусконаладочных работ для инженерных сетей и систем безопасности.
        </p>

        <div className="services-grid">
          {Object.entries(siteData.services).map(([key, service]) => {
            const IconComponent = iconMap[service.icon] || Info
            return (
              <div 
                key={key} 
                className="service-card glass reveal"
                onClick={() => handleOpenDetail(key)}
              >
                <div className="service-icon-wrapper">
                  <IconComponent size={28} className="service-icon" />
                </div>
                <h3 className="service-title">{service.title}</h3>
                <p className="service-preview">
                  {service.paragraphs[0] ? service.paragraphs[0].slice(0, 110) + '...' : ''}
                </p>
                <span className="service-more-btn">
                  Подробнее <span>&rarr;</span>
                </span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Modern Slide-over Modal for service details */}
      {activeService && (
        <div className="service-modal-overlay" onClick={handleCloseDetail}>
          <div className="service-modal-content glass" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={handleCloseDetail}>
              <X size={24} />
            </button>
            
            <div className="modal-header-section">
              <div className="modal-icon-wrapper">
                {React.createElement(iconMap[activeService.icon] || Info, { size: 36, className: "modal-icon" })}
              </div>
              <h2 className="modal-title">{activeService.title}</h2>
            </div>
            
            <div className="modal-body-section">
              <div className="modal-text-content">
                {activeService.paragraphs.map((p, idx) => (
                  <p key={idx} className="modal-paragraph">
                    {p.startsWith('-') || p.startsWith('•') ? (
                      <span className="bullet-point">{p}</span>
                    ) : (
                      p
                    )}
                  </p>
                ))}
              </div>

              {activeService.images && activeService.images.length > 1 && (
                <div className="modal-images-grid">
                  <h4 className="images-title">Галерея направления</h4>
                  <div className="images-layout">
                    {activeService.images.filter(img => !img.src.includes('logo0.svg')).map((img, idx) => (
                      <div key={idx} className="modal-img-container">
                        <img src={img.src} alt={img.alt || activeService.title} className="modal-img" />
                        {img.alt && <span className="img-caption">{img.alt}</span>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <style>{`
        .services-section {
          background-color: #0b0f19;
          position: relative;
        }

        .services-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 2rem;
        }

        .service-card {
          padding: 2.5rem 2rem;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          height: 100%;
          border-radius: var(--radius-md);
        }

        .service-icon-wrapper {
          padding: 0.8rem;
          background: rgba(0, 102, 255, 0.1);
          border: 1px solid rgba(0, 102, 255, 0.2);
          border-radius: var(--radius-sm);
          margin-bottom: 1.5rem;
          color: var(--accent);
          transition: all var(--transition-fast);
        }

        .service-card:hover .service-icon-wrapper {
          background: var(--primary);
          color: #fff;
          box-shadow: 0 0 15px var(--primary-glow);
        }

        .service-title {
          font-size: 1.15rem;
          font-weight: 700;
          margin-bottom: 1rem;
          line-height: 1.4;
          min-height: 2.8rem;
        }

        .service-preview {
          color: var(--text-muted);
          font-size: 0.88rem;
          line-height: 1.6;
          margin-bottom: 1.5rem;
          flex-grow: 1;
        }

        .service-more-btn {
          font-family: var(--font-family-title);
          font-size: 0.85rem;
          font-weight: 700;
          color: var(--accent);
          display: flex;
          align-items: center;
          gap: 0.4rem;
        }

        .service-card:hover .service-more-btn span {
          transform: translateX(5px);
          transition: transform var(--transition-fast);
        }

        /* Modal Overlay & Card Styling */
        .service-modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(4, 6, 12, 0.85);
          backdrop-filter: blur(8px);
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          animation: fade-in 0.3s forwards;
        }

        .service-modal-content {
          width: 100%;
          max-width: 900px;
          max-height: 85vh;
          overflow-y: auto;
          background: rgba(15, 23, 42, 0.95);
          border: 1px solid rgba(255, 255, 255, 0.1);
          padding: 4rem;
          position: relative;
          box-shadow: 0 50px 100px rgba(0, 0, 0, 0.8);
          animation: slide-up 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        .modal-close-btn {
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
        }

        .modal-close-btn:hover {
          background: rgba(255, 255, 255, 0.1);
          border-color: var(--accent);
          transform: rotate(90deg);
        }

        .modal-header-section {
          display: flex;
          align-items: center;
          gap: 1.5rem;
          margin-bottom: 2.5rem;
          border-bottom: 1px solid var(--border-color);
          padding-bottom: 1.5rem;
        }

        .modal-icon-wrapper {
          padding: 1rem;
          background: rgba(0, 242, 254, 0.1);
          border: 1px solid rgba(0, 242, 254, 0.3);
          border-radius: var(--radius-sm);
          color: var(--accent);
        }

        .modal-title {
          font-size: 1.8rem;
          line-height: 1.3;
        }

        .modal-body-section {
          display: grid;
          grid-template-columns: 1.2fr 0.8fr;
          gap: 3rem;
        }

        .modal-text-content {
          display: flex;
          flex-direction: column;
          gap: 1.2rem;
        }

        .modal-paragraph {
          font-size: 0.95rem;
          color: #d1d5db;
          line-height: 1.7;
        }

        .bullet-point {
          display: block;
          padding-left: 1rem;
          border-left: 2px solid var(--accent);
          color: var(--text-main);
        }

        .modal-images-grid {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .images-title {
          font-size: 1.1rem;
          color: var(--text-main);
        }

        .images-layout {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .modal-img-container {
          position: relative;
          border-radius: var(--radius-sm);
          overflow: hidden;
          border: 1px solid var(--border-color);
        }

        .modal-img {
          width: 100%;
          height: auto;
          display: block;
          transition: transform var(--transition-normal);
        }

        .modal-img-container:hover .modal-img {
          transform: scale(1.05);
        }

        .img-caption {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          background: rgba(10, 13, 22, 0.8);
          padding: 0.5rem;
          font-size: 0.75rem;
          text-align: center;
          backdrop-filter: blur(4px);
        }

        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes slide-up {
          from { transform: translateY(40px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }

        @media (max-width: 992px) {
          .modal-body-section {
            grid-template-columns: 1fr;
            gap: 2rem;
          }
        }

        @media (max-width: 768px) {
          .service-modal-content {
            padding: 2.5rem 1.5rem;
          }
          .modal-title {
            font-size: 1.4rem;
          }
        }
      `}</style>
    </section>
  )
}

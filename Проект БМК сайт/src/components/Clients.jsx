import React, { useState, useEffect } from 'react'
import { siteData } from '../data/siteData'
import { ChevronLeft, ChevronRight, Quote } from 'lucide-react'

export default function Clients() {
  const [activeReview, setActiveReview] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveReview((prev) => (prev + 1) % siteData.reviews.length)
    }, 8000) // Auto scroll reviews every 8 seconds
    return () => clearInterval(timer)
  }, [])

  const handlePrevReview = () => {
    setActiveReview((prev) => (prev - 1 + siteData.reviews.length) % siteData.reviews.length)
  }

  const handleNextReview = () => {
    setActiveReview((prev) => (prev + 1) % siteData.reviews.length)
  }

  return (
    <section id="clients" className="clients-section">
      <div className="bg-grid"></div>
      
      {/* Decorative Blob */}
      <div className="radial-blur blob-clients"></div>

      <div className="container">
        <h2 className="section-title">
          <span className="gradient-text">Наши клиенты и отзывы</span>
        </h2>
        <p className="section-subtitle">
          Мы гордимся долгосрочным партнерством с лидерами агропромышленного и фармацевтического секторов России.
        </p>

        {/* Clients Logos Infinite Scrolling Grid */}
        <div className="clients-logo-track-wrapper">
          <div className="clients-logo-track">
            {/* Double the array to make seamless scroll loop */}
            {[...siteData.clients, ...siteData.clients].map((client, idx) => (
              <div key={idx} className="client-logo-card glass">
                <img src={client.logo} alt={client.name} className="client-logo-img" />
                <span className="client-name-tooltip">{client.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Testimonials Slider */}
        <div className="reviews-slider-container" id="reviews">
          <h3 className="reviews-heading">Отзывы о нашей работе</h3>
          
          <div className="review-card-wrapper">
            <button className="slider-nav-btn prev-btn" onClick={handlePrevReview}>
              <ChevronLeft size={20} />
            </button>

            <div className="review-card glass">
              <Quote className="quote-icon" size={48} />
              
              <div className="review-body">
                <p className="review-text">
                  “{siteData.reviews[activeReview].text}”
                </p>
                <div className="review-meta">
                  <h4 className="review-company">
                    {siteData.reviews[activeReview].company}
                  </h4>
                  <span className="review-project">
                    Объект: {siteData.reviews[activeReview].project}
                  </span>
                </div>
              </div>
            </div>

            <button className="slider-nav-btn next-btn" onClick={handleNextReview}>
              <ChevronRight size={20} />
            </button>
          </div>

          {/* Dots Indicator */}
          <div className="slider-dots">
            {siteData.reviews.map((_, idx) => (
              <button
                key={idx}
                className={`dot-btn ${activeReview === idx ? 'active' : ''}`}
                onClick={() => setActiveReview(idx)}
              ></button>
            ))}
          </div>
        </div>
      </div>

      <style>{`
        .clients-section {
          background-color: #0b0f19;
          overflow: hidden;
          position: relative;
        }

        .blob-clients {
          width: 500px;
          height: 500px;
          background: rgba(0, 102, 255, 0.05);
          bottom: -10%;
          left: -10%;
        }

        /* Logos Infinite marquee animation */
        .clients-logo-track-wrapper {
          position: relative;
          width: 100%;
          overflow: hidden;
          margin-bottom: 7rem;
          padding: 1rem 0;
        }


        .clients-logo-track {
          display: flex;
          gap: 2rem;
          width: max-content;
          animation: scroll-marquee 90s linear infinite;
        }

        .clients-logo-track-wrapper::before,
        .clients-logo-track-wrapper::after {
          content: '';
          position: absolute;
          top: 0;
          bottom: 0;
          width: 150px;
          z-index: 5;
          pointer-events: none;
        }

        .clients-logo-track-wrapper::before {
          left: 0;
          background: linear-gradient(90deg, var(--bg-main) 0%, transparent 100%);
        }

        .clients-logo-track-wrapper::after {
          right: 0;
          background: linear-gradient(-90deg, var(--bg-main) 0%, transparent 100%);
        }

        .client-logo-card {
          padding: 1rem 2rem;
          width: 240px;
          height: 110px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: var(--radius-sm);
          position: relative;
        }

        .client-logo-img {
          max-width: 100%;
          max-height: 100%;
          filter: grayscale(1) opacity(0.6);
          transition: all var(--transition-fast);
        }

        .client-logo-card:hover .client-logo-img {
          filter: grayscale(0) opacity(1);
          transform: scale(1.05);
        }

        .client-name-tooltip {
          position: absolute;
          bottom: -10px;
          background: #ffffff;
          color: var(--text-main);
          border: 1px solid var(--border-color);
          padding: 0.3rem 0.6rem;
          font-size: 0.75rem;
          border-radius: 4px;
          opacity: 0;
          pointer-events: none;
          transition: all var(--transition-fast);
          white-space: nowrap;
          z-index: 10;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }

        .client-logo-card:hover .client-name-tooltip {
          opacity: 1;
          transform: translateY(-5px);
        }

        /* Testimonials styling */
        .reviews-heading {
          font-size: 1.5rem;
          margin-bottom: 3rem;
          font-family: var(--font-family-title);
          text-align: center;
          color: var(--text-main);
        }

        .review-card-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1.5rem;
          position: relative;
          max-width: 750px;
          margin: 0 auto;
        }

        .review-card {
          padding: 2.5rem;
          border-radius: var(--radius-lg);
          display: flex;
          flex-direction: column;
          position: relative;
          width: 100%;
          min-height: 260px;
          justify-content: center;
        }

        .quote-icon {
          position: absolute;
          top: 2rem;
          left: 2rem;
          color: rgba(0, 102, 255, 0.1);
        }

        .review-body {
          position: relative;
          z-index: 2;
        }

        .review-text {
          font-size: 1.05rem;
          line-height: 1.75;
          color: var(--text-main);
          margin-bottom: 1.5rem;
          font-style: italic;
        }

        .review-meta {
          border-top: 1px solid var(--border-color);
          padding-top: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 0.3rem;
        }

        .review-company {
          font-size: 1.1rem;
          font-weight: 700;
          color: var(--accent);
        }

        .review-project {
          color: var(--text-muted);
          font-size: 0.85rem;
        }

        .slider-nav-btn {
          background: #ffffff;
          border: 1px solid var(--border-color);
          color: var(--text-main);
          width: 50px;
          height: 50px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all var(--transition-fast);
          flex-shrink: 0;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
        }

        .slider-nav-btn:hover {
          background: #f1f5f9;
          border-color: var(--accent);
          color: var(--accent);
          transform: scale(1.05);
        }

        .slider-dots {
          display: flex;
          justify-content: center;
          gap: 0.8rem;
          margin-top: 2.5rem;
        }

        .dot-btn {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          border: none;
          background: var(--border-color);
          cursor: pointer;
          transition: all var(--transition-fast);
        }

        .dot-btn.active {
          background: var(--accent);
          width: 25px;
          border-radius: 10px;
          box-shadow: 0 0 10px var(--accent-glow);
        }

        @keyframes scroll-marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(calc(-240px * 20 - 2rem * 20)); }
        }

        @media (max-width: 768px) {
          .review-card {
            padding: 3rem 1.5rem;
            min-height: auto;
          }
          .review-text {
            font-size: 0.95rem;
            line-height: 1.6;
          }
          .slider-nav-btn {
            display: none;
          }
        }
      `}</style>
    </section>
  )
}
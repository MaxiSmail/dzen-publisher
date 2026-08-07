import React, { useState } from 'react'
import { siteData } from '../data/siteData'
import { Calendar, ChevronRight, Award, Compass, Truck, Shield } from 'lucide-react'

const advantageIcons = [
  Truck, // Собственный парк техники
  Shield, // Лицензии и СРО
  Award, // 15+ лет опыта
  Compass // География по всей России
]

const advantageTitles = [
  "Собственный парк спецтехники",
  "Лицензия МЧС и СРО допуски",
  "15+ лет опыта в инжиниринге",
  "Проекты по всей России"
]

const advantageDescs = [
  "В наличии весь спектр строительной техники от самосвалов и землеройных машин до подъемно-транспортных механизмов.",
  "Обладаем всеми необходимыми государственными лицензиями МЧС и допусками СРО на проектирование и строительство.",
  "Надежный технологический партнер. Успешно работаем с промышленным электромонтажом и безопасностью с 2009 года.",
  "Реализуем масштабные проекты по всей стране. Нам доверяют крупнейшие агрохолдинги и предприятия в РФ."
]

export default function About() {
  const [selectedMilestone, setSelectedMilestone] = useState(siteData.timeline.length - 1)

  return (
    <section id="about" className="about-section">
      <div className="bg-grid"></div>
      <div className="radial-blur blob-about"></div>

      <div className="container">
        <h2 className="section-title">
          <span className="gradient-text">О компании БМК</span>
        </h2>
        <p className="section-subtitle">
          Проектно-инжиниринговая компания БМК осуществляет полный цикл работ по проектированию, строительству и комплектации инженерным оборудованием.
        </p>

        {/* Company History Horizontal Interactive Timeline */}
        <div className="timeline-container glass">
          <h3 className="timeline-heading">История нашего развития</h3>
          
          <div className="timeline-track">
            <div className="timeline-line"></div>
            {siteData.timeline.map((item, index) => (
              <button 
                key={index} 
                className={`timeline-dot-wrapper ${selectedMilestone === index ? 'active' : ''}`}
                onClick={() => setSelectedMilestone(index)}
              >
                <div className="timeline-dot"></div>
                <span className="timeline-year">{item.year}</span>
              </button>
            ))}
          </div>

          <div className="timeline-milestone-content">
            <h4 className="milestone-title">
              <Calendar className="milestone-icon" size={20} />
              {siteData.timeline[selectedMilestone].title}
            </h4>
            <p className="milestone-desc">
              {siteData.timeline[selectedMilestone].desc}
            </p>
          </div>
        </div>

        {/* Advantages Cards Grid */}
        <div className="advantages-container">
          <h3 className="advantages-heading">Преимущества работы с нами</h3>
          <div className="advantages-grid">
            {advantageTitles.map((title, idx) => {
              const Icon = advantageIcons[idx]
              return (
                <div key={idx} className="advantage-card glass">
                  <div className="advantage-icon-wrapper">
                    <Icon size={24} className="advantage-icon" />
                  </div>
                  <h4 className="advantage-title">{title}</h4>
                  <p className="advantage-desc">{advantageDescs[idx]}</p>
                </div>
              )
            })}
          </div>
        </div>

        {/* Video Showcase */}
        <div className="video-showcase glass">
          <div className="video-side">
            <div className="video-embed-wrapper">
              <iframe
                src="https://www.youtube.com/embed/your-video-id?autoplay=0&rel=0&modestbranding=1"
                title="Видеовизитка ООО БМК"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="video-embed"
              ></iframe>
            </div>
          </div>
          <div className="video-text-side">
            <span className="video-label">Видеовизитка</span>
            <h3 className="video-title">Посмотрите, как мы работаем</h3>
            <p className="video-desc">
              За 15 лет мы реализовали сотни проектов по автоматизации, безопасности и энергоснабжению для крупнейших агрохолдингов и промышленных предприятий России. Смотрите наши объекты в деле.
            </p>
            <ul className="video-features">
              <li>🏗️ Полный цикл — от проекта до сдачи</li>
              <li>🛡️ Гарантия на все виды работ</li>
              <li>🌍 Объекты по всей России</li>
            </ul>
            <a href="#contacts" className="cta-button video-cta">Обсудить проект</a>
          </div>
        </div>
      </div>

      <style>{`
        .about-section {
          background-color: var(--bg-main);
          position: relative;
          border-bottom: 1px solid var(--border-color);
        }

        .blob-about {
          width: 450px;
          height: 450px;
          background: rgba(0, 102, 255, 0.04);
          top: 30%;
          left: 50%;
          transform: translate(-50%, -50%);
        }

        /* Timeline styling */
        .timeline-container {
          padding: 3rem;
          margin-bottom: 5rem;
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .timeline-heading {
          font-size: 1.5rem;
          margin-bottom: 3rem;
          font-family: var(--font-family-title);
          text-align: center;
        }

        .timeline-track {
          display: flex;
          justify-content: space-between;
          width: 100%;
          max-width: 800px;
          position: relative;
          margin-bottom: 3rem;
          padding: 0 1rem;
        }

        .timeline-line {
          position: absolute;
          top: 10px;
          left: 0;
          right: 0;
          height: 2px;
          background: var(--border-color);
          z-index: 1;
        }

        .timeline-dot-wrapper {
          background: none;
          border: none;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: center;
          position: relative;
          z-index: 2;
          width: 60px;
        }

        .timeline-dot {
          width: 22px;
          height: 22px;
          border-radius: 50%;
          background: #141c2f;
          border: 2px solid var(--border-color);
          margin-bottom: 0.8rem;
          transition: all var(--transition-fast);
        }

        .timeline-dot-wrapper:hover .timeline-dot {
          border-color: var(--accent);
          transform: scale(1.15);
        }

        .timeline-dot-wrapper.active .timeline-dot {
          background: var(--accent);
          border-color: var(--accent);
          box-shadow: 0 0 15px var(--accent-glow);
          transform: scale(1.2);
        }

        .timeline-year {
          font-family: var(--font-family-title);
          font-size: 0.9rem;
          font-weight: 700;
          color: var(--text-muted);
          transition: color var(--transition-fast);
        }

        .timeline-dot-wrapper.active .timeline-year {
          color: var(--accent);
        }

        .timeline-milestone-content {
          width: 100%;
          max-width: 700px;
          text-align: center;
          animation: fade-in-up 0.5s ease-out;
        }

        .milestone-title {
          font-size: 1.25rem;
          font-family: var(--font-family-title);
          font-weight: 700;
          color: var(--text-main);
          margin-bottom: 1rem;
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
        }

        .milestone-icon {
          color: var(--accent);
        }

        .milestone-desc {
          color: var(--text-muted);
          font-size: 0.95rem;
          line-height: 1.7;
        }

        /* Advantages Grid styling */
        .advantages-heading {
          font-size: 1.5rem;
          margin-bottom: 2.5rem;
          font-family: var(--font-family-title);
          text-align: center;
        }

        .advantages-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 2rem;
        }

        .advantage-card {
          padding: 2.5rem 2rem;
          border-radius: var(--radius-md);
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          height: 100%;
        }

        .advantage-icon-wrapper {
          padding: 0.8rem;
          background: rgba(0, 242, 254, 0.08);
          border: 1px solid rgba(0, 242, 254, 0.2);
          border-radius: var(--radius-sm);
          color: var(--accent);
          margin-bottom: 1.5rem;
        }

        .advantage-title {
          font-size: 1.1rem;
          font-weight: 700;
          margin-bottom: 0.8rem;
        }

        .advantage-desc {
          color: var(--text-muted);
          font-size: 0.88rem;
          line-height: 1.6;
        }

        /* Video showcase section */
        .video-showcase {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 3rem;
          margin-top: 5rem;
          padding: 3rem;
          border-radius: var(--radius-lg);
          align-items: center;
        }

        .video-embed-wrapper {
          position: relative;
          width: 100%;
          padding-bottom: 56.25%;
          border-radius: var(--radius-md);
          overflow: hidden;
          box-shadow: 0 20px 60px rgba(0, 102, 255, 0.2);
        }

        .video-embed {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border-radius: var(--radius-md);
          border: 1px solid var(--border-color);
        }

        .video-text-side {
          display: flex;
          flex-direction: column;
          gap: 1.2rem;
        }

        .video-label {
          display: inline-block;
          background: rgba(0, 242, 254, 0.12);
          color: var(--accent);
          border: 1px solid rgba(0, 242, 254, 0.3);
          padding: 0.3rem 0.8rem;
          border-radius: 100px;
          font-size: 0.8rem;
          font-weight: 600;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          width: fit-content;
        }

        .video-title {
          font-size: 1.8rem;
          font-family: var(--font-family-title);
          font-weight: 800;
          color: var(--text-main);
          line-height: 1.2;
        }

        .video-desc {
          color: var(--text-muted);
          font-size: 0.95rem;
          line-height: 1.7;
        }

        .video-features {
          list-style: none;
          display: flex;
          flex-direction: column;
          gap: 0.6rem;
        }

        .video-features li {
          color: var(--text-muted);
          font-size: 0.92rem;
        }

        .video-cta {
          margin-top: 0.5rem;
          width: fit-content;
        }

        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(15px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
          .timeline-container {
            padding: 2rem 1rem;
          }
          .timeline-track {
            overflow-x: auto;
            justify-content: flex-start;
            gap: 2rem;
            padding-bottom: 1rem;
          }
          .timeline-line {
            width: 500px;
          }
          .video-showcase {
            grid-template-columns: 1fr;
            padding: 2rem 1.5rem;
            gap: 2rem;
          }
          .video-title {
            font-size: 1.4rem;
          }
        }
      `}</style>
    </section>
  )
}

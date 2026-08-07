import React from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, ShieldCheck, Cpu, Zap, Activity } from 'lucide-react'

export default function Hero({ onContactClick, onManagementClick }) {
  return (
    <section className="hero-section">
      <div className="bg-grid"></div>
      
      {/* Decorative blurred blobs */}
      <div className="radial-blur blob-1"></div>
      <div className="radial-blur blob-2"></div>
      
      <div className="container hero-container">
        <motion.div 
          className="hero-content"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="badge-wrapper">
            <span className="hero-badge">
              <ShieldCheck size={14} className="badge-icon" />
              Лицензия МЧС и допуски СРО
            </span>
          </div>
          
          <h1 className="hero-title">
            Инженерные системы <br />
            <span className="accent-text">Безопасности и Автоматизации</span>
          </h1>
          
          <p className="hero-subtitle">
            Проектирование, промышленный электромонтаж, генеральный подряд и автоматизация под ключ для предприятий Москвы и регионов РФ.
          </p>
          
          <div className="hero-actions">
            <button className="btn btn-primary" onClick={onContactClick}>
              Заказать услугу <ArrowRight size={18} />
            </button>
            <button className="btn btn-secondary" onClick={onManagementClick}>
              <Activity size={16} className="text-cyan mr-2" /> Панель «БМК Управление»
            </button>
          </div>
        </motion.div>

        <motion.div 
          className="hero-visual"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          <div className="visual-card glass">
            {/* Interactive/Animated CSS Blueprint Grid */}
            <div className="blueprint-grid">
              <div className="blueprint-line h-line line-1"></div>
              <div className="blueprint-line h-line line-2"></div>
              <div className="blueprint-line h-line line-3"></div>
              <div className="blueprint-line v-line line-4"></div>
              <div className="blueprint-line v-line line-5"></div>
              
              {/* Nodes representing systems */}
              <motion.div 
                className="blueprint-node node-1"
                animate={{ y: [0, -6, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              >
                <Cpu size={24} className="node-icon" />
                <span className="node-label">АСУ ТП</span>
              </motion.div>
              <motion.div 
                className="blueprint-node node-2"
                animate={{ y: [0, 6, 0] }}
                transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut', delay: 1 }}
              >
                <ShieldCheck size={24} className="node-icon" />
                <span className="node-label">СКУД / ОПС</span>
              </motion.div>
              <motion.div 
                className="blueprint-node node-3"
                animate={{ y: [0, -5, 0] }}
                transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut', delay: 0.5 }}
              >
                <Zap size={24} className="node-icon" />
                <span className="node-label">Электромонтаж</span>
              </motion.div>
              
              {/* Glowing connection lines */}
              <svg className="connections-svg">
                <path d="M 120 180 L 320 100 L 260 280 Z" fill="none" stroke="rgba(0, 242, 254, 0.4)" strokeWidth="2" strokeDasharray="5,5" />
              </svg>
            </div>
            
            <div className="card-overlay-text">
              <span className="overlay-title">ООО «БМК»</span>
              <span className="overlay-desc">Работаем с 2009 года</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Metrics Bar */}
      <motion.div 
        className="container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <div className="metrics-bar glass">
          <div className="metric-item">
            <span className="metric-num">15+</span>
            <span className="metric-label">Лет на рынке</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-num">100+</span>
            <span className="metric-label">Крупных объектов</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-num">2 года</span>
            <span className="metric-label">Гарантии на работы</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-num">24/7</span>
            <span className="metric-label">Поддержка систем</span>
          </div>
        </div>
      </motion.div>

      <style>{`
        .hero-section {
          position: relative;
          padding: 140px 0 80px;
          min-height: 90vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          overflow: hidden;
        }
        .bg-grid {
          position: absolute;
          inset: 0;
          background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
          background-size: 32px 32px;
          opacity: 0.6;
          pointer-events: none;
        }
        .radial-blur {
          position: absolute;
          border-radius: 50%;
          filter: blur(120px);
          pointer-events: none;
        }
        .blob-1 {
          width: 500px;
          height: 500px;
          background: rgba(0, 242, 254, 0.12);
          top: -100px;
          left: -150px;
        }
        .blob-2 {
          width: 400px;
          height: 400px;
          background: rgba(79, 172, 254, 0.1);
          bottom: 0;
          right: -100px;
        }
        .hero-container {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 50px;
          align-items: center;
          margin-bottom: 60px;
        }
        .badge-wrapper {
          margin-bottom: 20px;
        }
        .hero-badge {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 6px 16px;
          border-radius: 20px;
          background: rgba(0, 242, 254, 0.08);
          border: 1px solid rgba(0, 242, 254, 0.3);
          color: #00f2fe;
          font-size: 0.85rem;
          font-weight: 600;
        }
        .hero-title {
          font-size: 3rem;
          line-height: 1.15;
          font-weight: 800;
          color: #fff;
          margin-bottom: 20px;
        }
        .accent-text {
          background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
          font-size: 1.1rem;
          color: #94a3b8;
          line-height: 1.6;
          margin-bottom: 32px;
          max-width: 540px;
        }
        .hero-actions {
          display: flex;
          gap: 16px;
        }
        .btn-secondary {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.12);
          color: #fff;
          padding: 12px 24px;
          border-radius: 12px;
          font-weight: 600;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          transition: all 0.2s;
        }
        .btn-secondary:hover {
          background: rgba(255, 255, 255, 0.1);
          border-color: rgba(0, 242, 254, 0.4);
        }
        .hero-visual {
          position: relative;
        }
        .visual-card {
          position: relative;
          height: 380px;
          border-radius: 24px;
          background: rgba(18, 26, 43, 0.6);
          border: 1px solid rgba(255, 255, 255, 0.1);
          overflow: hidden;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }
        .blueprint-grid {
          position: relative;
          width: 100%;
          height: 100%;
        }
        .blueprint-line {
          position: absolute;
          background: rgba(0, 242, 254, 0.15);
        }
        .h-line { height: 1px; width: 100%; }
        .v-line { width: 1px; height: 100%; }
        .line-1 { top: 25%; }
        .line-2 { top: 50%; }
        .line-3 { top: 75%; }
        .line-4 { left: 33%; }
        .line-5 { left: 66%; }
        .blueprint-node {
          position: absolute;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 6px;
          padding: 12px 18px;
          background: rgba(10, 15, 30, 0.85);
          border: 1px solid rgba(0, 242, 254, 0.4);
          border-radius: 14px;
          box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        }
        .node-1 { top: 20%; left: 15%; }
        .node-2 { top: 55%; left: 55%; }
        .node-3 { top: 25%; left: 65%; }
        .node-icon { color: #00f2fe; }
        .node-label { font-size: 0.78rem; font-weight: 700; color: #fff; }
        .connections-svg {
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
        }
        .card-overlay-text {
          position: absolute;
          bottom: 20px;
          left: 20px;
          display: flex;
          flex-direction: column;
        }
        .overlay-title { font-size: 1.1rem; font-weight: 800; color: #fff; }
        .overlay-desc { font-size: 0.8rem; color: #94a3b8; }
        .metrics-bar {
          display: flex;
          justify-content: space-around;
          align-items: center;
          padding: 24px 30px;
          border-radius: 20px;
          background: rgba(18, 26, 43, 0.5);
          border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .metric-item {
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        .metric-num {
          font-size: 1.8rem;
          font-weight: 800;
          color: #00f2fe;
        }
        .metric-label {
          font-size: 0.85rem;
          color: #94a3b8;
        }
        .metric-divider {
          width: 1px;
          height: 36px;
          background: rgba(255, 255, 255, 0.08);
        }
        .text-cyan { color: #00f2fe; }
        .mr-2 { margin-right: 8px; }
        @media (max-width: 992px) {
          .hero-container { grid-template-columns: 1fr; }
          .hero-title { font-size: 2.2rem; }
          .metrics-bar { flex-direction: column; gap: 16px; }
          .metric-divider { display: none; }
        }
      `}</style>
    </section>
  )
}

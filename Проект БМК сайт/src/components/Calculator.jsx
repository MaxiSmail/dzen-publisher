import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Calculator as CalcIcon, Check, ShieldCheck, ArrowRight, Sparkles } from 'lucide-react'

export default function Calculator({ onOrderClick }) {
  const [objectType, setObjectType] = useState('prom') // prom, log, office, retail
  const [area, setArea] = useState(1500)
  const [systems, setSystems] = useState({
    skud: true,
    ops: true,
    video: true,
    fireExtinguish: false,
    asu: false
  })

  const systemPrices = {
    skud: { name: 'СКУД (Контроль доступа)', perSqm: 120 },
    ops: { name: 'Охранно-пожарная сигнализация', perSqm: 150 },
    video: { name: 'Видеонаблюдение (IP / HD)', perSqm: 180 },
    fireExtinguish: { name: 'Автоматическое пожаротушение', perSqm: 320 },
    asu: { name: 'Диспетчеризация и АСУ ТП', perSqm: 250 }
  }

  const toggleSystem = (key) => {
    setSystems(prev => ({ ...prev, [key]: !prev[key] }))
  }

  // Calculation logic
  const calculateTotal = () => {
    let multiplier = 1.0
    if (objectType === 'prom') multiplier = 1.2
    if (objectType === 'log') multiplier = 1.0
    if (objectType === 'office') multiplier = 1.15
    if (objectType === 'retail') multiplier = 1.1

    let sumPerSqm = 0
    Object.keys(systems).forEach(key => {
      if (systems[key]) {
        sumPerSqm += systemPrices[key].perSqm
      }
    })

    const total = area * sumPerSqm * multiplier
    return Math.round(total)
  }

  const totalEstimate = calculateTotal()

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <motion.div 
          className="calc-header text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <div className="badge-wrapper">
            <span className="hero-badge">
              <CalcIcon size={14} /> Экспресс-расчет
            </span>
          </div>
          <h2 className="section-title">
            Калькулятор стоимости <span className="accent-text">Инженерных Систем</span>
          </h2>
          <p className="section-subtitle">
            Рассчитайте ориентировочную стоимость проектирования, оборудования и монтажа под ключ за 1 минуту.
          </p>
        </motion.div>

        <motion.div 
          className="calc-box glass"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <div className="calc-grid">
            {/* Options column */}
            <div className="calc-inputs">
              <div className="input-group">
                <label className="input-label">1. Тип объекта</label>
                <div className="type-buttons">
                  <button 
                    className={`type-btn ${objectType === 'prom' ? 'active' : ''}`}
                    onClick={() => setObjectType('prom')}
                  >
                    Пром. предприятие / Завод
                  </button>
                  <button 
                    className={`type-btn ${objectType === 'log' ? 'active' : ''}`}
                    onClick={() => setObjectType('log')}
                  >
                    Склад / Логистика
                  </button>
                  <button 
                    className={`type-btn ${objectType === 'office' ? 'active' : ''}`}
                    onClick={() => setObjectType('office')}
                  >
                    Бизнес-центр / Офисы
                  </button>
                  <button 
                    className={`type-btn ${objectType === 'retail' ? 'active' : ''}`}
                    onClick={() => setObjectType('retail')}
                  >
                    Торговый центр
                  </button>
                </div>
              </div>

              <div className="input-group">
                <div className="label-with-val">
                  <label className="input-label">2. Площадь объекта (м²)</label>
                  <span className="area-val">{area.toLocaleString()} м²</span>
                </div>
                <input 
                  type="range" 
                  min="100" 
                  max="20000" 
                  step="100" 
                  value={area} 
                  onChange={(e) => setArea(Number(e.target.value))}
                  className="area-slider"
                />
              </div>

              <div className="input-group">
                <label className="input-label">3. Требуемые системы</label>
                <div className="systems-list">
                  {Object.keys(systemPrices).map((key) => (
                    <div 
                      key={key} 
                      className={`system-checkbox ${systems[key] ? 'checked' : ''}`}
                      onClick={() => toggleSystem(key)}
                    >
                      <div className="checkbox-box">
                        {systems[key] && <Check size={14} />}
                      </div>
                      <span>{systemPrices[key].name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Results summary column */}
            <div className="calc-summary glass-card">
              <div className="summary-title">
                <Sparkles size={20} className="text-cyan" /> Итоговая оценка
              </div>
              
              <div className="price-display">
                <div className="price-num">{totalEstimate.toLocaleString()} ₽</div>
                <div className="price-note">*Включает проект, оборудование, монтаж и пусконаладку</div>
              </div>

              <div className="summary-features">
                <div className="s-feat">
                  <ShieldCheck size={16} className="text-cyan" /> Гарантия на работы 24 месяца
                </div>
                <div className="s-feat">
                  <ShieldCheck size={16} className="text-cyan" /> Полный комплект документации для МЧС
                </div>
              </div>

              <button className="btn btn-primary w-full shadow-cyan" onClick={onOrderClick}>
                Получить точную смету <ArrowRight size={18} />
              </button>
            </div>
          </div>
        </motion.div>
      </div>

      <style>{`
        .calculator-section {
          padding: 90px 0;
          position: relative;
        }
        .calc-box {
          margin-top: 40px;
          padding: 40px;
          border-radius: 24px;
          background: rgba(18, 26, 43, 0.6);
          border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .calc-grid {
          display: grid;
          grid-template-columns: 1fr 380px;
          gap: 40px;
        }
        .input-group {
          margin-bottom: 28px;
        }
        .input-label {
          display: block;
          font-size: 0.95rem;
          font-weight: 600;
          color: #e2e8f0;
          margin-bottom: 12px;
        }
        .type-buttons {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
        }
        .type-btn {
          padding: 12px;
          border-radius: 10px;
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.08);
          color: #94a3b8;
          font-size: 0.85rem;
          cursor: pointer;
          transition: all 0.2s;
          text-align: left;
        }
        .type-btn.active {
          background: rgba(0, 242, 254, 0.12);
          border-color: rgba(0, 242, 254, 0.4);
          color: #00f2fe;
          font-weight: 600;
        }
        .label-with-val {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .area-val {
          font-size: 1.1rem;
          font-weight: 700;
          color: #00f2fe;
        }
        .area-slider {
          width: 100%;
          accent-color: #00f2fe;
          cursor: pointer;
        }
        .systems-list {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .system-checkbox {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 16px;
          border-radius: 10px;
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid rgba(255, 255, 255, 0.06);
          cursor: pointer;
          transition: all 0.2s;
          color: #cbd5e1;
          font-size: 0.9rem;
        }
        .system-checkbox.checked {
          background: rgba(0, 242, 254, 0.06);
          border-color: rgba(0, 242, 254, 0.3);
          color: #fff;
        }
        .checkbox-box {
          width: 20px;
          height: 20px;
          border-radius: 6px;
          border: 1px solid rgba(255, 255, 255, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          color: #00f2fe;
        }
        .system-checkbox.checked .checkbox-box {
          border-color: #00f2fe;
          background: rgba(0, 242, 254, 0.2);
        }
        .calc-summary {
          padding: 30px;
          border-radius: 18px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(0, 242, 254, 0.04));
          border: 1px solid rgba(0, 242, 254, 0.2);
        }
        .summary-title {
          font-size: 1.1rem;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .price-num {
          font-size: 2.2rem;
          font-weight: 800;
          background: linear-gradient(90deg, #fff, #00f2fe);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          margin: 16px 0 4px;
        }
        .price-note {
          font-size: 0.78rem;
          color: #64748b;
        }
        .summary-features {
          margin: 24px 0;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .s-feat {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.85rem;
          color: #cbd5e1;
        }
        .shadow-cyan {
          box-shadow: 0 10px 30px -5px rgba(0, 242, 254, 0.4);
        }
        @media (max-width: 992px) {
          .calc-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </section>
  )
}

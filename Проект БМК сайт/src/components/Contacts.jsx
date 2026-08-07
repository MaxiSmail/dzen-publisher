import React, { useState } from 'react'
import { Phone, Mail, MapPin, Send, CheckCircle } from 'lucide-react'

export default function Contacts() {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    service: '',
    message: ''
  })
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.name || !formData.phone) return

    setLoading(true)
    // Simulate API request
    setTimeout(() => {
      setLoading(false)
      setSubmitted(true)
      setFormData({ name: '', phone: '', service: '', message: '' })
    }, 1500)
  }

  const servicesList = [
    "Генеральный подряд",
    "Проектирование систем безопасности",
    "Автоматизация (АСУ ТП / Диспетчеризация)",
    "Электромонтажные работы",
    "Пожарная безопасность (АПС / СОУЭ)",
    "Системы пожаротушения",
    "Другое"
  ]

  return (
    <section id="contacts" className="contacts-section">
      <div className="bg-grid"></div>
      <div className="radial-blur blob-contacts"></div>

      <div className="container">
        <h2 className="section-title">
          <span className="gradient-text">Связаться с нами</span>
        </h2>
        <p className="section-subtitle">
          Оставьте заявку, и наши инженеры свяжутся с вами для обсуждения вашего проекта или составления сметы.
        </p>

        <div className="contacts-grid">
          {/* Contacts details & map */}
          <div className="contacts-info-column">
            <div className="info-cards">
              <div className="info-card glass">
                <MapPin className="info-icon" size={20} />
                <div className="info-text">
                  <h5>Адрес офиса</h5>
                  <p>Россия, Московская область, г. Московский, ул. Хабарова, 2, ТРЦ Новомосковский, оф. 18</p>
                </div>
              </div>

              <div className="info-card glass">
                <Phone className="info-icon" size={20} />
                <div className="info-text">
                  <h5>Телефоны</h5>
                  <p>
                    <a href="tel:+79803239999" className="info-link">8 (980) 323-99-99</a> (Моб.)
                  </p>
                  <p>
                    <a href="tel:+74722402400" className="info-link">8 (4722) 40-24-00</a> (Офис)
                  </p>
                </div>
              </div>

              <div className="info-card glass">
                <Mail className="info-icon" size={20} />
                <div className="info-text">
                  <h5>Электронная почта</h5>
                  <p>
                    <a href="mailto:info@bmk-31.ru" className="info-link">info@bmk-31.ru</a>
                  </p>
                  <p>
                    <a href="mailto:v.shmelyov_bmk@mail.ru" className="info-link">v.shmelyov_bmk@mail.ru</a>
                  </p>
                </div>
              </div>
            </div>

            {/* Embedded Yandex Map */}
            <div className="map-container glass">
              <iframe 
                title="Yandex Map"
                src="https://yandex.ru/map-widget/v1/?text=г.%20Московский%2C%20ул.%20Хабарова%2C%202%2C%20ТРЦ%20Новомосковский&z=15"
                width="100%" 
                height="100%" 
                frameBorder="0" 
                allowFullScreen={true}
                className="yandex-map-iframe"
              ></iframe>
            </div>
          </div>

          {/* Contact form card */}
          <div className="contacts-form-column">
            <div className="form-card glass">
              {submitted ? (
                <div className="success-message">
                  <CheckCircle size={64} className="success-icon" />
                  <h4>Заявка успешно отправлена!</h4>
                  <p>Наш технический специалист свяжется с вами в течение 30 минут для уточнения деталей.</p>
                  <button className="btn btn-secondary" onClick={() => setSubmitted(false)}>
                    Отправить еще одну заявку
                  </button>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="contact-form">
                  <h3 className="form-title">Быстрый расчет сметы</h3>
                  
                  <div className="form-group">
                    <label htmlFor="name">Ваше имя *</label>
                    <input 
                      type="text" 
                      id="name" 
                      name="name" 
                      required
                      placeholder="Иван Иванов" 
                      value={formData.name}
                      onChange={handleChange}
                      className="form-input"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="phone">Номер телефона *</label>
                    <input 
                      type="tel" 
                      id="phone" 
                      name="phone" 
                      required
                      placeholder="+7 (999) 999-99-99" 
                      value={formData.phone}
                      onChange={handleChange}
                      className="form-input"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="service">Направление работ</label>
                    <select 
                      id="service" 
                      name="service"
                      value={formData.service}
                      onChange={handleChange}
                      className="form-select"
                    >
                      <option value="">Выберите услугу...</option>
                      {servicesList.map((service, idx) => (
                        <option key={idx} value={service}>{service}</option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="message">Сообщение / Описание проекта</label>
                    <textarea 
                      id="message" 
                      name="message" 
                      placeholder="Опишите ваши требования, желаемые сроки или особенности объекта..."
                      rows="4"
                      value={formData.message}
                      onChange={handleChange}
                      className="form-textarea"
                    ></textarea>
                  </div>

                  <button 
                    type="submit" 
                    disabled={loading}
                    className="btn btn-primary form-submit-btn"
                  >
                    {loading ? (
                      "Отправка..."
                    ) : (
                      <>
                        Отправить запрос <Send size={16} />
                      </>
                    )}
                  </button>
                  
                  <span className="privacy-note">
                    Нажимая кнопку, вы соглашаетесь на обработку персональных данных.
                  </span>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .contacts-section {
          background-color: var(--bg-main);
          position: relative;
          border-bottom: 1px solid var(--border-color);
        }

        .blob-contacts {
          width: 500px;
          height: 500px;
          background: rgba(0, 242, 254, 0.05);
          top: 10%;
          right: -10%;
        }

        .contacts-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 3rem;
          align-items: start;
        }

        .info-cards {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
          margin-bottom: 2rem;
        }

        .info-card {
          display: flex;
          gap: 1.5rem;
          padding: 1.8rem;
          align-items: flex-start;
          border-radius: var(--radius-md);
        }

        .info-icon {
          color: var(--accent);
          flex-shrink: 0;
          margin-top: 3px;
        }

        .info-text h5 {
          font-size: 1.05rem;
          font-weight: 700;
          margin-bottom: 0.5rem;
        }

        .info-text p {
          color: var(--text-muted);
          font-size: 0.9rem;
          line-height: 1.5;
        }

        .info-link {
          color: var(--text-main);
          text-decoration: none;
          font-weight: 600;
          transition: color var(--transition-fast);
        }

        .info-link:hover {
          color: var(--accent);
        }

        /* Map styling */
        .map-container {
          height: 250px;
          border-radius: var(--radius-md);
          overflow: hidden;
          position: relative;
          border: 1px solid var(--border-color);
        }

        .yandex-map-iframe {
          filter: grayscale(0.8) invert(0.9) contrast(1.1); /* Stylize map under dark mode */
          transition: filter var(--transition-normal);
        }

        .map-container:hover .yandex-map-iframe {
          filter: none;
        }

        /* Form styling */
        .form-card {
          padding: 3rem;
          border-radius: var(--radius-lg);
        }

        .form-title {
          font-size: 1.5rem;
          margin-bottom: 2rem;
          font-family: var(--font-family-title);
          text-align: center;
        }

        .contact-form {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .form-group label {
          font-size: 0.85rem;
          font-weight: 600;
          color: var(--text-muted);
        }

        .form-input,
        .form-select,
        .form-textarea {
          background: rgba(10, 13, 22, 0.5);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-sm);
          padding: 0.8rem 1rem;
          color: var(--text-main);
          font-family: var(--font-family-body);
          font-size: 0.9rem;
          transition: all var(--transition-fast);
        }

        .form-input:focus,
        .form-select:focus,
        .form-textarea:focus {
          outline: none;
          border-color: var(--accent);
          box-shadow: 0 0 10px var(--accent-glow);
        }

        .form-select option {
          background: #0a0d16;
          color: var(--text-main);
        }

        .form-submit-btn {
          margin-top: 1rem;
          width: 100%;
        }

        .privacy-note {
          font-size: 0.75rem;
          color: var(--text-muted);
          text-align: center;
          margin-top: 0.5rem;
        }

        /* Success message state */
        .success-message {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          gap: 1.5rem;
          padding: 2rem 0;
          animation: fade-in-up 0.5s ease-out;
        }

        .success-icon {
          color: var(--accent);
          animation: scale-up 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .success-message h4 {
          font-size: 1.4rem;
        }

        .success-message p {
          color: var(--text-muted);
          font-size: 0.95rem;
          margin-bottom: 1.5rem;
        }

        @keyframes scale-up {
          from { transform: scale(0); }
          to { transform: scale(1); }
        }

        @media (max-width: 992px) {
          .contacts-grid {
            grid-template-columns: 1fr;
            gap: 4rem;
          }
        }
      `}</style>
    </section>
  )
}

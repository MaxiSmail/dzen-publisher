import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Send, CheckCircle } from 'lucide-react'

export default function Modal({ isOpen, onClose }) {
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
    setTimeout(() => {
      setLoading(false)
      setSubmitted(true)
      setFormData({ name: '', phone: '', service: '', message: '' })
    }, 1500)
  }

  const handleClose = () => {
    setSubmitted(false)
    onClose()
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
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          className="request-modal-overlay" 
          onClick={handleClose}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
        >
          <motion.div 
            className="request-modal-content glass" 
            onClick={(e) => e.stopPropagation()}
            initial={{ scale: 0.9, y: 30, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.9, y: 30, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 220 }}
          >
            <button className="modal-close-btn" onClick={handleClose}>
              <X size={24} />
            </button>

            {submitted ? (
              <motion.div 
                className="success-message"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4 }}
              >
                <CheckCircle size={64} className="success-icon" />
                <h4>Заявка успешно принята!</h4>
                <p>Наш ведущий инженер свяжется с вами в течение 30 минут для проведения первичной консультации.</p>
                <button className="btn btn-primary" onClick={handleClose}>
                  Отлично
                </button>
              </motion.div>
            ) : (
              <form onSubmit={handleSubmit} className="modal-form">
                <h3 className="modal-form-title">Заявка на инженерные услуги</h3>
                <p className="modal-form-subtitle">Заполните поля, и мы подготовим для вас индивидуальное коммерческое предложение.</p>

                <div className="form-group">
                  <label htmlFor="modal-name">Ваше имя *</label>
                  <input 
                    type="text" 
                    id="modal-name" 
                    name="name" 
                    required
                    placeholder="Иван Иванов" 
                    value={formData.name}
                    onChange={handleChange}
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="modal-phone">Номер телефона *</label>
                  <input 
                    type="tel" 
                    id="modal-phone" 
                    name="phone" 
                    required
                    placeholder="+7 (999) 999-99-99" 
                    value={formData.phone}
                    onChange={handleChange}
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="modal-service">Направление работ</label>
                  <select 
                    id="modal-service" 
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
                  <label htmlFor="modal-message">Описание объекта или задачи</label>
                  <textarea 
                    id="modal-message" 
                    name="message" 
                    placeholder="Расскажите о вашем объекте, требуемых работах или прикрепите ссылку на ТЗ..."
                    rows="3"
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
                  Нажимая кнопку, вы даете согласие на обработку персональных данных.
                </span>
              </form>
            )}
          </motion.div>
        </motion.div>
      )}
      
      <style>{`
        .request-modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(15, 23, 42, 0.45);
          backdrop-filter: blur(8px);
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
        }

        .request-modal-content {
          width: 100%;
          max-width: 550px;
          background: #ffffff;
          border: 1px solid var(--border-color);
          padding: 3rem;
          position: relative;
          border-radius: var(--radius-md);
          box-shadow: 0 50px 100px rgba(15, 23, 42, 0.15);
        }

        .modal-close-btn {
          position: absolute;
          top: 1.5rem;
          right: 1.5rem;
          background: #f1f5f9;
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
          background: #e2e8f0;
          border-color: var(--accent);
          transform: rotate(90deg);
        }

        .modal-form {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .modal-form-title {
          font-size: 1.6rem;
          font-weight: 900;
          color: var(--primary);
          text-align: center;
          text-transform: uppercase;
        }

        .modal-form-subtitle {
          font-size: 0.9rem;
          color: var(--text-muted);
          text-align: center;
          margin-top: -0.5rem;
          line-height: 1.5;
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
          background: #ffffff;
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
          background: #ffffff;
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

        .success-message {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          gap: 1.5rem;
          padding: 2rem 0;
        }

        .success-icon {
          color: var(--accent);
        }

        .success-message h4 {
          font-size: 1.4rem;
          color: var(--primary);
        }

        .success-message p {
          color: var(--text-muted);
          font-size: 0.95rem;
          margin-bottom: 1.5rem;
        }
      `}</style>
    </AnimatePresence>
  )
}

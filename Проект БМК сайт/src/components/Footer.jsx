import React from 'react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="site-footer">
      <div className="container footer-container">
        <div className="footer-brand">
          <a href="#" className="footer-logo">
            <img src="https://bmk-company.ru/files/110/logo0.svg" alt="БМК" className="footer-logo-img" />
            <div className="footer-logo-text">
              <span className="logo-title">БМК</span>
              <span className="logo-sub">Строительно-монтажная компания</span>
            </div>
          </a>
          <p className="footer-desc">
            Проектирование и монтаж комплексных систем безопасности, автоматизации технологических процессов и промышленного электроснабжения с 2009 года.
          </p>
        </div>

        <div className="footer-links-column">
          <h5>Услуги</h5>
          <a href="#services" className="footer-link">Генеральный подряд</a>
          <a href="#services" className="footer-link">Проектирование систем</a>
          <a href="#services" className="footer-link">Автоматизация АСУ ТП</a>
          <a href="#services" className="footer-link">Электромонтаж</a>
        </div>

        <div className="footer-links-column">
          <h5>Навигация</h5>
          <a href="#services" className="footer-link">Направления</a>
          <a href="#about" className="footer-link">О компании</a>
          <a href="#reviews" className="footer-link">Отзывы</a>
          <a href="#licenses" className="footer-link">Лицензии</a>
        </div>

        <div className="footer-links-column">
          <h5>Связь</h5>
          <span className="footer-contact-item">Тел: <a href="tel:+79803239999">8 (980) 323-99-99</a></span>
          <span className="footer-contact-item">Почта: <a href="mailto:info@bmk-31.ru">info@bmk-31.ru</a></span>
          <span className="footer-contact-item">Офис: оф. 18, ТРЦ Новомосковский</span>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="container bottom-container">
          <span className="copy-text">
            &copy; 2009 - {currentYear} ООО «БМК». Все права защищены.
          </span>
          <div className="bottom-links">
            <a href="#" className="bottom-link">Политика конфиденциальности</a>
            <span className="link-separator">|</span>
            <a href="#" className="bottom-link">Персональные данные</a>
          </div>
        </div>
      </div>

      <style>{`
        .site-footer {
          background-color: #080a10;
          border-top: 1px solid var(--border-color);
          padding-top: 5rem;
          padding-bottom: 2rem;
          position: relative;
          z-index: 10;
        }

        .footer-container {
          display: grid;
          grid-template-columns: 1.5fr 1fr 1fr 1fr;
          gap: 3rem;
          margin-bottom: 4rem;
        }

        .footer-brand {
          display: flex;
          flex-direction: column;
          gap: 1.2rem;
        }

        .footer-logo {
          display: flex;
          align-items: center;
          gap: 0.8rem;
          text-decoration: none;
          color: var(--text-main);
        }

        .footer-logo-img {
          height: 36px;
        }

        .footer-logo-text {
          display: flex;
          flex-direction: column;
        }

        .footer-desc {
          color: var(--text-muted);
          font-size: 0.9rem;
          line-height: 1.6;
        }

        .footer-links-column {
          display: flex;
          flex-direction: column;
          gap: 0.8rem;
        }

        .footer-links-column h5 {
          color: var(--text-main);
          font-size: 1rem;
          margin-bottom: 0.5rem;
          font-family: var(--font-family-title);
          font-weight: 700;
        }

        .footer-link {
          color: var(--text-muted);
          text-decoration: none;
          font-size: 0.9rem;
          transition: color var(--transition-fast);
        }

        .footer-link:hover {
          color: var(--accent);
        }

        .footer-contact-item {
          color: var(--text-muted);
          font-size: 0.9rem;
        }

        .footer-contact-item a {
          color: var(--text-muted);
          text-decoration: none;
          transition: color var(--transition-fast);
        }

        .footer-contact-item a:hover {
          color: var(--accent);
        }

        .footer-bottom {
          border-top: 1px solid var(--border-color);
          padding-top: 2rem;
        }

        .bottom-container {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .copy-text {
          color: var(--text-muted);
          font-size: 0.85rem;
        }

        .bottom-links {
          display: flex;
          align-items: center;
          gap: 0.8rem;
          color: var(--text-muted);
          font-size: 0.85rem;
        }

        .bottom-link {
          color: var(--text-muted);
          text-decoration: none;
          transition: color var(--transition-fast);
        }

        .bottom-link:hover {
          color: var(--accent);
        }

        .link-separator {
          color: var(--border-color);
        }

        @media (max-width: 768px) {
          .footer-container {
            grid-template-columns: 1fr;
            gap: 2rem;
          }
          .bottom-container {
            flex-direction: column;
            text-align: center;
          }
        }
      `}</style>
    </footer>
  )
}
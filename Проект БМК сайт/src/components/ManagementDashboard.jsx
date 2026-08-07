import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  X, Activity, CheckCircle2, Clock, AlertTriangle, FileText, 
  Layers, Shield, Cpu, Building2, Wrench, ChevronRight, UserCheck
} from 'lucide-react'

export default function ManagementDashboard({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('projects')
  const [selectedProject, setSelectedProject] = useState(0)

  if (!isOpen) return null

  const mockProjects = [
    {
      id: 'BMK-2026-01',
      name: 'Промышленный комплекс «Агро-Технология»',
      type: 'Генеральный подряд & АСУ ТП',
      progress: 84,
      status: 'В работе',
      statusColor: '#00f2fe',
      location: 'Московская обл., Наро-Фоминск',
      manager: 'Алексеев В. С.',
      stages: [
        { title: 'Проектирование СКУД и ОПС', status: 'completed', date: '15.01.2026' },
        { title: 'Поставка оборудования и шкафов АСУ', status: 'completed', date: '02.02.2026' },
        { title: 'Монтаж силовых кабельных трасс', status: 'in-progress', date: ' В процессе (85%)' },
        { title: 'Пусконаладка и сдача МЧС', status: 'pending', date: 'Запланировано на 20.02.2026' }
      ],
      stats: {
        sensors: 340,
        cameras: 64,
        cablesKm: 14.2
      }
    },
    {
      id: 'BMK-2026-02',
      name: 'Логистический терминал «Восток»',
      type: 'Системы противопожарной защиты',
      progress: 95,
      status: 'Тестирование',
      statusColor: '#10b981',
      location: 'Москва, Новая Москва',
      manager: 'Григорьев М. В.',
      stages: [
        { title: 'Разработка рабочей документации', status: 'completed', date: '10.12.2025' },
        { title: 'Установка сплинкерного пожаротушения', status: 'completed', date: '20.01.2026' },
        { title: 'Комплексные испытания автоматики', status: 'in-progress', date: 'Завершение 10.02' },
        { title: 'Передача исполнительной документации', status: 'pending', date: 'Ожидает подписи' }
      ],
      stats: {
        sensors: 520,
        cameras: 110,
        cablesKm: 28.5
      }
    },
    {
      id: 'BMK-2026-03',
      name: 'Торгово-офисный центр «Арбат Плаза»',
      type: 'СКУД & Серверная автоматика',
      progress: 45,
      status: 'Монтаж',
      statusColor: '#f59e0b',
      location: 'Москва, ЦАО',
      manager: 'Дмитриев Е. К.',
      stages: [
        { title: 'Согласование ТЗ и Сметы', status: 'completed', date: '18.01.2026' },
        { title: 'Установка биометрических турникетов', status: 'in-progress', date: 'В процессе (50%)' },
        { title: 'Интеграция с 1С:Управление персоналом', status: 'pending', date: 'Старт 15.02.2026' },
        { title: 'Финишные пусконаладочные работы', status: 'pending', date: 'Март 2026' }
      ],
      stats: {
        sensors: 180,
        cameras: 42,
        cablesKm: 8.7
      }
    }
  ]

  const current = mockProjects[selectedProject]

  return (
    <AnimatePresence>
      <div className="dash-backdrop" onClick={onClose}>
        <motion.div 
          className="dash-window glass"
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          transition={{ duration: 0.3 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="dash-header">
            <div className="dash-brand">
              <div className="dash-icon-box">
                <Activity size={24} className="accent-icon" />
              </div>
              <div>
                <div className="dash-title">БМК Управление</div>
                <div className="dash-sub">Панель мониторинга проектов и инженерных объектов</div>
              </div>
            </div>
            <button className="dash-close" onClick={onClose}>
              <X size={20} />
            </button>
          </div>

          {/* Navigation Tabs */}
          <div className="dash-tabs">
            <button 
              className={`dash-tab ${activeTab === 'projects' ? 'active' : ''}`}
              onClick={() => setActiveTab('projects')}
            >
              <Building2 size={16} /> Мои Объекты ({mockProjects.length})
            </button>
            <button 
              className={`dash-tab ${activeTab === 'docs' ? 'active' : ''}`}
              onClick={() => setActiveTab('docs')}
            >
              <FileText size={16} /> Исполнительная документация
            </button>
            <button 
              className={`dash-tab ${activeTab === 'support' ? 'active' : ''}`}
              onClick={() => setActiveTab('support')}
            >
              <Wrench size={16} /> Диспетчер 24/7
            </button>
          </div>

          {/* Body */}
          <div className="dash-body">
            {activeTab === 'projects' && (
              <div className="dash-grid">
                {/* Left project list */}
                <div className="projects-sidebar">
                  {mockProjects.map((p, idx) => (
                    <div 
                      key={p.id}
                      className={`project-card ${selectedProject === idx ? 'selected' : ''}`}
                      onClick={() => setSelectedProject(idx)}
                    >
                      <div className="card-top">
                        <span className="p-id">{p.id}</span>
                        <span className="p-status" style={{ color: p.statusColor, borderColor: p.statusColor }}>
                          {p.status}
                        </span>
                      </div>
                      <div className="p-name">{p.name}</div>
                      <div className="p-type">{p.type}</div>
                      <div className="progress-bar-bg">
                        <div className="progress-bar-fill" style={{ width: `${p.progress}%`, backgroundColor: p.statusColor }}></div>
                      </div>
                      <div className="progress-text">{p.progress}% Готовности</div>
                    </div>
                  ))}
                </div>

                {/* Right project details */}
                <div className="project-detail glass-card">
                  <div className="detail-header">
                    <div>
                      <span className="detail-tag">{current.type}</span>
                      <h3 className="detail-title">{current.name}</h3>
                      <div className="detail-loc">{current.location}</div>
                    </div>
                    <div className="manager-info">
                      <UserCheck size={16} /> Руководитель: <strong>{current.manager}</strong>
                    </div>
                  </div>

                  {/* Metrics Row */}
                  <div className="detail-metrics">
                    <div className="m-box">
                      <Cpu size={20} className="m-icon" />
                      <div className="m-val">{current.stats.sensors}</div>
                      <div className="m-lbl">Датчиков и модулей</div>
                    </div>
                    <div className="m-box">
                      <Shield size={20} className="m-icon" />
                      <div className="m-val">{current.stats.cameras}</div>
                      <div className="m-lbl">Камер видеонаблюдения</div>
                    </div>
                    <div className="m-box">
                      <Layers size={20} className="m-icon" />
                      <div className="m-val">{current.stats.cablesKm} км</div>
                      <div className="m-lbl">Кабельных трасс</div>
                    </div>
                  </div>

                  {/* Stages timeline */}
                  <div className="stages-wrapper">
                    <h4>График выполнения работ</h4>
                    <div className="stages-list">
                      {current.stages.map((st, i) => (
                        <div key={i} className={`stage-item ${st.status}`}>
                          <div className="stage-icon">
                            {st.status === 'completed' && <CheckCircle2 size={18} className="text-success" />}
                            {st.status === 'in-progress' && <Clock size={18} className="text-warning spin-slow" />}
                            {st.status === 'pending' && <AlertTriangle size={18} className="text-muted" />}
                          </div>
                          <div className="stage-info">
                            <div className="stage-title">{st.title}</div>
                            <div className="stage-date">{st.date}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'docs' && (
              <div className="docs-panel glass-card">
                <h3>Реестр исполнительной документации</h3>
                <p>Все акты, чертежи, лицензии МЧС и сертификаты соответствия по вашему объекту доступны для скачивания в 1 клик.</p>

                <div className="docs-table">
                  <div className="doc-row header">
                    <span>Наименование документа</span>
                    <span>Формат</span>
                    <span>Статус</span>
                    <span>Действие</span>
                  </div>
                  <div className="doc-row">
                    <span>Акт освидетельствования скрытых работ (АОСР-01)</span>
                    <span>PDF / XLSX</span>
                    <span className="badge-ok">Подписан</span>
                    <button className="btn-link">Скачать</button>
                  </div>
                  <div className="doc-row">
                    <span>Проектная документация стадии "Р" (СКУД, АСУ)</span>
                    <span>DWG / PDF</span>
                    <span className="badge-ok">Согласовано</span>
                    <button className="btn-link">Скачать</button>
                  </div>
                  <div className="doc-row">
                    <span>Лицензия МЧС на монтаж противопожарных систем</span>
                    <span>PDF</span>
                    <span className="badge-ok">Действительна</span>
                    <button className="btn-link">Скачать</button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'support' && (
              <div className="support-panel glass-card">
                <h3>Круглосуточный диспетчерский центр ООО «БМК»</h3>
                <p>В случае сбоя или необходимости экстренного выезда инженерной бригады вы можете отправить заявку мгновенно.</p>
                <div className="support-contacts">
                  <div className="s-card">
                    <strong>Горячая линия 24/7</strong>
                    <a href="tel:+79803239999" className="s-phone">8 (980) 323-99-99</a>
                  </div>
                  <div className="s-card">
                    <strong>Инженерная служба</strong>
                    <span>support@bmk-company.ru</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        <style>{`
          .dash-backdrop {
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(10, 15, 30, 0.85);
            backdrop-filter: blur(12px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
          }
          .dash-window {
            width: 100%;
            max-width: 1100px;
            height: 85vh;
            max-height: 750px;
            border-radius: 20px;
            background: rgba(18, 26, 43, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            color: #fff;
          }
          .dash-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 28px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          }
          .dash-brand {
            display: flex;
            align-items: center;
            gap: 14px;
          }
          .dash-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(79, 172, 254, 0.2));
            border: 1px solid rgba(0, 242, 254, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .dash-title {
            font-size: 1.25rem;
            font-weight: 700;
            background: linear-gradient(90deg, #fff, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
          }
          .dash-sub {
            font-size: 0.82rem;
            color: #94a3b8;
          }
          .dash-close {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #cbd5e1;
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
          }
          .dash-close:hover {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
          }
          .dash-tabs {
            display: flex;
            gap: 8px;
            padding: 12px 28px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            background: rgba(10, 16, 28, 0.5);
          }
          .dash-tab {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 10px;
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
          }
          .dash-tab.active {
            background: rgba(0, 242, 254, 0.12);
            color: #00f2fe;
            border: 1px solid rgba(0, 242, 254, 0.3);
          }
          .dash-body {
            flex: 1;
            padding: 24px 28px;
            overflow-y: auto;
          }
          .dash-grid {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 24px;
            height: 100%;
          }
          .projects-sidebar {
            display: flex;
            flex-direction: column;
            gap: 12px;
          }
          .project-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 14px;
            cursor: pointer;
            transition: all 0.2s;
          }
          .project-card.selected {
            background: rgba(0, 242, 254, 0.08);
            border-color: rgba(0, 242, 254, 0.4);
          }
          .card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
          }
          .p-id {
            font-size: 0.75rem;
            color: #64748b;
            font-family: monospace;
          }
          .p-status {
            font-size: 0.72rem;
            padding: 2px 8px;
            border-radius: 20px;
            border: 1px solid;
          }
          .p-name {
            font-size: 0.95rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 4px;
          }
          .p-type {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-bottom: 12px;
          }
          .progress-bar-bg {
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 6px;
          }
          .progress-bar-fill {
            height: 100%;
            border-radius: 3px;
          }
          .progress-text {
            font-size: 0.75rem;
            color: #64748b;
            text-align: right;
          }
          .project-detail {
            padding: 20px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            flex-direction: column;
            gap: 20px;
          }
          .detail-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
          }
          .detail-tag {
            font-size: 0.78rem;
            color: #00f2fe;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
          }
          .detail-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin: 4px 0;
          }
          .detail-loc {
            font-size: 0.85rem;
            color: #94a3b8;
          }
          .manager-info {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            background: rgba(255, 255, 255, 0.05);
            padding: 8px 14px;
            border-radius: 10px;
            color: #cbd5e1;
          }
          .detail-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
          }
          .m-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 14px;
            text-align: center;
          }
          .m-icon {
            color: #00f2fe;
            margin-bottom: 6px;
          }
          .m-val {
            font-size: 1.2rem;
            font-weight: 700;
            color: #fff;
          }
          .m-lbl {
            font-size: 0.75rem;
            color: #94a3b8;
          }
          .stages-wrapper h4 {
            font-size: 0.95rem;
            margin-bottom: 14px;
            color: #e2e8f0;
          }
          .stages-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
          }
          .stage-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
          }
          .stage-title {
            font-size: 0.88rem;
            font-weight: 500;
          }
          .stage-date {
            font-size: 0.75rem;
            color: #64748b;
          }
          .text-success { color: #10b981; }
          .text-warning { color: #f59e0b; }
          .text-muted { color: #64748b; }
          .docs-table {
            margin-top: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
          }
          .doc-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            padding: 12px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            align-items: center;
            font-size: 0.88rem;
          }
          .doc-row.header {
            background: transparent;
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 600;
          }
          .badge-ok {
            color: #10b981;
            font-size: 0.8rem;
          }
          .btn-link {
            background: none;
            border: none;
            color: #00f2fe;
            cursor: pointer;
            text-decoration: underline;
          }
          .support-contacts {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 20px;
          }
          .s-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
          }
          .s-phone {
            font-size: 1.2rem;
            font-weight: 700;
            color: #00f2fe;
            text-decoration: none;
          }
        `}</style>
      </div>
    </AnimatePresence>
  )
}

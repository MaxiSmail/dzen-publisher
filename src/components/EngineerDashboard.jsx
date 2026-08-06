import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Briefcase, Clock, CheckCircle2, AlertCircle, Send, MessageSquare, 
  Play, FileText, Sparkles, User, AlertTriangle, Percent, Users
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { StorageService } from '../services/storage';

export default function EngineerDashboard({ tasks, currentUser, onTasksUpdated }) {
  const [selectedTask, setSelectedTask] = useState(null);
  const [reportText, setReportText] = useState('');
  const [targetStatus, setTargetStatus] = useState('review');
  const [progressVal, setProgressVal] = useState(50);

  // Filter tasks assigned to current logged in engineer (individual or joint)
  const myTasks = tasks.filter(t => {
    const ids = t.assignedToIds || [t.assignedToId];
    return ids.includes(currentUser.id);
  });

  const handleStartTask = (task) => {
    StorageService.updateTaskStatus(
      task.id, 
      'in_progress', 
      'Инженер принял задачу в работу.', 
      currentUser.name,
      task.progress || 0
    );
    onTasksUpdated();
  };

  const openReportModal = (task) => {
    setSelectedTask(task);
    setProgressVal(task.progress || 50);
    setTargetStatus('review');
    setReportText('');
  };

  const handleSubmitReport = (e) => {
    e.preventDefault();
    if (!selectedTask) return;

    StorageService.updateTaskStatus(
      selectedTask.id, 
      targetStatus, 
      reportText.trim() || `Обновлена процентовка выполнения: ${progressVal}%`, 
      currentUser.name,
      progressVal
    );

    if (targetStatus === 'review' || targetStatus === 'completed' || progressVal === 100) {
      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.6 }
      });
    }

    onTasksUpdated();
    setSelectedTask(null);
    setReportText('');
  };

  const getDeadlineDays = (endDateStr) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const end = new Date(endDateStr);
    end.setHours(0, 0, 0, 0);
    const diffTime = end - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  return (
    <div className="space-y-6">
      
      {/* Top Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-700/60 bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/30 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <img
            src={currentUser.avatar}
            alt={currentUser.name}
            className="w-12 h-12 rounded-2xl object-cover ring-2 ring-emerald-500/50 shadow-lg"
          />
          <div>
            <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
              Личный кабинет инженера
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Сотрудник: <strong className="text-emerald-400">{currentUser.name}</strong> • {currentUser.roleTitle}
            </p>
          </div>
        </div>

        <div className="glass-card px-4 py-2 rounded-2xl border border-emerald-500/30 text-xs">
          <span className="text-slate-400">Назначено задач: </span>
          <strong className="text-emerald-400 text-sm font-bold ml-1">{myTasks.length}</strong>
        </div>
      </div>

      {/* Task Cards List */}
      <div className="space-y-4">
        {myTasks.length === 0 ? (
          <div className="glass-panel p-12 text-center rounded-3xl border border-slate-800">
            <Briefcase className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <h3 className="text-sm font-semibold text-slate-300">У вас пока нет назначенных задач</h3>
            <p className="text-xs text-slate-500 mt-1">Руководство добавит индивидуальные или совместные задачи по мере появления объектов.</p>
          </div>
        ) : (
          myTasks.map(task => {
            const daysLeft = getDeadlineDays(task.endDate);
            const assigneeNames = task.assignedToNames || [task.assignedToName];

            return (
              <motion.div
                key={task.id}
                layout
                className="glass-panel p-6 rounded-2xl border border-slate-700/60 bg-slate-900/80 space-y-4 shadow-xl"
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  
                  {/* Title & Creator Info */}
                  <div className="space-y-1.5 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${
                        task.priority === 'urgent'
                          ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                          : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      }`}>
                        {task.priority === 'urgent' ? '🔥 Срочно' : 'Обычный'}
                      </span>

                      {assigneeNames.length > 1 && (
                        <span className="px-2 py-0.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded text-[10px] font-bold flex items-center gap-1">
                          <Users className="w-3 h-3" /> Совместная работа ({assigneeNames.join(', ')})
                        </span>
                      )}

                      {task.status === 'completed' && (
                        <span className="px-2.5 py-0.5 bg-emerald-500/20 text-emerald-400 rounded-lg text-[11px] font-semibold flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Выполнено (100%)
                        </span>
                      )}

                      {task.status === 'review' && (
                        <span className="px-2.5 py-0.5 bg-purple-500/20 text-purple-300 rounded-lg text-[11px] font-semibold flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5" /> На проверке руководства
                        </span>
                      )}

                      {task.status === 'in_progress' && (
                        <span className="px-2.5 py-0.5 bg-amber-500/20 text-amber-300 rounded-lg text-[11px] font-semibold flex items-center gap-1">
                          <Play className="w-3.5 h-3.5" /> В работе
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-slate-100">
                      {task.title}
                    </h3>
                    <p className="text-xs text-slate-300 bg-slate-950/40 p-3 rounded-xl border border-slate-800">
                      {task.description}
                    </p>
                  </div>

                  {/* Right Box: Action Buttons */}
                  <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                    <div className="text-xs text-slate-400 space-y-1">
                      <div>Поставил: <strong className="text-slate-200">{task.creatorName}</strong></div>
                      <div>Дедлайн: <strong className="text-amber-300">{task.endDate}</strong> ({daysLeft} дн.)</div>
                      <div>Процентовка: <strong className="text-emerald-400 text-sm">{task.progress}%</strong></div>
                    </div>

                    <div className="flex items-center space-x-2">
                      {task.status === 'pending' && (
                        <button
                          onClick={() => handleStartTask(task)}
                          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-indigo-600/30 flex items-center gap-1.5 transition-all"
                        >
                          <Play className="w-4 h-4" />
                          <span>Принять в работу</span>
                        </button>
                      )}

                      {task.status !== 'completed' && (
                        <button
                          onClick={() => openReportModal(task)}
                          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-emerald-600/20 flex items-center gap-1.5 transition-all"
                        >
                          <Percent className="w-4 h-4" />
                          <span>Обновить % & Отчет</span>
                        </button>
                      )}
                    </div>
                  </div>

                </div>

                {/* Progress bar visual */}
                <div className="space-y-1">
                  <div className="flex justify-between text-[11px] text-slate-400">
                    <span>Текущий прогресс выполнения:</span>
                    <span className="font-bold text-emerald-400">{task.progress}%</span>
                  </div>
                  <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-indigo-500 to-emerald-400 rounded-full transition-all duration-500"
                      style={{ width: `${task.progress}%` }}
                    />
                  </div>
                </div>

                {/* Submitted reports timeline */}
                {task.reports && task.reports.length > 0 && (
                  <div className="border-t border-slate-800 pt-3">
                    <div className="text-[11px] font-semibold text-slate-400 mb-2 flex items-center gap-1">
                      <MessageSquare className="w-3.5 h-3.5 text-indigo-400" />
                      История статусов и отчетов ({task.reports.length}):
                    </div>
                    <div className="space-y-2">
                      {task.reports.map((rep) => (
                        <div key={rep.id} className="p-3 bg-slate-950/60 rounded-xl border border-slate-800 text-xs">
                          <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="font-semibold text-emerald-400">{rep.author}</span>
                            <div className="flex items-center space-x-2">
                              {rep.progress !== undefined && (
                                <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold text-[10px]">
                                  Прогресс: {rep.progress}%
                                </span>
                              )}
                              <span className="text-[10px]">{rep.date}</span>
                            </div>
                          </div>
                          <p className="text-slate-200">{rep.text}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            );
          })
        )}
      </div>

      {/* Modal: Submit Engineer Progress & Report */}
      <AnimatePresence>
        {selectedTask && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl"
            >
              <div className="flex items-center justify-between p-5 border-b border-slate-800">
                <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                  <Percent className="w-5 h-5 text-emerald-400" />
                  Обновление процентовки и сдача отчета
                </h3>
                <button
                  onClick={() => setSelectedTask(null)}
                  className="p-1.5 text-slate-400 hover:text-white rounded-xl hover:bg-slate-800"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleSubmitReport} className="p-6 space-y-5 text-xs">
                <div>
                  <div className="text-slate-400 font-medium mb-1">Задача:</div>
                  <div className="font-bold text-slate-200 bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                    {selectedTask.title}
                  </div>
                </div>

                {/* PERCENTAGE PROGRESS SLIDER & PRESETS */}
                <div className="space-y-2 bg-slate-950/70 p-4 rounded-2xl border border-slate-800">
                  <div className="flex items-center justify-between">
                    <label className="text-slate-200 font-bold flex items-center gap-1.5">
                      <Percent className="w-4 h-4 text-emerald-400" />
                      Укажите % выполнения работы:
                    </label>
                    <span className="text-lg font-black text-emerald-400">{progressVal}%</span>
                  </div>

                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={progressVal}
                    onChange={(e) => setProgressVal(parseInt(e.target.value, 10))}
                    className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />

                  <div className="flex items-center justify-between gap-1 pt-1">
                    {[0, 25, 50, 75, 100].map(val => (
                      <button
                        key={val}
                        type="button"
                        onClick={() => setProgressVal(val)}
                        className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all ${
                          progressVal === val
                            ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/30'
                            : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        {val}%
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Комментарий / Ежедневный отчет</label>
                  <textarea
                    rows={3}
                    placeholder="Опишите выполненные работы, смонтированное оборудование или текущий этап..."
                    value={reportText}
                    onChange={(e) => setReportText(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Обновить статус задачи</label>
                  <select
                    value={targetStatus}
                    onChange={(e) => setTargetStatus(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="in_progress">В процессе выполнения (Промежуточный статус)</option>
                    <option value="review">На проверку руководству (Ждет приемки)</option>
                    <option value="completed">Полностью завершено (100%)</option>
                  </select>
                </div>

                <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setSelectedTask(null)}
                    className="px-4 py-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                  >
                    Отмена
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-xl shadow-lg shadow-emerald-600/30 flex items-center gap-1.5"
                  >
                    <Send className="w-4 h-4" />
                    <span>Сохранить и отправить</span>
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

    </div>
  );
}

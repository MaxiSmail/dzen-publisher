import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, Calendar, Clock, CheckCircle2, AlertTriangle, AlertCircle, 
  User, ChevronRight, ChevronDown, Filter, Trash2, Edit3, MessageSquare, 
  Check, Play, Award, Sparkles, Users
} from 'lucide-react';
import { StorageService } from '../services/storage';

export default function GanttPlanner({ tasks, users, currentUser, onTasksUpdated }) {
  // Exclude Admin from task assignees list
  const assignableUsers = users.filter(u => u.id !== 'user-admin' && u.role !== 'Admin');

  const [filterStatus, setFilterStatus] = useState('all');
  const [filterAssignee, setFilterAssignee] = useState('all');
  const [expandedTaskId, setExpandedTaskId] = useState(null);
  
  // Task Creation Form Modal State
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedAssigneeIds, setSelectedAssigneeIds] = useState([]);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(
    new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  );
  const [priority, setPriority] = useState('medium');

  // Compute days until deadline
  const getDeadlineDays = (endDateStr) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const end = new Date(endDateStr);
    end.setHours(0, 0, 0, 0);
    const diffTime = end - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const handleToggleAssignee = (userId) => {
    if (selectedAssigneeIds.includes(userId)) {
      setSelectedAssigneeIds(selectedAssigneeIds.filter(id => id !== userId));
    } else {
      setSelectedAssigneeIds([...selectedAssigneeIds, userId]);
    }
  };

  const handleCreateTask = (e) => {
    e.preventDefault();
    if (!title.trim() || selectedAssigneeIds.length === 0) {
      alert('Пожалуйста, введите название и выберите хотя бы одного исполнителя!');
      return;
    }

    const assignedUsers = users.filter(u => selectedAssigneeIds.includes(u.id));
    const assignedToNames = assignedUsers.map(u => u.name);

    StorageService.createTask({
      title: title.trim(),
      description: description.trim(),
      assignedToIds: selectedAssigneeIds,
      assignedToNames: assignedToNames,
      creatorId: currentUser.id,
      creatorName: `${currentUser.name} (${currentUser.roleTitle})`,
      startDate,
      endDate,
      priority,
    });

    onTasksUpdated();
    setShowCreateModal(false);
    setTitle('');
    setDescription('');
    setSelectedAssigneeIds([]);
  };

  const handleDeleteTask = (taskId) => {
    if (confirm('Удалить эту задачу?')) {
      StorageService.deleteTask(taskId);
      onTasksUpdated();
    }
  };

  const handleApproveCompletion = (taskId) => {
    StorageService.updateTaskStatus(
      taskId, 
      'completed', 
      'Задача принята руководителем. Работы завершены на 100%.', 
      currentUser.name,
      100
    );
    onTasksUpdated();
  };

  // Filter tasks
  const filteredTasks = tasks.filter(task => {
    if (filterStatus !== 'all' && task.status !== filterStatus) return false;
    if (filterAssignee !== 'all') {
      const ids = task.assignedToIds || [task.assignedToId];
      if (!ids.includes(filterAssignee)) return false;
    }
    return true;
  });

  // Calculate stats
  const totalTasks = tasks.length;
  const inProgressCount = tasks.filter(t => t.status === 'in_progress').length;
  const reviewCount = tasks.filter(t => t.status === 'review').length;
  const completedCount = tasks.filter(t => t.status === 'completed').length;

  return (
    <div className="space-y-6">
      
      {/* Top Banner & Stats Overview */}
      <div className="flex flex-wrap items-center justify-between gap-4 glass-panel p-6 rounded-3xl border border-slate-700/60 bg-gradient-to-r from-slate-900 via-slate-900/90 to-indigo-950/40">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Calendar className="w-6 h-6 text-indigo-400" />
            Интерактивный планер задач & График Гантта
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Кабинет руководства: {currentUser.name} ({currentUser.roleTitle})
          </p>
        </div>

        {/* Action Button */}
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white font-medium text-xs rounded-2xl shadow-lg shadow-indigo-600/30 flex items-center space-x-2 transition-all hover:scale-105"
        >
          <Plus className="w-4 h-4" />
          <span>Поставить задачу (в т.ч. совместную)</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card p-4 rounded-2xl border border-slate-700/50 flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold">
            {totalTasks}
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">Всего задач</div>
            <div className="text-lg font-bold text-slate-100">{totalTasks}</div>
          </div>
        </div>

        <div className="glass-card p-4 rounded-2xl border border-slate-700/50 flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold">
            {inProgressCount}
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">В работе</div>
            <div className="text-lg font-bold text-amber-400">{inProgressCount}</div>
          </div>
        </div>

        <div className="glass-card p-4 rounded-2xl border border-slate-700/50 flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold">
            {reviewCount}
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">На проверке</div>
            <div className="text-lg font-bold text-purple-400">{reviewCount}</div>
          </div>
        </div>

        <div className="glass-card p-4 rounded-2xl border border-slate-700/50 flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold">
            {completedCount}
          </div>
          <div>
            <div className="text-xs font-medium text-slate-400">Завершено</div>
            <div className="text-lg font-bold text-emerald-400">{completedCount}</div>
          </div>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="glass-card p-4 rounded-2xl border border-slate-700/60 flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-slate-400 flex items-center gap-1 font-semibold">
            <Filter className="w-3.5 h-3.5 text-indigo-400" /> Фильтры:
          </span>

          {/* Status buttons */}
          <div className="flex items-center space-x-1 bg-slate-900/60 p-1 rounded-xl border border-slate-700/50">
            {[
              { id: 'all', label: 'Все' },
              { id: 'pending', label: 'Ожидают' },
              { id: 'in_progress', label: 'В работе' },
              { id: 'review', label: 'На проверке' },
              { id: 'completed', label: 'Готово' },
            ].map(st => (
              <button
                key={st.id}
                onClick={() => setFilterStatus(st.id)}
                className={`px-3 py-1 rounded-lg transition-all ${
                  filterStatus === st.id
                    ? 'bg-indigo-600 text-white font-medium shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {st.label}
              </button>
            ))}
          </div>

          {/* Assignee select */}
          <select
            value={filterAssignee}
            onChange={(e) => setFilterAssignee(e.target.value)}
            className="px-3 py-1.5 bg-slate-900/80 border border-slate-700 rounded-xl text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="all">Все исполнители</option>
            {assignableUsers.map(u => (
              <option key={u.id} value={u.id}>{u.name} ({u.roleTitle})</option>
            ))}
          </select>
        </div>

        <div className="text-slate-500 text-[11px]">
          Отображено задач: {filteredTasks.length} из {tasks.length}
        </div>
      </div>

      {/* Task Gantt List */}
      <div className="space-y-4">
        {filteredTasks.length === 0 ? (
          <div className="glass-panel p-12 text-center rounded-3xl border border-slate-800">
            <Calendar className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <h3 className="text-sm font-semibold text-slate-300">Задач по выбранным фильтрам не найдено</h3>
            <p className="text-xs text-slate-500 mt-1">Попробуйте изменить параметры фильтрации или создайте новую задачу.</p>
          </div>
        ) : (
          filteredTasks.map(task => {
            const daysLeft = getDeadlineDays(task.endDate);
            const isExpanded = expandedTaskId === task.id;

            // Determine status badge colors
            let deadlineBadge = null;
            if (task.status === 'completed') {
              deadlineBadge = (
                <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-lg flex items-center gap-1 text-[11px] font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Выполнено
                </span>
              );
            } else if (daysLeft < 0) {
              deadlineBadge = (
                <span className="px-2.5 py-1 bg-red-500/20 text-red-400 border border-red-500/40 rounded-lg flex items-center gap-1 text-[11px] font-bold animate-pulse">
                  <AlertCircle className="w-3.5 h-3.5" /> Просрочено на {Math.abs(daysLeft)} дн.
                </span>
              );
            } else if (daysLeft === 0) {
              deadlineBadge = (
                <span className="px-2.5 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-lg flex items-center gap-1 text-[11px] font-bold">
                  <Clock className="w-3.5 h-3.5 text-amber-400" /> Дедлайн СЕГОДНЯ!
                </span>
              );
            } else if (daysLeft <= 2) {
              deadlineBadge = (
                <span className="px-2.5 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded-lg flex items-center gap-1 text-[11px] font-medium">
                  <Clock className="w-3.5 h-3.5" /> Поджимает ({daysLeft} дн.)
                </span>
              );
            } else {
              deadlineBadge = (
                <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 rounded-lg flex items-center gap-1 text-[11px]">
                  <Clock className="w-3.5 h-3.5 text-emerald-400" /> В сроках (осталось {daysLeft} дн.)
                </span>
              );
            }

            const assigneeIds = task.assignedToIds || [task.assignedToId];
            const assignedUsers = users.filter(u => assigneeIds.includes(u.id));

            return (
              <motion.div
                key={task.id}
                layout
                className="glass-panel rounded-2xl border border-slate-700/60 overflow-hidden shadow-xl"
              >
                {/* Task Header Row */}
                <div className="p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-slate-900/60">
                  
                  {/* Left Column: Title & Assignees */}
                  <div className="flex-1 space-y-2">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${
                        task.priority === 'urgent'
                          ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                          : task.priority === 'high'
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : 'bg-slate-700/50 text-slate-300'
                      }`}>
                        {task.priority === 'urgent' ? 'Срочно' : task.priority === 'high' ? 'Высокий' : 'Обычный'}
                      </span>

                      {assigneeIds.length > 1 && (
                        <span className="px-2 py-0.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded text-[10px] font-bold flex items-center gap-1">
                          <Users className="w-3 h-3" /> Совместная ({assigneeIds.length} чел.)
                        </span>
                      )}

                      {deadlineBadge}

                      {task.status === 'review' && (
                        <span className="px-2.5 py-1 bg-purple-500/20 text-purple-300 border border-purple-500/40 rounded-lg text-[11px] font-semibold flex items-center gap-1">
                          <MessageSquare className="w-3.5 h-3.5" /> На проверке руководства!
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-slate-100 hover:text-indigo-300 transition-colors">
                      {task.title}
                    </h3>
                    <p className="text-xs text-slate-400 line-clamp-2">
                      {task.description}
                    </p>
                  </div>

                  {/* Right Column: Assignees Avatars & Dates */}
                  <div className="flex flex-wrap items-center gap-4 border-t lg:border-t-0 pt-3 lg:pt-0 border-slate-800">
                    
                    {/* Assignees Badges */}
                    <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700/60">
                      <div className="flex -space-x-2">
                        {assignedUsers.map(u => (
                          <img
                            key={u.id}
                            src={u.avatar}
                            alt={u.name}
                            className="w-7 h-7 rounded-full object-cover ring-2 ring-indigo-500/50"
                            title={`${u.name} (${u.roleTitle})`}
                          />
                        ))}
                      </div>
                      <div className="text-left">
                        <div className="text-xs font-semibold text-slate-200 truncate max-w-[150px]">
                          {assignedUsers.map(u => u.name.split(' ')[0]).join(', ')}
                        </div>
                        <div className="text-[10px] text-slate-400">
                          {assignedUsers.length > 1 ? 'Исполнители (Совместно)' : 'Исполнитель'}
                        </div>
                      </div>
                    </div>

                    {/* Timeline dates */}
                    <div className="text-xs text-slate-400 space-y-0.5">
                      <div>Сроки: <span className="text-slate-200 font-medium">{task.startDate}</span> — <span className="text-amber-300 font-medium">{task.endDate}</span></div>
                      <div className="text-[10px] text-slate-500">Поставил: {task.creatorName}</div>
                    </div>

                    {/* Controls */}
                    <div className="flex items-center space-x-2">
                      {task.status === 'review' && (
                        <button
                          onClick={() => handleApproveCompletion(task.id)}
                          className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-emerald-600/20 flex items-center gap-1 transition-all"
                          title="Принять работу и закрыть задачу"
                        >
                          <Check className="w-4 h-4" />
                          <span>Принять отчет</span>
                        </button>
                      )}

                      <button
                        onClick={() => setExpandedTaskId(isExpanded ? null : task.id)}
                        className="p-2 text-slate-400 hover:text-white rounded-xl bg-slate-800 hover:bg-slate-700 transition-colors"
                      >
                        <ChevronDown className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                      </button>

                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="p-2 text-slate-400 hover:text-red-400 rounded-xl hover:bg-red-500/10 transition-colors"
                        title="Удалить задачу"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>

                {/* Visual Progress Timeline Bar (Gantt element with percent) */}
                <div className="px-5 py-3 bg-slate-950/60 border-t border-slate-800/80">
                  <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
                    <span className="font-semibold text-slate-200">
                      Процентовка выполнения инженером: <strong className="text-emerald-400 font-extrabold text-sm">{task.progress}%</strong>
                    </span>
                    <span className="text-[11px] text-slate-500">
                      Отсчет дедлайна: {daysLeft < 0 ? `Просрочено на ${Math.abs(daysLeft)} дн.` : `${daysLeft} дн.`}
                    </span>
                  </div>
                  <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${task.progress}%` }}
                      transition={{ duration: 0.8 }}
                      className={`h-full rounded-full ${
                        task.status === 'completed'
                          ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
                          : daysLeft < 0
                          ? 'bg-gradient-to-r from-red-600 to-rose-400'
                          : 'bg-gradient-to-r from-indigo-500 via-blue-500 to-emerald-400'
                      }`}
                    />
                  </div>
                </div>

                {/* Expanded Details & Reports */}
                {isExpanded && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="p-5 bg-slate-900/90 border-t border-slate-800 space-y-4"
                  >
                    <div>
                      <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                        Полное описание задачи:
                      </h4>
                      <p className="text-xs text-slate-300 bg-slate-950/50 p-3 rounded-xl border border-slate-800 whitespace-pre-wrap">
                        {task.description}
                      </p>
                    </div>

                    {/* History of Reports from Engineers */}
                    <div>
                      <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <MessageSquare className="w-3.5 h-3.5 text-indigo-400" />
                        История статусов и отчетов инженеров ({task.reports?.length || 0}):
                      </h4>

                      {(!task.reports || task.reports.length === 0) ? (
                        <p className="text-xs text-slate-500 italic bg-slate-950/30 p-3 rounded-xl border border-slate-800">
                          Инженеры пока не отправляли отчетов по этой задаче.
                        </p>
                      ) : (
                        <div className="space-y-2">
                          {task.reports.map((rep) => (
                            <div key={rep.id} className="p-3 bg-slate-950/70 rounded-xl border border-slate-800 text-xs">
                              <div className="flex items-center justify-between text-slate-400 mb-1">
                                <span className="font-semibold text-indigo-300">{rep.author}</span>
                                <div className="flex items-center space-x-2">
                                  {rep.progress !== undefined && (
                                    <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold text-[10px]">
                                      Прогресс: {rep.progress}%
                                    </span>
                                  )}
                                  <span className="text-[11px]">{rep.date}</span>
                                </div>
                              </div>
                              <p className="text-slate-200">{rep.text}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </motion.div>
            );
          })
        )}
      </div>

      {/* Modal: Create Task (With Joint Multi-Assignees) */}
      <AnimatePresence>
        {showCreateModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-xl overflow-hidden shadow-2xl"
            >
              <div className="flex items-center justify-between p-5 border-b border-slate-800">
                <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                  <Plus className="w-5 h-5 text-indigo-400" />
                  Постановка новой (в т.ч. совместной) задачи
                </h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="p-1.5 text-slate-400 hover:text-white rounded-xl hover:bg-slate-800"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleCreateTask} className="p-6 space-y-4 text-xs">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">Название задачи *</label>
                  <input
                    type="text"
                    placeholder="Например: Пусконаладка системы диспетчеризации объекта"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-indigo-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">Описание и требования</label>
                  <textarea
                    rows={3}
                    placeholder="Укажите детали, необходимый инструмент или распределение обязанностей..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                {/* MULTI-SELECT ASSIGNEES FOR JOINT TASKS */}
                <div>
                  <label className="block text-slate-300 font-medium mb-1 flex items-center gap-1.5">
                    <Users className="w-4 h-4 text-indigo-400" />
                    Выберите исполнителей задачи (можно выбрать нескольких для совместной работы) *
                  </label>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 bg-slate-950/80 p-3 rounded-xl border border-slate-800 max-h-40 overflow-y-auto">
                    {assignableUsers.map(u => {
                      const isChecked = selectedAssigneeIds.includes(u.id);
                      return (
                        <label
                          key={u.id}
                          onClick={() => handleToggleAssignee(u.id)}
                          className={`flex items-center space-x-2.5 p-2 rounded-lg cursor-pointer border transition-all ${
                            isChecked
                              ? 'bg-indigo-600/20 border-indigo-500 text-slate-100'
                              : 'bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-800'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={() => {}} // handled by div click
                            className="rounded border-slate-700 text-indigo-600 focus:ring-0"
                          />
                          <img src={u.avatar} alt={u.name} className="w-6 h-6 rounded-full object-cover" />
                          <div className="truncate text-xs font-semibold">{u.name}</div>
                        </label>
                      );
                    })}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-slate-300 font-medium mb-1">Приоритет</label>
                    <select
                      value={priority}
                      onChange={(e) => setPriority(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-indigo-500"
                    >
                      <option value="medium">Обычный</option>
                      <option value="high">Высокий</option>
                      <option value="urgent">🔥 Срочный (Критично)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-300 font-medium mb-1">Дата начала</label>
                    <input
                      type="date"
                      value={startDate}
                      onChange={(e) => setStartDate(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-indigo-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-slate-300 font-medium mb-1">Дедлайн (Срок)</label>
                    <input
                      type="date"
                      value={endDate}
                      onChange={(e) => setEndDate(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-indigo-500"
                      required
                    />
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                  >
                    Отмена
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl shadow-lg shadow-indigo-600/30"
                  >
                    Создать задачу
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

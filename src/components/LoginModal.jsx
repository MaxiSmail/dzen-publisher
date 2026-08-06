import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  X, ShieldCheck, Check, User, Key, Camera, LogIn, AlertCircle, Lock
} from 'lucide-react';
import { StorageService } from '../services/storage';
import bmkLogo from '../assets/bmk_logo.png';

export default function LoginModal({ 
  isOpen, 
  onClose, 
  users, 
  currentUser, 
  onLoginSuccess,
  onAvatarUpdated 
}) {
  const [activeTab, setActiveTab] = useState('login'); // 'login' | 'avatar'
  const [selectedUsername, setSelectedUsername] = useState(users[0]?.username || '');
  const [pinInput, setPinInput] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    if (!selectedUsername || !pinInput) {
      setErrorMsg('Пожалуйста, введите пароль (ПИН-код)');
      return;
    }

    const res = StorageService.authenticateUser(selectedUsername, pinInput);
    if (res.success) {
      onLoginSuccess(res.user);
      setPinInput('');
      setErrorMsg('');
      onClose();
    } else {
      setErrorMsg('Неверный логин или пароль!');
    }
  };

  const handleAvatarUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 2 * 1024 * 1024) {
      alert('Размер файла изображения не должен превышать 2 МБ!');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target.result;
      StorageService.updateUserAvatar(currentUser.id, dataUrl);
      onAvatarUpdated();
      alert('Аватарка успешно обновлена!');
    };
    reader.readAsDataURL(file);
  };

  const categories = ['Администрация', 'Руководство', 'Инженерный состав', 'Отдел ПТО', 'Прорабы'];
  const currentSelectedUserObj = users.find(u => u.username === selectedUsername) || users[0];

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="glass-panel bg-slate-900 border border-slate-700/80 rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl"
        >
          {/* Header with BMK Logo */}
          <div className="flex items-center justify-between p-6 border-b border-slate-800 bg-slate-900/50">
            <div className="flex items-center space-x-3">
              <div className="bg-white/95 p-1 rounded-xl border border-slate-700 shadow-md">
                <img src={bmkLogo} alt="ООО БМК" className="h-8 object-contain" />
              </div>
              <div>
                <h2 className="text-lg font-black text-slate-100 flex items-center gap-2">
                  Вход в систему — ООО «БМК»
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Авторизация по логину и персональному паролю
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Tab Switcher */}
          <div className="flex items-center border-b border-slate-800 bg-slate-950/60 px-6 py-2 gap-2 text-xs">
            <button
              onClick={() => setActiveTab('login')}
              className={`px-4 py-1.5 rounded-xl font-medium transition-all ${
                activeTab === 'login'
                  ? 'bg-indigo-600 text-white font-bold shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              🔑 Форма авторизации
            </button>

            <button
              onClick={() => setActiveTab('avatar')}
              className={`px-4 py-1.5 rounded-xl font-medium transition-all ${
                activeTab === 'avatar'
                  ? 'bg-indigo-600 text-white font-bold shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              📷 Смена аватарки
            </button>
          </div>

          <div className="p-6 max-h-[70vh] overflow-y-auto">
            
            {/* TAB 1: AUTHENTICATION FORM */}
            {activeTab === 'login' && (
              <form onSubmit={handleLoginSubmit} className="space-y-5">
                
                {/* Employee Selector */}
                <div>
                  <label className="block text-slate-300 text-xs font-semibold mb-1.5">
                    Выберите профиль для входа:
                  </label>
                  <select
                    value={selectedUsername}
                    onChange={(e) => {
                      setSelectedUsername(e.target.value);
                      setErrorMsg('');
                    }}
                    className="w-full px-4 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-100 font-bold focus:outline-none focus:border-indigo-500"
                  >
                    {categories.map(cat => {
                      const catUsers = users.filter(u => (u.category || 'Инженерный состав') === cat);
                      if (catUsers.length === 0) return null;
                      return (
                        <optgroup key={cat} label={cat}>
                          {catUsers.map(u => (
                            <option key={u.id} value={u.username}>
                              {u.name} ({u.roleTitle})
                            </option>
                          ))}
                        </optgroup>
                      );
                    })}
                  </select>
                </div>

                {/* Profile Card Preview */}
                <div className="p-4 bg-slate-950/60 rounded-2xl border border-slate-800 flex items-center space-x-4">
                  <img
                    src={currentSelectedUserObj?.avatar}
                    alt={currentSelectedUserObj?.name}
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(currentSelectedUserObj?.name || 'User')}&background=6366f1&color=fff`;
                    }}
                    className="w-12 h-12 rounded-xl object-cover ring-2 ring-indigo-500/50 flex-shrink-0"
                  />
                  <div>
                    <div className="text-sm font-bold text-slate-100">{currentSelectedUserObj?.name}</div>
                    <div className="text-xs text-indigo-400 font-medium">{currentSelectedUserObj?.roleTitle}</div>
                    <div className="text-[11px] text-slate-400">Логин: <strong className="text-slate-200">{currentSelectedUserObj?.username}</strong></div>
                  </div>
                </div>

                {/* Password / PIN Input */}
                <div>
                  <label className="block text-slate-300 text-xs font-semibold mb-1.5">
                    Введите ваш пароль / ПИН-код:
                  </label>
                  <input
                    type="password"
                    placeholder="Введите ваш пароль"
                    value={pinInput}
                    onChange={(e) => setPinInput(e.target.value)}
                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-center text-lg font-extrabold tracking-widest text-emerald-400 focus:outline-none focus:border-indigo-500"
                    required
                  />
                </div>

                {errorMsg && (
                  <div className="p-3 bg-red-500/20 text-red-400 border border-red-500/30 rounded-xl text-xs flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    <span>{errorMsg}</span>
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-600/30 flex items-center justify-center space-x-2 transition-all hover:scale-[1.01]"
                >
                  <LogIn className="w-4 h-4" />
                  <span>Войти в систему</span>
                </button>
              </form>
            )}

            {/* TAB 2: AVATAR UPLOAD */}
            {activeTab === 'avatar' && (
              <div className="space-y-5 text-center">
                <div className="mx-auto w-24 h-24 rounded-2xl relative overflow-hidden ring-4 ring-indigo-500/40 shadow-xl">
                  <img
                    src={currentUser.avatar}
                    alt={currentUser.name}
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(currentUser.name)}&background=6366f1&color=fff`;
                    }}
                    className="w-full h-full object-cover"
                  />
                </div>

                <div>
                  <h3 className="text-sm font-bold text-slate-100">{currentUser.name}</h3>
                  <p className="text-xs text-indigo-400">{currentUser.roleTitle}</p>
                </div>

                <div className="p-6 glass-card rounded-2xl border border-slate-800 space-y-3">
                  <label className="cursor-pointer inline-flex items-center space-x-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-xl shadow-lg shadow-indigo-600/30 transition-all">
                    <Camera className="w-4 h-4" />
                    <span>Выбрать фото / аватарку с компьютера</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleAvatarUpload}
                      className="hidden"
                    />
                  </label>
                  <p className="text-[11px] text-slate-500">
                    Поддерживаются файлы JPG, PNG, WEBP (макс. 2 МБ).
                  </p>
                </div>
              </div>
            )}

          </div>

          <div className="p-4 bg-slate-950/60 border-t border-slate-800 text-center text-[11px] text-slate-500">
            ООО «БМК» • Авторизация защищена персональным паролем
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}

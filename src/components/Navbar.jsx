import React from 'react';
import { motion } from 'framer-motion';
import { 
  Users, Calendar, FileSpreadsheet, Sparkles,
  Sun, Moon, Palette, Camera, LogOut, ShieldCheck, Eye
} from 'lucide-react';
import bmkLogo from '../assets/bmk_logo.png';

export default function Navbar({ 
  currentUser, 
  authenticatedUser,
  users = [],
  onSelectUser,
  onOpenAvatarModal,
  onLogout,
  activeTab, 
  setActiveTab,
  currentTheme,
  onThemeChange
}) {

  const handleSelectChange = (e) => {
    const selectedId = e.target.value;
    const targetUser = users.find(u => u.id === selectedId);
    if (targetUser) {
      onSelectUser(targetUser);
    }
  };

  const categories = ['Администрация', 'Руководство', 'Инженерный состав', 'Отдел ПТО', 'Прорабы'];
  const isAdmin = authenticatedUser?.role === 'Admin' || currentUser?.role === 'Admin';
  const isViceDirectorOrAdmin = currentUser?.role === 'ViceDirector' || currentUser?.role === 'Admin' || authenticatedUser?.role === 'Admin';

  return (
    <header className="glass-panel sticky top-0 z-30 border-b border-slate-700/50 bg-slate-900/90 backdrop-blur-md px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        
        {/* Brand Logo & App Title */}
        <div className="flex items-center space-x-3">
          <div className="bg-white/95 p-1.5 rounded-xl border border-slate-700 shadow-md shadow-indigo-500/10 flex items-center justify-center">
            <img
              src={bmkLogo}
              alt="ООО БМК Logo"
              className="h-8 object-contain"
            />
          </div>
          <div>
            <h1 className="text-[17px] font-black text-slate-100 leading-tight">
              Система управления.
            </h1>
            <p className="text-xs text-indigo-400 font-extrabold tracking-wide">
              ООО «БМК»
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        {isViceDirectorOrAdmin && (
          <div className="flex items-center bg-slate-800/80 p-1 rounded-xl border border-slate-700/60 shadow-inner">
            <button
              onClick={() => setActiveTab('planning')}
              className={`flex items-center space-x-2 px-4 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'planning'
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
              }`}
            >
              <Calendar className="w-3.5 h-3.5" />
              <span>Планирование задач</span>
            </button>

            <button
              onClick={() => setActiveTab('travel')}
              className={`flex items-center space-x-2 px-4 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === 'travel'
                  ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
              }`}
            >
              <FileSpreadsheet className="w-3.5 h-3.5" />
              <span>Командировочные расходы</span>
            </button>
          </div>
        )}

        {/* Right Section: Theme Selector, Profile Display & Logout */}
        <div className="flex items-center space-x-3">
          
          {/* THEME SWITCHER BUTTONS */}
          <div className="flex items-center space-x-1 bg-slate-800/90 p-1 rounded-xl border border-slate-700">
            <button
              onClick={() => onThemeChange('light')}
              className={`p-1.5 rounded-lg text-xs transition-all ${
                currentTheme === 'light'
                  ? 'bg-amber-500 text-slate-950 font-bold shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Светлая тема"
            >
              <Sun className="w-3.5 h-3.5" />
            </button>

            <button
              onClick={() => onThemeChange('dark')}
              className={`p-1.5 rounded-lg text-xs transition-all ${
                currentTheme === 'dark'
                  ? 'bg-indigo-600 text-white font-bold shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Тёмная тема (Glass Night)"
            >
              <Moon className="w-3.5 h-3.5" />
            </button>

            <button
              onClick={() => onThemeChange('corporate')}
              className={`p-1.5 rounded-lg text-xs transition-all ${
                currentTheme === 'corporate'
                  ? 'bg-blue-600 text-white font-bold shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Корпоративная тема"
            >
              <Palette className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* PROFILE DISPLAY & ADMIN SWITCHER */}
          <div className={`flex items-center space-x-3 border px-3 py-1.5 rounded-2xl shadow-inner ${
            isAdmin ? 'bg-amber-950/40 border-amber-500/60 ring-1 ring-amber-500/30' : 'bg-slate-800/90 border-slate-700'
          }`}>
            
            {/* User Avatar */}
            <div 
              onClick={onOpenAvatarModal} 
              className="relative cursor-pointer group"
              title="Нажмите для смены фотографии / аватарки"
            >
              <img
                src={currentUser.avatar}
                alt={currentUser.name}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(currentUser.name)}&background=6366f1&color=fff`;
                }}
                className="w-8 h-8 rounded-xl object-cover ring-2 ring-indigo-500/40"
              />
              <span className="absolute -bottom-1 -right-1 bg-slate-900 p-0.5 rounded-full border border-slate-700">
                <Camera className="w-2.5 h-2.5 text-indigo-300" />
              </span>
            </div>

            {/* ADMIN MODE: Show dropdown to switch view to any employee */}
            {isAdmin ? (
              <div className="flex flex-col text-left">
                <span className="text-[10px] text-amber-400 font-extrabold uppercase tracking-wider flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3 text-amber-400" />
                  Админ просмотр:
                </span>
                <select
                  value={currentUser.id}
                  onChange={handleSelectChange}
                  className="bg-transparent text-xs font-black text-amber-200 focus:outline-none cursor-pointer pr-1"
                >
                  {categories.map(cat => {
                    const catUsers = users.filter(u => (u.category || 'Инженерный состав') === cat);
                    if (catUsers.length === 0) return null;
                    return (
                      <optgroup key={cat} label={cat}>
                        {catUsers.map(u => (
                          <option key={u.id} value={u.id} className="bg-slate-900 text-slate-100 font-medium">
                            {u.name} ({u.roleTitle})
                          </option>
                        ))}
                      </optgroup>
                    );
                  })}
                </select>
              </div>
            ) : (
              /* REGULAR EMPLOYEE: Profile locked to single user */
              <div className="flex flex-col text-left pr-1">
                <span className="text-xs font-bold text-slate-100 leading-tight">
                  {currentUser.name}
                </span>
                <span className="text-[10px] text-indigo-400 font-medium">
                  {currentUser.roleTitle}
                </span>
              </div>
            )}

          </div>

          {/* LOGOUT BUTTON */}
          <button
            onClick={onLogout}
            className="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 rounded-xl transition-all flex items-center gap-1.5 text-xs font-medium"
            title="Выйти из системы"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Выйти</span>
          </button>

        </div>

      </div>
    </header>
  );
}

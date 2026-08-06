import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  FileSpreadsheet, Calendar, DollarSign, Download, Printer, Check, 
  ChevronLeft, ChevronRight, UserCheck, Briefcase, Zap, RefreshCw, Maximize2
} from 'lucide-react';
import * as XLSX from 'xlsx';
import { StorageService, getCurrentMonthYearStr } from '../services/storage';

export default function TravelAllowanceCalculator({ users, currentUser }) {
  // Exclude Admin from travel expenses calculation table
  const staffUsers = users.filter(u => u.id !== 'user-admin' && u.role !== 'Admin');

  // State for Month Selection
  const [selectedMonthYear, setSelectedMonthYear] = useState(getCurrentMonthYearStr());
  const [travelData, setTravelData] = useState(StorageService.getTravelData());

  const [yearStr, monthStr] = selectedMonthYear.split('-');
  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10); // 1-indexed

  // Month names in Russian
  const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  const daysInMonth = new Date(year, month, 0).getDate();

  const getDayOfWeekName = (dayNum) => {
    const d = new Date(year, month - 1, dayNum);
    const dayNames = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
    return dayNames[d.getDay()];
  };

  const isWeekend = (dayNum) => {
    const d = new Date(year, month - 1, dayNum);
    const day = d.getDay();
    return day === 0 || day === 6; // Sunday or Saturday
  };

  const handleToggleDay = (userId, dayNum) => {
    const updatedData = StorageService.toggleTravelDay(selectedMonthYear, userId, dayNum);
    setTravelData({ ...updatedData });
  };

  // Preset: Toggle Mon, Wed, Fri for an employee
  const handlePresetMonWedFri = (userId) => {
    const targetDays = [];
    for (let day = 1; day <= daysInMonth; day++) {
      const d = new Date(year, month - 1, day);
      const dayOfWeek = d.getDay(); // 1 = Mon, 3 = Wed, 5 = Fri
      if (dayOfWeek === 1 || dayOfWeek === 3 || dayOfWeek === 5) {
        targetDays.push(day);
      }
    }

    const newTravelData = StorageService.getTravelData();
    if (!newTravelData[selectedMonthYear]) newTravelData[selectedMonthYear] = {};
    newTravelData[selectedMonthYear][userId] = targetDays;

    StorageService.saveTravelData(newTravelData);
    setTravelData({ ...newTravelData });
  };

  const handleClearEmployee = (userId) => {
    const newTravelData = StorageService.getTravelData();
    if (newTravelData[selectedMonthYear]?.[userId]) {
      newTravelData[selectedMonthYear][userId] = [];
      StorageService.saveTravelData(newTravelData);
      setTravelData({ ...newTravelData });
    }
  };

  // Change Month
  const handlePrevMonth = () => {
    let newM = month - 1;
    let newY = year;
    if (newM < 1) {
      newM = 12;
      newY -= 1;
    }
    const newStr = `${newY}-${String(newM).padStart(2, '0')}`;
    setSelectedMonthYear(newStr);
  };

  const handleNextMonth = () => {
    let newM = month + 1;
    let newY = year;
    if (newM > 12) {
      newM = 1;
      newY += 1;
    }
    const newStr = `${newY}-${String(newM).padStart(2, '0')}`;
    setSelectedMonthYear(newStr);
  };

  // Calculate totals
  const currentMonthTravel = travelData[selectedMonthYear] || {};
  let totalCompanyDays = 0;
  staffUsers.forEach(u => {
    const days = currentMonthTravel[u.id] || [];
    totalCompanyDays += days.length;
  });
  const totalCompanyBudget = totalCompanyDays * 1000;

  // Export to Excel
  const handleExportExcel = () => {
    const rows = [];
    const headerRow = ['№', 'ФИО Сотрудника', 'Должность', 'Дней командировок', 'Ставка (руб/день)', 'Итого начислено (руб)'];
    rows.push(headerRow);

    staffUsers.forEach((u, index) => {
      const days = currentMonthTravel[u.id] || [];
      const count = days.length;
      const sum = count * 1000;
      rows.push([index + 1, u.name, u.roleTitle, count, 1000, sum]);
    });

    rows.push([]);
    rows.push(['Итого по организации', '', '', totalCompanyDays, '', totalCompanyBudget]);

    const worksheet = XLSX.utils.aoa_to_sheet(rows);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, `Командировки_${selectedMonthYear}`);
    
    XLSX.writeFile(workbook, `Vedomost_Komandirovochnye_${selectedMonthYear}.xlsx`);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 w-full">
      
      {/* Header Banner & Controls */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-700/60 bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/30 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <FileSpreadsheet className="w-6 h-6 text-emerald-400" />
            Полноэкранный табель командировочных расходов
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Кабинет Зам. директора: {currentUser.name} • Авторасчет <strong>1 000 ₽ / день</strong>
          </p>
        </div>

        {/* Month Navigator */}
        <div className="flex items-center space-x-3 bg-slate-800/90 p-1.5 rounded-2xl border border-slate-700">
          <button
            onClick={handlePrevMonth}
            className="p-1.5 text-slate-300 hover:text-white rounded-xl hover:bg-slate-700 transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <div className="px-3 text-center min-w-[140px]">
            <div className="text-sm font-bold text-emerald-400">
              {monthNames[month - 1]} {year}
            </div>
            <div className="text-[10px] text-slate-400">Табель командировок</div>
          </div>

          <button
            onClick={handleNextMonth}
            className="p-1.5 text-slate-300 hover:text-white rounded-xl hover:bg-slate-700 transition-colors"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        {/* Export / Print Actions */}
        <div className="flex items-center space-x-3 no-print">
          <button
            onClick={handleExportExcel}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-emerald-600/20 flex items-center space-x-2 transition-all hover:scale-105"
          >
            <Download className="w-4 h-4" />
            <span>Экспорт в Excel</span>
          </button>

          <button
            onClick={handlePrint}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-medium rounded-xl border border-slate-700 flex items-center space-x-2 transition-all"
          >
            <Printer className="w-4 h-4" />
            <span>Печать ведомости</span>
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-4 rounded-2xl border border-slate-700/60 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-medium">Штат сотрудников</div>
            <div className="text-xl font-bold text-slate-100 mt-1">{staffUsers.length} чел.</div>
          </div>
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
            <UserCheck className="w-5 h-5" />
          </div>
        </div>

        <div className="glass-card p-4 rounded-2xl border border-slate-700/60 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-medium">Командировочных дней за месяц</div>
            <div className="text-xl font-bold text-blue-400 mt-1">{totalCompanyDays} дн.</div>
          </div>
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <Briefcase className="w-5 h-5" />
          </div>
        </div>

        <div className="glass-card p-4 rounded-2xl border border-emerald-500/30 bg-emerald-950/20 flex items-center justify-between">
          <div>
            <div className="text-xs text-emerald-400 font-medium">Общая сумма выплат</div>
            <div className="text-2xl font-black text-emerald-300 mt-0.5">
              {totalCompanyBudget.toLocaleString('ru-RU')} ₽
            </div>
          </div>
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <DollarSign className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Full Width Table without Overflow Scrollbar */}
      <div className="glass-panel rounded-3xl border border-slate-700/60 overflow-hidden shadow-2xl w-full">
        <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2">
          <div className="text-xs text-slate-300 font-semibold flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            Полноэкранная табель-сетка за {monthNames[month - 1]} {year} (все 31 день помещаются целиком)
          </div>
          <div className="text-[11px] text-slate-400">
            Кликните на число для добавления или снятия дня командировки
          </div>
        </div>

        <div className="w-full overflow-x-auto lg:overflow-x-visible">
          <table className="w-full text-left border-collapse table-fixed text-xs">
            <thead>
              <tr className="bg-slate-950/90 text-slate-300 border-b border-slate-800">
                {/* Employee info column */}
                <th className="p-2 w-48 text-left font-semibold border-r border-slate-800">
                  Сотрудник
                </th>
                
                {/* Days Columns Header (Fit to full width) */}
                {Array.from({ length: daysInMonth }, (_, i) => i + 1).map(dayNum => {
                  const dayName = getDayOfWeekName(dayNum);
                  const weekend = isWeekend(dayNum);
                  return (
                    <th
                      key={dayNum}
                      className={`p-1 text-center border-r border-slate-800/60 ${
                        weekend ? 'bg-slate-900/90 text-rose-400' : 'text-slate-300'
                      }`}
                    >
                      <div className="text-[9px] opacity-75 font-normal">{dayName}</div>
                      <div className="font-bold text-[11px]">{dayNum}</div>
                    </th>
                  );
                })}

                <th className="p-2 w-16 text-center font-semibold border-l border-slate-800">Дней</th>
                <th className="p-2 w-24 text-right font-semibold">Итого (₽)</th>
                <th className="p-1 w-16 text-center no-print font-normal text-[10px]">Пн,Ср,Пт</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-800/60">
              {staffUsers.map(user => {
                const userDays = currentMonthTravel[user.id] || [];
                const dayCount = userDays.length;
                const totalSum = dayCount * 1000;

                return (
                  <tr key={user.id} className="hover:bg-slate-800/30 transition-colors">
                    
                    {/* Employee Profile Cell */}
                    <td className="p-2 border-r border-slate-800 bg-slate-900/40 truncate">
                      <div className="flex items-center space-x-2">
                        <img
                          src={user.avatar}
                          alt={user.name}
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=6366f1&color=fff`;
                          }}
                          className="w-7 h-7 rounded-full object-cover ring-1 ring-slate-700 flex-shrink-0"
                        />
                        <div className="min-w-0 truncate">
                          <div className="font-bold text-slate-100 truncate text-[11px]">{user.name}</div>
                          <div className="text-[9px] text-slate-400 truncate">{user.roleTitle}</div>
                        </div>
                      </div>
                    </td>

                    {/* Day Cells Grid (Fitting screen width) */}
                    {Array.from({ length: daysInMonth }, (_, i) => i + 1).map(dayNum => {
                      const isSelected = userDays.includes(dayNum);
                      const weekend = isWeekend(dayNum);

                      return (
                        <td
                          key={dayNum}
                          onClick={() => handleToggleDay(user.id, dayNum)}
                          className={`p-0.5 text-center cursor-pointer select-none border-r border-slate-800/40 transition-all ${
                            isSelected
                              ? 'bg-emerald-500/30 text-emerald-300 font-bold hover:bg-emerald-500/50'
                              : weekend
                              ? 'bg-slate-950/40 text-slate-600 hover:bg-slate-800/60'
                              : 'hover:bg-slate-800/60 text-slate-500'
                          }`}
                          title={`Сотрудник: ${user.name}, День: ${dayNum} (${getDayOfWeekName(dayNum)})`}
                        >
                          {isSelected ? (
                            <motion.div
                              initial={{ scale: 0.5 }}
                              animate={{ scale: 1 }}
                              className="w-5 h-5 mx-auto rounded-md bg-emerald-500 text-slate-950 flex items-center justify-center font-extrabold text-[9px] shadow-sm shadow-emerald-500/50"
                            >
                              ✓
                            </motion.div>
                          ) : (
                            <span className="text-[9px] opacity-30">•</span>
                          )}
                        </td>
                      );
                    })}

                    {/* Total Days */}
                    <td className="p-2 text-center font-bold text-blue-400 bg-slate-900/60 border-l border-slate-800 text-[11px]">
                      {dayCount}
                    </td>

                    {/* Total Amount */}
                    <td className="p-2 text-right font-extrabold text-emerald-400 bg-slate-900/60 text-[11px]">
                      {totalSum.toLocaleString('ru-RU')} ₽
                    </td>

                    {/* Quick Presets */}
                    <td className="p-1 text-center no-print">
                      <button
                        onClick={() => handlePresetMonWedFri(user.id)}
                        className="px-1.5 py-0.5 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 rounded text-[9px] font-medium border border-indigo-500/30 transition-all"
                        title="Заполнить Пн, Ср, Пт"
                      >
                        +Пн,Ср,Пт
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>

            {/* Total Footer Row */}
            <tfoot>
              <tr className="bg-slate-950 text-xs font-bold border-t border-slate-700">
                <td className="p-2 text-slate-200 border-r border-slate-800">
                  ИТОГО ВЕДОМОСТЬ:
                </td>
                <td colSpan={daysInMonth} className="p-2 text-slate-400 text-right text-[11px]">
                  Всего дней командировок за месяц:
                </td>
                <td className="p-2 text-center text-blue-400 text-xs border-l border-slate-800">
                  {totalCompanyDays} дн.
                </td>
                <td className="p-2 text-right text-emerald-300 text-sm font-black">
                  {totalCompanyBudget.toLocaleString('ru-RU')} ₽
                </td>
                <td className="no-print"></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

    </div>
  );
}

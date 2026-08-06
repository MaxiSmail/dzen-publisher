import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LoginModal from './components/LoginModal';
import GanttPlanner from './components/GanttPlanner';
import TravelAllowanceCalculator from './components/TravelAllowanceCalculator';
import EngineerDashboard from './components/EngineerDashboard';
import { StorageService } from './services/storage';

export default function App() {
  const [currentUser, setCurrentUser] = useState(StorageService.getCurrentUser());
  const [authenticatedUser, setAuthenticatedUser] = useState(StorageService.getAuthUser() || currentUser);
  const [users, setUsers] = useState(StorageService.getUsers());
  const [tasks, setTasks] = useState(StorageService.getTasks());
  const [activeTab, setActiveTab] = useState('planning'); // 'planning' | 'travel'
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(!StorageService.getIsAuthenticated());
  const [currentTheme, setCurrentTheme] = useState(StorageService.getTheme());

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', currentTheme);
  }, [currentTheme]);

  const handleThemeChange = (newTheme) => {
    StorageService.setTheme(newTheme);
    setCurrentTheme(newTheme);
  };

  const handleDataRefresh = () => {
    setUsers(StorageService.getUsers());
    setTasks(StorageService.getTasks());
    setCurrentUser(StorageService.getCurrentUser());
  };

  const handleLoginSuccess = (user) => {
    StorageService.setCurrentUser(user);
    StorageService.setAuthUser(user);
    setCurrentUser(user);
    setAuthenticatedUser(user);

    if (user.role === 'ViceDirector' || user.role === 'Admin') {
      setActiveTab('planning');
    }
    setIsLoginModalOpen(false);
  };

  const handleSelectUser = (user) => {
    // Only Admin can switch views on the fly
    if (authenticatedUser?.role === 'Admin' || user.id === authenticatedUser?.id) {
      StorageService.setCurrentUser(user);
      setCurrentUser(user);
      if (user.role === 'ViceDirector') {
        setActiveTab('planning');
      }
    }
  };

  const handleLogout = () => {
    StorageService.logout();
    setAuthenticatedUser(null);
    setIsLoginModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-[var(--bg-app)] text-[var(--text-main)] flex flex-col font-sans selection:bg-indigo-500 selection:text-white transition-colors duration-300">
      
      {/* Top Navigation Bar with Official ООО «БМК» Logo */}
      <Navbar
        currentUser={currentUser}
        authenticatedUser={authenticatedUser}
        users={users}
        onSelectUser={handleSelectUser}
        onOpenAvatarModal={() => setIsLoginModalOpen(true)}
        onLogout={handleLogout}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentTheme={currentTheme}
        onThemeChange={handleThemeChange}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-[1440px] w-full mx-auto p-4 sm:p-6 lg:p-8">
        
        {/* Render View based on Current Logged In Role or Admin Inspecting Role */}
        {(currentUser.role === 'Director' || (authenticatedUser?.role === 'Admin' && currentUser.role === 'Director')) && (
          <GanttPlanner
            tasks={tasks}
            users={users}
            currentUser={currentUser}
            onTasksUpdated={handleDataRefresh}
          />
        )}

        {(currentUser.role === 'ViceDirector' || (authenticatedUser?.role === 'Admin' && currentUser.role === 'ViceDirector')) && (
          <>
            {activeTab === 'planning' ? (
              <GanttPlanner
                tasks={tasks}
                users={users}
                currentUser={currentUser}
                onTasksUpdated={handleDataRefresh}
              />
            ) : (
              <TravelAllowanceCalculator
                users={users}
                currentUser={currentUser}
              />
            )}
          </>
        )}

        {currentUser.role === 'Admin' && (
          <GanttPlanner
            tasks={tasks}
            users={users}
            currentUser={currentUser}
            onTasksUpdated={handleDataRefresh}
          />
        )}

        {currentUser.role === 'Engineer' && (
          <EngineerDashboard
            tasks={tasks}
            currentUser={currentUser}
            onTasksUpdated={handleDataRefresh}
          />
        )}

      </main>

      {/* Footer */}
      <footer className="glass-panel border-t border-slate-800/80 py-4 px-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            ООО «БМК» • Строительно-Монтажная Компания
          </div>
          <div>
            Разработано для Шмелёва В.В. и Администратора
          </div>
        </div>
      </footer>

      {/* PIN Login & Avatar Upload Modal */}
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        users={users}
        currentUser={currentUser}
        onLoginSuccess={handleLoginSuccess}
        onAvatarUpdated={handleDataRefresh}
      />

    </div>
  );
}

import { CloudSyncService } from './cloudSync';

const STORAGE_KEYS = {
  USERS: 'ag_app_users_v12',
  TASKS: 'ag_app_tasks_v12',
  TRAVEL: 'ag_app_travel_expenses_v12',
  CURRENT_USER: 'ag_app_current_user_v12',
  AUTH_USER: 'ag_app_auth_user_v12',
  THEME: 'ag_app_theme_v12',
  IS_AUTHENTICATED: 'ag_app_is_auth_v12',
};

// High quality reliable photo portraits with gender matching
export const DEFAULT_USERS = [
  // Админ (Мужской)
  {
    id: 'user-admin',
    name: 'Администратор системы',
    role: 'Admin',
    roleTitle: 'Главный администратор',
    category: 'Администрация',
    username: 'admin',
    pin: '135798642',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
    badge: 'Полный доступ ко всем профилям',
  },

  // Руководство (Мужчины)
  {
    id: 'user-director',
    name: 'Шмелёв В.В.',
    role: 'Director',
    roleTitle: 'Директор',
    category: 'Руководство',
    username: 'shmelev',
    pin: '1001',
    avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80',
    badge: 'Генеральное руководство',
  },
  {
    id: 'user-vice-moskovchenko',
    name: 'Московченко А.Н.',
    role: 'ViceDirector',
    roleTitle: 'Заместитель директора',
    category: 'Руководство',
    username: 'moskovchenko',
    pin: '1002',
    avatar: 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80',
    badge: 'Планирование и командировки',
  },
  {
    id: 'user-vice-dudkin',
    name: 'Дудкин Максим',
    role: 'ViceDirector',
    roleTitle: 'Заместитель директора',
    category: 'Руководство',
    username: 'dudkin',
    pin: '1003',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    badge: 'Оперативное руководство',
  },

  // Инженерный состав (Мужчины)
  {
    id: 'user-eng-chertok',
    name: 'Черток Алексей',
    role: 'Engineer',
    roleTitle: 'Главный инженер',
    category: 'Инженерный состав',
    username: 'chertok',
    pin: '2001',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-eng-khramenko',
    name: 'Храменко Алексей',
    role: 'Engineer',
    roleTitle: 'Инженер',
    category: 'Инженерный состав',
    username: 'khramenko',
    pin: '2002',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-eng-shcherbakov',
    name: 'Щербаков Анатолий',
    role: 'Engineer',
    roleTitle: 'Инженер',
    category: 'Инженерный состав',
    username: 'shcherbakov',
    pin: '2003',
    avatar: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-eng-litvinov',
    name: 'Литвинов Дмитрий',
    role: 'Engineer',
    roleTitle: 'Инженер',
    category: 'Инженерный состав',
    username: 'litvinov',
    pin: '2004',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-eng-khomyakov',
    name: 'Хомяков Василий',
    role: 'Engineer',
    roleTitle: 'Инженер',
    category: 'Инженерный состав',
    username: 'khomyakov',
    pin: '2005',
    avatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-eng-budatov',
    name: 'Будатов Денис',
    role: 'Engineer',
    roleTitle: 'Инженер',
    category: 'Инженерный состав',
    username: 'budatov',
    pin: '2006',
    avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-eng-aksenov',
    name: 'Аксенов Константин',
    role: 'Engineer',
    roleTitle: 'Инженер',
    category: 'Инженерный состав',
    username: 'aksenov',
    pin: '2007',
    avatar: 'https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=150&auto=format&fit=crop&q=80',
  },

  // Отдел ПТО (Женщины: Горетая Л., Кузнецова Я.; Мужчины: Ерышев М., Поплаухин Д.)
  {
    id: 'user-pto-goretaya',
    name: 'Горетая Людмила',
    role: 'Engineer',
    roleTitle: 'Инженер ПТО',
    category: 'Отдел ПТО',
    username: 'goretaya',
    pin: '3001',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-pto-eryshev',
    name: 'Ерышев Максим',
    role: 'Engineer',
    roleTitle: 'Инженер ПТО',
    category: 'Отдел ПТО',
    username: 'eryshev',
    pin: '3002',
    avatar: 'https://images.unsplash.com/photo-1521119989659-a83eee488004?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-pto-poplaukhin',
    name: 'Поплаухин Даниил',
    role: 'Engineer',
    roleTitle: 'Инженер ПТО',
    category: 'Отдел ПТО',
    username: 'poplaukhin',
    pin: '3003',
    avatar: 'https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=150&auto=format&fit=crop&q=80',
  },
  {
    id: 'user-pto-kuznetsova',
    name: 'Кузнецова Яна',
    role: 'Engineer',
    roleTitle: 'Сметчица',
    category: 'Отдел ПТО',
    username: 'kuznetsova',
    pin: '3004',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80',
  },

  // Прорабы (Мужчина)
  {
    id: 'user-prorab-radchenko',
    name: 'Радченко Андрей',
    role: 'Engineer',
    roleTitle: 'Прораб',
    category: 'Прорабы',
    username: 'radchenko',
    pin: '4001',
    avatar: 'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=150&auto=format&fit=crop&q=80',
  },
];

const getDateStr = (offsetDays = 0) => {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  return d.toISOString().split('T')[0];
};

export const DEFAULT_TASKS = [
  {
    id: 'task-101',
    title: 'Монтаж шкафов автоматики на объекте "Северный терминал"',
    description: 'Совместная задача: установить и протестировать 4 шкафа КИПиА, проверить кабельные трассы.',
    assignedToIds: ['user-eng-chertok', 'user-eng-khramenko'],
    assignedToNames: ['Черток Алексей', 'Храменко Алексей'],
    creatorId: 'user-director',
    creatorName: 'Шмелёв В.В. (Директор)',
    startDate: getDateStr(-2),
    endDate: getDateStr(5),
    status: 'in_progress',
    priority: 'high',
    progress: 40,
    reports: [
      {
        id: 'rep-1',
        date: getDateStr(-1),
        author: 'Храменко Алексей',
        text: 'Установлены 2 шкафа из 4. Проложены питающие кабели.',
        statusChange: 'in_progress',
        progress: 40
      }
    ]
  },
  {
    id: 'task-102',
    title: 'Подготовка исполнительной документации по объекту "Арбат"',
    description: 'Проверка комплекта АОСР, ведомостей и паспортов оборудования.',
    assignedToIds: ['user-pto-goretaya', 'user-pto-eryshev'],
    assignedToNames: ['Горетая Людмила', 'Ерышев Максим'],
    creatorId: 'user-director',
    creatorName: 'Шмелёв В.В. (Директор)',
    startDate: getDateStr(-5),
    endDate: getDateStr(2),
    status: 'in_progress',
    priority: 'urgent',
    progress: 75,
    reports: []
  },
  {
    id: 'task-103',
    title: 'Составление сметы на доп. работы по объекту "Подмосковье"',
    description: 'Расчет объемов материалов и калькуляция трудозатрат.',
    assignedToIds: ['user-pto-kuznetsova'],
    assignedToNames: ['Кузнецова Яна'],
    creatorId: 'user-vice-moskovchenko',
    creatorName: 'Московченко А.Н. (Зам. директора)',
    startDate: getDateStr(0),
    endDate: getDateStr(4),
    status: 'pending',
    priority: 'medium',
    progress: 0,
    reports: []
  },
  {
    id: 'task-104',
    title: 'Организация общестроительных работ на площадке',
    description: 'Руководство бригадами и контроль соблюдения графика производства работ.',
    assignedToIds: ['user-prorab-radchenko'],
    assignedToNames: ['Радченко Андрей'],
    creatorId: 'user-vice-dudkin',
    creatorName: 'Дудкин Максим (Зам. директора)',
    startDate: getDateStr(-3),
    endDate: getDateStr(3),
    status: 'in_progress',
    priority: 'high',
    progress: 50,
    reports: []
  }
];

export const getCurrentMonthYearStr = () => {
  const d = new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}`;
};

export const DEFAULT_TRAVEL_EXPENSES = {
  [getCurrentMonthYearStr()]: {
    'user-eng-chertok': [3, 5, 7, 10, 12, 14, 17, 19],
    'user-eng-khramenko': [4, 6, 11, 13, 18, 20],
    'user-prorab-radchenko': [1, 2, 8, 9, 15, 16, 22, 23],
    'user-vice-moskovchenko': [5, 12, 19, 26]
  }
};

export const StorageService = {
  getTheme: () => {
    return localStorage.getItem(STORAGE_KEYS.THEME) || 'dark';
  },
  setTheme: (theme) => {
    localStorage.setItem(STORAGE_KEYS.THEME, theme);
    document.documentElement.setAttribute('data-theme', theme);
  },

  getIsAuthenticated: () => {
    return localStorage.getItem(STORAGE_KEYS.IS_AUTHENTICATED) === 'true';
  },

  setIsAuthenticated: (isAuth) => {
    localStorage.setItem(STORAGE_KEYS.IS_AUTHENTICATED, isAuth ? 'true' : 'false');
  },

  getUsers: () => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.USERS);
      if (data) {
        const parsedUsers = JSON.parse(data);
        // Force update avatars to latest DEFAULT_USERS photo avatars if old svg/procedural links exist
        return parsedUsers.map(user => {
          const defaultUser = DEFAULT_USERS.find(d => d.id === user.id);
          if (defaultUser && (!user.avatar || user.avatar.includes('api.dicebear.com') || user.avatar.includes('robohash'))) {
            user.avatar = defaultUser.avatar;
          }
          return user;
        });
      }
    } catch (e) {
      console.error(e);
    }
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(DEFAULT_USERS));
    return DEFAULT_USERS;
  },

  getStaffUsers: () => {
    const users = StorageService.getUsers();
    return users.filter(u => u.id !== 'user-admin' && u.role !== 'Admin');
  },

  saveUsers: async (users) => {
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
    await CloudSyncService.pushToCloud();
  },

  updateUserAvatar: (userId, avatarDataUrl) => {
    const users = StorageService.getUsers();
    const uIndex = users.findIndex(u => u.id === userId);
    if (uIndex !== -1) {
      users[uIndex].avatar = avatarDataUrl;
      StorageService.saveUsers(users);
      
      const curr = StorageService.getCurrentUser();
      if (curr && curr.id === userId) {
        curr.avatar = avatarDataUrl;
        StorageService.setCurrentUser(curr);
      }
    }
    return users;
  },

  addUser: (newUser) => {
    const users = StorageService.getUsers();
    users.push(newUser);
    StorageService.saveUsers(users);
    return users;
  },

  getCurrentUser: () => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
      if (data) {
        const user = JSON.parse(data);
        const defaultUser = DEFAULT_USERS.find(d => d.id === user.id);
        if (defaultUser && (!user.avatar || user.avatar.includes('api.dicebear.com') || user.avatar.includes('robohash'))) {
          user.avatar = defaultUser.avatar;
        }
        return user;
      }
    } catch (e) {
      console.error(e);
    }
    return DEFAULT_USERS[1];
  },

  setCurrentUser: (user) => {
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
  },

  getAuthUser: () => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.AUTH_USER);
      if (data) return JSON.parse(data);
    } catch (e) {
      console.error(e);
    }
    return null;
  },

  setAuthUser: (user) => {
    localStorage.setItem(STORAGE_KEYS.AUTH_USER, JSON.stringify(user));
  },

  authenticateUser: (username, pin) => {
    const users = StorageService.getUsers();
    const target = users.find(u => 
      u.username.toLowerCase() === username.trim().toLowerCase() && 
      String(u.pin).trim() === String(pin).trim()
    );
    if (target) {
      StorageService.setAuthUser(target);
      StorageService.setCurrentUser(target);
      StorageService.setIsAuthenticated(true);
      return { success: true, user: target };
    }
    return { success: false, message: 'Неверный логин или пароль (ПИН-код)' };
  },

  logout: () => {
    StorageService.setIsAuthenticated(false);
    localStorage.removeItem(STORAGE_KEYS.AUTH_USER);
  },

  getTasks: () => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.TASKS);
      if (!data) return DEFAULT_TASKS;
      const tasks = JSON.parse(data);
      return tasks.map(t => {
        if (!t.assignedToIds) {
          t.assignedToIds = t.assignedToId ? [t.assignedToId] : [];
          t.assignedToNames = t.assignedToName ? [t.assignedToName] : [];
        }
        return t;
      });
    } catch (e) {
      console.error(e);
      return DEFAULT_TASKS;
    }
  },

  saveTasks: async (tasks) => {
    localStorage.setItem(STORAGE_KEYS.TASKS, JSON.stringify(tasks));
    await CloudSyncService.pushToCloud();
  },

  createTask: (newTaskData) => {
    const tasks = StorageService.getTasks();
    const newTask = {
      id: 'task-' + Date.now(),
      progress: 0,
      reports: [],
      status: 'pending',
      assignedToIds: newTaskData.assignedToIds || [],
      assignedToNames: newTaskData.assignedToNames || [],
      ...newTaskData
    };
    tasks.unshift(newTask);
    StorageService.saveTasks(tasks);
    return tasks;
  },

  updateTaskStatus: (taskId, newStatus, reportText = '', authorName = '', newProgress = null) => {
    const tasks = StorageService.getTasks();
    const taskIndex = tasks.findIndex(t => t.id === taskId);
    if (taskIndex !== -1) {
      tasks[taskIndex].status = newStatus;
      
      if (newProgress !== null && newProgress !== undefined) {
        tasks[taskIndex].progress = Math.min(100, Math.max(0, parseInt(newProgress, 10)));
      } else if (newStatus === 'completed') {
        tasks[taskIndex].progress = 100;
      }

      if (reportText || newProgress !== null || newStatus === 'in_progress') {
        if (!tasks[taskIndex].reports) tasks[taskIndex].reports = [];
        const noteText = reportText || (newStatus === 'in_progress' ? 'Принял задачу в работу' : `Обновлен прогресс работы: ${tasks[taskIndex].progress}%`);
        tasks[taskIndex].reports.unshift({
          id: 'rep-' + Date.now(),
          date: new Date().toISOString().split('T')[0],
          author: authorName,
          text: noteText,
          statusChange: newStatus,
          progress: tasks[taskIndex].progress
        });
      }
      StorageService.saveTasks(tasks);
    }
    return tasks;
  },

  deleteTask: (taskId) => {
    let tasks = StorageService.getTasks();
    tasks = tasks.filter(t => t.id !== taskId);
    StorageService.saveTasks(tasks);
    return tasks;
  },

  getTravelData: () => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.TRAVEL);
      return data ? JSON.parse(data) : DEFAULT_TRAVEL_EXPENSES;
    } catch (e) {
      console.error(e);
      return DEFAULT_TRAVEL_EXPENSES;
    }
  },

  saveTravelData: async (travelData) => {
    localStorage.setItem(STORAGE_KEYS.TRAVEL, JSON.stringify(travelData));
    await CloudSyncService.pushToCloud();
  },

  toggleTravelDay: (monthYearStr, userId, dayNumber) => {
    const travelData = StorageService.getTravelData();
    if (!travelData[monthYearStr]) {
      travelData[monthYearStr] = {};
    }
    if (!travelData[monthYearStr][userId]) {
      travelData[monthYearStr][userId] = [];
    }

    const currentDays = travelData[monthYearStr][userId];
    if (currentDays.includes(dayNumber)) {
      travelData[monthYearStr][userId] = currentDays.filter(d => d !== dayNumber);
    } else {
      travelData[monthYearStr][userId] = [...currentDays, dayNumber].sort((a, b) => a - b);
    }

    StorageService.saveTravelData(travelData);
    return travelData;
  },

  resetData: () => {
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(DEFAULT_USERS));
    localStorage.setItem(STORAGE_KEYS.TASKS, JSON.stringify(DEFAULT_TASKS));
    localStorage.setItem(STORAGE_KEYS.TRAVEL, JSON.stringify(DEFAULT_TRAVEL_EXPENSES));
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(DEFAULT_USERS[1]));
    localStorage.setItem(STORAGE_KEYS.IS_AUTHENTICATED, 'false');
    return {
      users: DEFAULT_USERS,
      tasks: DEFAULT_TASKS,
      travel: DEFAULT_TRAVEL_EXPENSES,
      currentUser: DEFAULT_USERS[1]
    };
  },

  exportJSON: () => {
    const exportObject = {
      users: StorageService.getUsers(),
      tasks: StorageService.getTasks(),
      travel: StorageService.getTravelData(),
      exportedAt: new Date().toISOString()
    };
    return JSON.stringify(exportObject, null, 2);
  },

  importJSON: (jsonStr) => {
    try {
      const parsed = JSON.parse(jsonStr);
      if (parsed.users) StorageService.saveUsers(parsed.users);
      if (parsed.tasks) StorageService.saveTasks(parsed.tasks);
      if (parsed.travel) StorageService.saveTravelData(parsed.travel);
      return true;
    } catch (e) {
      console.error('Invalid JSON', e);
      return false;
    }
  }
};

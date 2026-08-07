import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DB_FILE = path.join(__dirname, 'bmk_database.json');

const app = express();
const PORT = process.env.PORT || 4000;

// Enable Full CORS for all clients (GitHub Pages, local dev, mobile)
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'Accept']
}));

app.use(express.json({ limit: '10mb' }));

// Initial default database structure
const DEFAULT_DB = {
  updatedAt: new Date().toISOString(),
  tasks: [
    {
      id: 'task-1723000000001',
      title: 'Проектирование АСУ ТП и монтаж ОПС на объекте БМК №1',
      description: 'Монтаж шкафов управления, пусконаладочные работы, исполнительная документация АОСР.',
      startDate: '2026-08-01',
      endDate: '2026-08-15',
      priority: 'high',
      status: 'in_progress',
      progress: 60,
      assignedToIds: ['user-1', 'user-2'],
      assignedToNames: ['Черток А.', 'Храменко А.'],
      reports: [
        {
          id: 'rep-1',
          date: '2026-08-05',
          author: 'Черток А.',
          text: 'Завершен монтаж перфорированных лотков и укладка сигнальных кабелей в секторах A и B.',
          statusChange: 'in_progress',
          progress: 60
        }
      ]
    }
  ],
  travel: {},
  users: []
};

// Ensure database file exists
function loadDatabase() {
  try {
    if (fs.existsSync(DB_FILE)) {
      const data = fs.readFileSync(DB_FILE, 'utf-8');
      return JSON.parse(data);
    }
  } catch (e) {
    console.error('Error reading DB file:', e.message);
  }
  saveDatabase(DEFAULT_DB);
  return DEFAULT_DB;
}

function saveDatabase(db) {
  try {
    db.updatedAt = new Date().toISOString();
    fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2), 'utf-8');
  } catch (e) {
    console.error('Error writing DB file:', e.message);
  }
}

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', server: 'BMK Management Express Server', time: new Date().toISOString() });
});

// GET full database state
app.get('/api/sync', (req, res) => {
  const db = loadDatabase();
  res.json(db);
});

// POST update full database state (PUT/POST sync)
app.post('/api/sync', (req, res) => {
  const incomingData = req.body;
  if (!incomingData) {
    return res.status(400).json({ error: 'No data provided' });
  }

  const db = loadDatabase();

  if (Array.isArray(incomingData.tasks)) {
    db.tasks = incomingData.tasks;
  }
  if (incomingData.travel && typeof incomingData.travel === 'object') {
    db.travel = incomingData.travel;
  }
  if (Array.isArray(incomingData.users)) {
    db.users = incomingData.users;
  }

  saveDatabase(db);
  console.log(`[BMK Server] 🔄 Synced state. Tasks: ${db.tasks.length}`);
  res.json({ success: true, updatedAt: db.updatedAt, tasksCount: db.tasks.length });
});

// POST add/update single task
app.post('/api/tasks', (req, res) => {
  const task = req.body;
  if (!task || !task.title) {
    return res.status(400).json({ error: 'Invalid task payload' });
  }

  const db = loadDatabase();
  const existingIdx = db.tasks.findIndex(t => t.id === task.id);

  if (existingIdx !== -1) {
    db.tasks[existingIdx] = { ...db.tasks[existingIdx], ...task };
  } else {
    if (!task.id) task.id = 'task-' + Date.now();
    db.tasks.unshift(task);
  }

  saveDatabase(db);
  console.log(`[BMK Server] ➕ Task saved: "${task.title}"`);
  res.json({ success: true, task, updatedAt: db.updatedAt });
});

// Start Express server
app.listen(PORT, () => {
  console.log(`=================================================`);
  console.log(`🚀 ООО «БМК» Express Server is running on port ${PORT}`);
  console.log(`🌐 Health check: http://localhost:${PORT}/api/health`);
  console.log(`🌐 Sync endpoint: http://localhost:${PORT}/api/sync`);
  console.log(`=================================================`);
});

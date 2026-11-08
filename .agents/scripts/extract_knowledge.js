import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Функция для получения аргументов командной строки
function getArg(flag, defaultValue) {
  const index = process.argv.indexOf(flag);
  if (index !== -1 && index + 1 < process.argv.length) {
    return process.argv[index + 1];
  }
  return defaultValue;
}

// Определяем проект и контекст
const projectPath = process.cwd();
const defaultProjectName = path.basename(projectPath);
const projectName = getArg('--project', getArg('-p', defaultProjectName));

const sessionTitle = getArg('--title', getArg('-t', 'Автозахват сессии'));
const sessionId = getArg('--session', getArg('-s', process.env.ANTIGRAVITY_SESSION_ID || 'manual-' + Date.now()));

// Форматируем дату и время
const now = new Date();
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
const day = String(now.getDate()).padStart(2, '0');
const hours = String(now.getHours()).padStart(2, '0');
const minutes = String(now.getMinutes()).padStart(2, '0');
const seconds = String(now.getSeconds()).padStart(2, '0');

const dateStr = `${year}-${month}-${day}`;
const timestampStr = `${hours}${minutes}${seconds}`;

// Имя файла: YYYY-MM-DD-session-{project}-{timestamp}.md
const cleanProjectName = projectName.toLowerCase()
  .replace(/\s+/g, '-')
  .replace(/[^a-z0-9а-яё-]/gi, '');
const fileName = `${dateStr}-session-${cleanProjectName}-${timestampStr}.md`;

// Ищем корень проекта Antigravity, где находится папка .agents
let currentDir = __dirname;
let antigravityRoot = null;
for (let i = 0; i < 5; i++) {
  if (fs.existsSync(path.join(currentDir, '.agents'))) {
    antigravityRoot = currentDir;
    break;
  }
  currentDir = path.dirname(currentDir);
}

if (!antigravityRoot) {
  antigravityRoot = path.resolve(__dirname, '..', '..');
}

// Путь к Obsidian Vault находится на одном уровне с Antigravity (../Obsidian)
const obsidianVaultPath = path.resolve(antigravityRoot, '..', 'Obsidian');
const dailyNotesPath = path.join(obsidianVaultPath, 'Daily');

// Создаем папку Daily, если её нет
if (!fs.existsSync(dailyNotesPath)) {
  fs.mkdirSync(dailyNotesPath, { recursive: true });
}

const targetFilePath = path.join(dailyNotesPath, fileName);

const frontmatter = `---
title: "${sessionTitle}"
type: conversation
status: seed
created: ${dateStr}
updated: ${dateStr}
tags:
  - topic/session
  - project/${cleanProjectName}
  - status/seed
source: "${sessionId}"
summary: "Автоматически захваченный лог сессии"
related: []
---

# Разговор: ${sessionTitle}

## 🎯 Контекст сессии
*Сессия запущена в папке:* \`${projectPath}\`

## 📋 Выполненные действия
- [ ] Описать выполненные в ходе сессии действия.

## 🛠️ Изменения и кодовые паттерны
- [ ] Зафиксировать ключевой код и изменения.
`;

fs.writeFileSync(targetFilePath, frontmatter, 'utf8');
console.log(`[Успех] Лог сессии успешно создан: ${targetFilePath}`);

// Интеграция с Graphify
const graphifyReportSource = path.join(antigravityRoot, 'graphify-out', 'GRAPH_REPORT.md');
const reportsDestDir = path.join(obsidianVaultPath, 'Projects', 'graphify_reports');

if (fs.existsSync(graphifyReportSource)) {
  if (!fs.existsSync(reportsDestDir)) {
    fs.mkdirSync(reportsDestDir, { recursive: true });
  }
  const reportContent = fs.readFileSync(graphifyReportSource, 'utf8');
  
  const formattedReport = `---
title: "Архитектурный отчет Graphify — ${projectName}"
type: project
status: evergreen
created: ${dateStr}
updated: ${dateStr}
tags:
  - topic/architecture
  - project/${cleanProjectName}
  - status/evergreen
summary: "Локальный граф связей и ключевые концепты кодовой базы"
---

${reportContent}`;

  const reportDestFile = path.join(reportsDestDir, `${cleanProjectName}-report.md`);
  fs.writeFileSync(reportDestFile, formattedReport, 'utf8');
  console.log(`[Успех] Архитектурный отчет Graphify скопирован в Obsidian: ${reportDestFile}`);
}

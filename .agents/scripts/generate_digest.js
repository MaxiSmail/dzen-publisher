import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const antigravityRoot = path.resolve(__dirname, '..', '..');
const obsidianVault = path.resolve(antigravityRoot, '..', 'Obsidian');
const dailyDir = path.join(obsidianVault, 'Daily');

if (!fs.existsSync(dailyDir)) {
  fs.mkdirSync(dailyDir, { recursive: true });
}

const today = new Date().toISOString().split('T')[0];
const dailyFilePath = path.join(dailyDir, `${today}.md`);

// 1. Получаем недавние Git коммиты за 24 часа
let gitCommits = 'Коммиты отсутствуют';
try {
  gitCommits = execSync('git log --since="24 hours ago" --oneline', { cwd: antigravityRoot, encoding: 'utf8' }).trim() || 'Нет коммитов за последние 24 часа';
} catch (e) {
  gitCommits = 'Не удалось загрузить Git log';
}

// 2. Считываем активные проекты
const projectsDir = path.join(obsidianVault, 'Projects');
let projectList = [];
if (fs.existsSync(projectsDir)) {
  projectList = fs.readdirSync(projectsDir).filter(f => f.endsWith('.md')).map(f => f.replace('.md', ''));
}

const digestContent = `---
title: "ИИ-Дайджест за ${today}"
type: conversation
status: seed
created: ${today}
updated: ${today}
tags:
  - topic/digest
  - status/seed
summary: "Сводка результатов работы и коммитов за день"
---

# 📊 ИИ-Дайджест и Итоги Дня (${today})

> Автоматически сформированный отчет о выполненной работе в системе **Antigravity**.

---

## 🎯 Выполненные Git-коммиты (последние 24 часа)
\`\`\`text
${gitCommits}
\`\`\`

---

## 📁 Активные Проекты в Работе
${projectList.slice(0, 10).map(p => `* [[Projects/${p}|${p}]]`).join('\n')}

---

## 📌 Заметки и Планы на Завтра
- [ ] Проверить текущий статус задач в [[Мои Задачи|Едином Дашборде Задач]]
- [ ] Ознакомиться с картой проекта [[Карта проекта.canvas|Карта Проекта Canvas]]

---
*Создано автоматическим генератором Antigravity Digest.*
`;

fs.writeFileSync(dailyFilePath, digestContent, 'utf8');
console.log(`[Успех] ИИ-Дайджест дня сформирован в Obsidian: ${dailyFilePath}`);

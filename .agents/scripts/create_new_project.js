import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function getArg(flag, defaultValue) {
  const index = process.argv.indexOf(flag);
  if (index !== -1 && index + 1 < process.argv.length) {
    return process.argv[index + 1];
  }
  return defaultValue;
}

const rawName = getArg('--name', getArg('-n', null));
if (!rawName) {
  console.error('[Ошибка] Укажите название проекта: node create_new_project.js --name "МойНовыйПроект" --category "automation" --stack "python,fastapi"');
  process.exit(1);
}

const category = getArg('--category', getArg('-c', 'automation'));
const rawStack = getArg('--stack', getArg('-s', 'python,gemini-api'));
const stackList = rawStack.split(',').map(s => s.trim().toLowerCase());

const antigravityRoot = path.resolve(__dirname, '..', '..');
const obsidianVault = path.resolve(antigravityRoot, '..', 'Obsidian');

const projectFolderName = rawName.startsWith('Проект ') ? rawName : `Проект ${rawName}`;
const projectPath = path.join(antigravityRoot, projectFolderName);
const obsidianNotePath = path.join(obsidianVault, 'Projects', `${rawName.replace(/^Проект\s+/, '')}.md`);

// 1. Создаем папку в Antigravity
if (!fs.existsSync(projectPath)) {
  fs.mkdirSync(projectPath, { recursive: true });
}

// 2. Создаем .gitignore в проекте
const gitignoreContent = `# Исключения проекта
node_modules/
.venv/
__pycache__/
*.pyc
.env
.env.local
dist/
build/
*.log
`;
fs.writeFileSync(path.join(projectPath, '.gitignore'), gitignoreContent, 'utf8');

// 3. Создаем .env.example
const envExampleContent = `# Настройки и API Ключи проекта ${rawName}
PORT=3000
NODE_ENV=development
API_KEY=your_api_key_here
`;
fs.writeFileSync(path.join(projectPath, '.env.example'), envExampleContent, 'utf8');

// 4. Создаем базовый README.md в проекте
const readmeContent = `# ${rawName}

## 📋 Описание
Автоматически сгенерированный проект в системе **Antigravity**.

## 🛠 Стек технологий
${stackList.map(s => `- \`${s}\``).join('\n')}

## 🚀 Запуск проекта
\`\`\`bash
# Установите зависимости и заполните .env файл
cp .env.example .env
\`\`\`

---
*Документация и заметки проекта находятся в Obsidian:* \`[[Projects/${rawName.replace(/^Проект\s+/, '')}]]\`
`;
fs.writeFileSync(path.join(projectPath, 'README.md'), readmeContent, 'utf8');

// 5. Создаем карточку проекта в Obsidian
const dateStr = new Date().toISOString().split('T')[0];
const cleanTitle = rawName.replace(/^Проект\s+/, '');
const stackYaml = stackList.map(s => `  - "${s}"`).join('\n');

const obsidianNoteContent = `---
title: "${cleanTitle}"
status: "active"
category: "${category}"
stack:
${stackYaml}
code_path: "${projectFolderName}"
updated: ${dateStr}
---

# Проект: ${cleanTitle}

## 📋 Описание проекта
Инициализирован через генератор \`/new-project\`.

## 🛠 Технический Стек
${stackList.map(s => `* **\`${s}\`**`).join('\n')}

## 📂 Путь к кодовой базе
* **Папка репозитория:** [\`${projectFolderName}\`](file:///${projectPath.replace(/\\/g, '/')})

## 📌 Текущий Канбан / Задачи
- [ ] Сформулировать требования к MVP
- [ ] Настроить стартовую структуру кода
- [ ] Провести первое тестирование

---
**Связанные заметки:**
* [[База знаний|Главная Карта Знаний]]
* [[Мои Задачи|Единый Дашборд Задач]]
* [[Правила поведения ИИ]]
`;

fs.writeFileSync(obsidianNotePath, obsidianNoteContent, 'utf8');

console.log(`[Успех] Проект "${rawName}" успешно создан:`);
console.log(` - Папка кода: ${projectPath}`);
console.log(` - Карточка в Obsidian: ${obsidianNotePath}`);

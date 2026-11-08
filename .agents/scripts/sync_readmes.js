import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const antigravityRoot = path.resolve(__dirname, '..', '..');
const obsidianProjectsDir = path.resolve(antigravityRoot, '..', 'Obsidian', 'Projects');

if (!fs.existsSync(obsidianProjectsDir)) {
  console.error('[Ошибка] Папка Obsidian/Projects не найдена.');
  process.exit(1);
}

const files = fs.readdirSync(obsidianProjectsDir).filter(f => f.endsWith('.md'));
let syncedCount = 0;

for (const file of files) {
  const fullPath = path.join(obsidianProjectsDir, file);
  const content = fs.readFileSync(fullPath, 'utf8');
  
  let title = file.replace('.md', '');
  let status = 'active';
  let category = 'general';
  let codePathRel = null;

  const lines = content.split(/\r?\n/);
  let inFrontmatter = false;
  
  for (const line of lines) {
    if (line.trim() === '---') {
      if (!inFrontmatter) { inFrontmatter = true; continue; }
      else { break; }
    }
    if (inFrontmatter) {
      if (line.startsWith('title:')) {
        title = line.replace('title:', '').replace(/"/g, '').trim();
      } else if (line.startsWith('status:')) {
        status = line.replace('status:', '').replace(/"/g, '').trim();
      } else if (line.startsWith('category:')) {
        category = line.replace('category:', '').replace(/"/g, '').trim();
      } else if (line.startsWith('code_path:')) {
        codePathRel = line.replace('code_path:', '').replace(/"/g, '').trim();
      }
    }
  }
  
  if (!codePathRel) continue;
  
  const cleanRelPath = codePathRel.replace(/^Antigravity[\/\\]/, '');
  const targetProjectDir = path.join(antigravityRoot, cleanRelPath);
  
  if (fs.existsSync(targetProjectDir)) {
    const targetReadme = path.join(targetProjectDir, 'README.md');
    const readmeContent = `# ${title} 🚀

> **Статус:** \`${status}\` | **Категория:** \`${category}\`

## 📋 Описание
Этот проект входит в локальную рабочую среду **Antigravity**.

## 📁 Интеграция с Obsidian
* Карточка в базе знаний: \`[[Projects/${file.replace('.md', '')}]]\`
* Главная карта знаний: \`[[База знаний]]\`
* Единый дашборд задач: \`[[Мои Задачи]]\`

## 🛠 Руководство по разработке
1. Сверяйтесь с переменными окружения в \`.env.example\` перед запуском.
2. Проверяйте активный спринт и список задач в \`task.md\`.
`;
    fs.writeFileSync(targetReadme, readmeContent, 'utf8');
    syncedCount++;
    console.log(`[Синхронизация] Обновлен README.md в: ${codePathRel}`);
  }
}

console.log(`[Успех] Всего синхронизировано ${syncedCount} README.md файлов.`);

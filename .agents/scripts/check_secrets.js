import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const antigravityRoot = path.resolve(__dirname, '..', '..');

// Паттерны опасных открытых API-ключей
const secretPatterns = [
  { name: 'OpenAI API Key', regex: /sk-[a-zA-Z0-9]{32,64}/g },
  { name: 'Gemini API Key', regex: /AIzaSy[a-zA-Z0-9_-]{33}/g },
  { name: 'Telegram Bot Token', regex: /[0-9]{8,10}:AA[a-zA-Z0-9_-]{33}/g },
  { name: 'Stitch API Token', regex: /AQ\.[a-zA-Z0-9_-]{40,80}/g },
  { name: 'Private Key', regex: /-----BEGIN (RSA|EC|PRIVATE) KEY-----/g }
];

let stagedFiles = [];
try {
  const output = execSync('git diff --cached --name-only', { cwd: antigravityRoot, encoding: 'utf8' });
  stagedFiles = output.split(/\r?\n/).filter(f => f.trim().length > 0);
} catch (e) {
  stagedFiles = [];
}

let leaksFound = 0;

for (const file of stagedFiles) {
  // Пропускаем .env файлы (они и так в gitignore) и бинарные файлы
  if (file.endsWith('.env') || file.endsWith('.png') || file.endsWith('.jpg') || file.endsWith('.lock')) continue;
  
  const fullPath = path.join(antigravityRoot, file);
  if (!fs.existsSync(fullPath)) continue;
  
  const content = fs.readFileSync(fullPath, 'utf8');
  
  for (const pattern of secretPatterns) {
    if (pattern.regex.test(content)) {
      console.error(`[БЛОКИРОВКА СЕКУРИТИ] Найдена утечка секретного ключа (${pattern.name}) в файле: ${file}`);
      leaksFound++;
    }
  }
}

if (leaksFound > 0) {
  console.error(`\n[ОШИБКА] Коммит заблокирован. Вынесите ключи в секретный файл .env!`);
  process.exit(1);
} else {
  console.log(`[Страж Безопасности] Утечек API-ключей не обнаружено. Коммит разрешен.`);
  process.exit(0);
}

(function() {
    const rows = document.querySelectorAll('div[role="row"], div[dir="auto"]');
    const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
    const collected = [];

    rows.forEach(r => {
        const text = (r.innerText || '').trim();
        const rowLinks = Array.from(r.querySelectorAll('a[href]')).map(a => a.href);
        if (text || rowLinks.length) {
            collected.push({ text: text, urls: rowLinks });
        }
    });

    links.forEach(l => {
        if (l.includes('/reel/') || l.includes('/p/')) {
            collected.push({ text: '(Reel/Post)', urls: [l] });
        }
    });

    const payload = { items: collected };

    // Уведомление на странице
    function showToast(msg, isError) {
        const div = document.createElement('div');
        div.style.cssText = 'position:fixed;bottom:30px;right:30px;z-index:999999;padding:16px 24px;border-radius:12px;background:' + 
            (isError ? '#e74c3c' : '#2ecc71') + ';color:#fff;font-family:sans-serif;font-size:15px;box-shadow:0 10px 25px rgba(0,0,0,0.3);transition:all 0.3s;';
        div.innerText = msg;
        document.body.appendChild(div);
        setTimeout(() => { div.style.opacity = '0'; setTimeout(() => div.remove(), 400); }, 3500);
    }

    fetch('http://127.0.0.1:54321/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(res => {
        showToast('✅ Антигравити: ' + res.message, false);
    })
    .catch(err => {
        // Если сервер не запущен, сохраняем файлом
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'instagram_materials.json';
        a.click();
        showToast('⚠️ Сервер выключен. Скачан файл instagram_materials.json в Загрузки!', true);
    });
})();

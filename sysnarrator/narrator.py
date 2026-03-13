"""
SysNarrator — Core narration engine
Transforms raw system metrics into human-readable messages.
"""

import psutil
import time


class ProcessHistory:
    """Tracks process resource usage over time."""

    def __init__(self):
        self.records = {}

    def update(self):
        now = time.time()
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                pid = proc.info['pid']
                ram_mb = proc.info['memory_info'].rss / 1024 / 1024
                cpu = proc.info['cpu_percent']

                if pid not in self.records:
                    self.records[pid] = {
                        'name': proc.info['name'],
                        'ram_samples': [],
                        'cpu_samples': [],
                        'first_seen': now,
                    }

                r = self.records[pid]
                r['ram_samples'].append((now, ram_mb))
                r['cpu_samples'].append((now, cpu))

                cutoff = now - 1800
                r['ram_samples'] = [(t, v) for t, v in r['ram_samples'] if t > cutoff]
                r['cpu_samples'] = [(t, v) for t, v in r['cpu_samples'] if t > cutoff]

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        alive_pids = {p.pid for p in psutil.process_iter()}
        for pid in list(self.records):
            if pid not in alive_pids:
                del self.records[pid]

    def duration_minutes(self, pid: int) -> float:
        if pid not in self.records:
            return 0
        return (time.time() - self.records[pid]['first_seen']) / 60


class Narrator:
    """Main narration engine — converts metrics to human messages."""

    def __init__(self, lang: str = 'en', top_n: int = 5):
        self.lang = lang
        self.top_n = top_n
        self.boot_time = psutil.boot_time()
        self.history = ProcessHistory()

    def _fmt_bytes(self, mb: float) -> str:
        if mb >= 1024:
            return f"{mb/1024:.1f} GB" if self.lang == 'en' else f"{mb/1024:.1f} Go"
        return f"{mb:.0f} MB" if self.lang == 'en' else f"{mb:.0f} Mo"

    def _fmt_duration(self, minutes: float) -> str:
        if minutes < 1:
            return "less than a minute" if self.lang == 'en' else "moins d'une minute"
        elif minutes < 60:
            return f"{int(minutes)} min"
        elif minutes < 1440:
            h = int(minutes / 60)
            m = int(minutes % 60)
            return f"{h}h{m:02d}" if m else f"{h}h"
        else:
            d = int(minutes / 1440)
            s = 's' if d > 1 else ''
            return f"{d} day{s}" if self.lang == 'en' else f"{d} jour{s}"

    def _msg(self, key: str, **kwargs) -> str:
        messages = MESSAGES.get(self.lang, MESSAGES['en'])
        template = messages.get(key, MESSAGES['en'].get(key, key))
        try:
            return template.format(**kwargs)
        except KeyError:
            return template

    def narrate_cpu(self) -> list[dict]:
        msgs = []
        pct = psutil.cpu_percent(interval=0.5)
        cores = psutil.cpu_percent(interval=0.1, percpu=True)
        freq = psutil.cpu_freq()

        if pct > 90:
            level, key = 'critical', 'cpu_critical'
        elif pct > 70:
            level, key = 'warning', 'cpu_warning'
        elif pct > 40:
            level, key = 'info', 'cpu_moderate'
        else:
            level, key = 'ok', 'cpu_ok'

        msgs.append({'level': level, 'text': self._msg(key, pct=pct), 'category': 'CPU'})

        hot = [(i, v) for i, v in enumerate(cores) if v > 85]
        if hot:
            core_str = ', '.join(f"core {i} ({v:.0f}%)" for i, v in hot)
            msgs.append({'level': 'warning', 'text': self._msg('cpu_hot_cores', cores=core_str), 'category': 'CPU'})

        if freq:
            msgs.append({'level': 'info', 'text': self._msg('cpu_freq', cur=freq.current, mx=freq.max), 'category': 'CPU'})

        return msgs

    def narrate_memory(self) -> list[dict]:
        msgs = []
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        used = mem.used / 1024**3
        total = mem.total / 1024**3
        pct = mem.percent

        if pct > 90:
            level, key = 'critical', 'ram_critical'
        elif pct > 75:
            level, key = 'warning', 'ram_warning'
        elif pct > 50:
            level, key = 'info', 'ram_moderate'
        else:
            level, key = 'ok', 'ram_ok'

        msgs.append({'level': level, 'text': self._msg(key, used=used, total=total, pct=pct), 'category': 'RAM'})

        if swap.total > 0 and swap.percent > 10:
            su = swap.used / 1024**3
            st = swap.total / 1024**3
            level = 'warning' if swap.percent > 50 else 'info'
            key = 'swap_heavy' if swap.percent > 50 else 'swap_active'
            msgs.append({'level': level, 'text': self._msg(key, used=su, total=st), 'category': 'RAM'})

        return msgs

    def narrate_disk(self) -> list[dict]:
        msgs = []
        try:
            disk = psutil.disk_usage('/')
            free = disk.free / 1024**3
            total = disk.total / 1024**3
            pct = disk.percent

            if pct > 95:
                level, key = 'critical', 'disk_critical'
            elif pct > 85:
                level, key = 'warning', 'disk_warning'
            elif pct > 60:
                level, key = 'info', 'disk_moderate'
            else:
                level, key = 'ok', 'disk_ok'

            cat = 'Disk' if self.lang == 'en' else 'Disque'
            msgs.append({'level': level, 'text': self._msg(key, free=free, total=total, pct=pct), 'category': cat})
        except Exception:
            pass
        return msgs

    def narrate_network(self) -> list[dict]:
        msgs = []
        try:
            n1 = psutil.net_io_counters()
            time.sleep(1)
            n2 = psutil.net_io_counters()

            recv = (n2.bytes_recv - n1.bytes_recv) / 1024
            sent = (n2.bytes_sent - n1.bytes_sent) / 1024

            if recv > 1024 or sent > 1024:
                level, key = 'warning', 'net_heavy'
            elif recv > 100 or sent > 100:
                level, key = 'info', 'net_active'
            else:
                level, key = 'ok', 'net_quiet'

            cat = 'Network' if self.lang == 'en' else 'Réseau'
            msgs.append({'level': level, 'text': self._msg(key, recv=recv, sent=sent), 'category': cat})

            total_recv = n2.bytes_recv / 1024**3
            total_sent = n2.bytes_sent / 1024**3
            msgs.append({'level': 'info', 'text': self._msg('net_total', recv=total_recv, sent=total_sent), 'category': cat})
        except Exception:
            pass
        return msgs

    def narrate_temperature(self) -> list[dict]:
        msgs = []
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return []
            for chip, sensors in temps.items():
                for s in sensors:
                    if s.current and s.current > 0:
                        label = s.label or chip
                        t = s.current
                        if t > 85:
                            msgs.append({'level': 'critical', 'text': self._msg('temp_critical', label=label, t=t), 'category': 'Temp'})
                        elif t > 70:
                            msgs.append({'level': 'warning', 'text': self._msg('temp_warning', label=label, t=t), 'category': 'Temp'})
        except Exception:
            pass
        return msgs

    def narrate_uptime(self) -> list[dict]:
        minutes = (time.time() - self.boot_time) / 60
        hours = minutes / 60
        dur = self._fmt_duration(minutes)

        if hours > 720:
            level, key = 'warning', 'uptime_long'
        elif hours > 168:
            level, key = 'info', 'uptime_week'
        else:
            level, key = 'ok', 'uptime_ok'

        cat = 'System' if self.lang == 'en' else 'Système'
        return [{'level': level, 'text': self._msg(key, dur=dur), 'category': cat}]

    def narrate_top_processes(self) -> list[dict]:
        msgs = []
        self.history.update()

        procs = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                ram_mb = proc.info['memory_info'].rss / 1024 / 1024
                procs.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'ram_mb': ram_mb,
                    'cpu': proc.info['cpu_percent'],
                    'duration': self.history.duration_minutes(proc.info['pid']),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        top = sorted(procs, key=lambda x: x['ram_mb'], reverse=True)[:self.top_n]
        cat = 'Processes' if self.lang == 'en' else 'Processus'

        msgs.append({'level': 'info', 'text': '─' * 52, 'category': cat})
        msgs.append({'level': 'info', 'text': self._msg('proc_header', n=self.top_n), 'category': cat})

        for i, p in enumerate(top, 1):
            ram_str = self._fmt_bytes(p['ram_mb'])
            dur_str = self._fmt_duration(p['duration'])
            name = p['name'][:22]
            cpu_note = f" | CPU {p['cpu']:.0f}%" if p['cpu'] > 20 else ""
            level = 'warning' if p['ram_mb'] > 1500 else ('info' if p['ram_mb'] > 400 else 'ok')
            text = f"  {i}. {name:<22} (PID {p['pid']:>6})  → {ram_str} for {dur_str}{cpu_note}"
            msgs.append({'level': level, 'text': text, 'category': cat})

        if top and top[0]['ram_mb'] > 1500:
            p = top[0]
            msgs.append({
                'level': 'warning',
                'text': self._msg('proc_suggest', name=p['name'], ram=self._fmt_bytes(p['ram_mb']), dur=self._fmt_duration(p['duration'])),
                'category': cat
            })

        return msgs


# ─── Message Templates ──────────────────────────────────────────────────────────

MESSAGES = {
    'en': {
        'cpu_critical':  '🔥 CPU saturated at {pct:.0f}% — system is under extreme pressure.',
        'cpu_warning':   '⚡ CPU loaded at {pct:.0f}% — performance starting to degrade.',
        'cpu_moderate':  '💻 CPU active at {pct:.0f}% — moderate load, all good.',
        'cpu_ok':        '✅ CPU quiet at {pct:.0f}% — your machine is breathing easy.',
        'cpu_hot_cores': '🌡️  Overloaded cores: {cores} — unbalanced load.',
        'cpu_freq':      '⚙️  CPU frequency: {cur:.0f} MHz (max {mx:.0f} MHz)',
        'ram_critical':  '🚨 RAM critical: {used:.1f} GB / {total:.1f} GB ({pct:.0f}%) — freeze risk!',
        'ram_warning':   '⚠️  RAM under pressure: {used:.1f} GB / {total:.1f} GB ({pct:.0f}%) — close some apps.',
        'ram_moderate':  '📊 RAM at {pct:.0f}%: {used:.1f} GB used out of {total:.1f} GB — normal usage.',
        'ram_ok':        '✅ RAM comfortable: {used:.1f} GB / {total:.1f} GB ({pct:.0f}%) — plenty of headroom.',
        'swap_heavy':    '💾 Swap heavily used: {used:.1f} GB / {total:.1f} GB — disk compensating RAM, system slow.',
        'swap_active':   '💾 Swap active: {used:.2f} GB used — Linux is optimizing memory.',
        'disk_critical': '🚨 Disk almost full: only {free:.1f} GB left on {total:.0f} GB — urgent!',
        'disk_warning':  '⚠️  Disk at {pct:.0f}%: only {free:.1f} GB free — cleanup recommended.',
        'disk_moderate': '💿 Disk at {pct:.0f}% used — {free:.1f} GB available, keep an eye on it.',
        'disk_ok':       '✅ Disk OK: {free:.1f} GB free on {total:.0f} GB ({pct:.0f}% used).',
        'net_heavy':     '📡 High network traffic: ↓ {recv:.0f} KB/s — ↑ {sent:.0f} KB/s — check downloads.',
        'net_active':    '🌐 Network active: ↓ {recv:.0f} KB/s — ↑ {sent:.0f} KB/s',
        'net_quiet':     '✅ Network quiet: ↓ {recv:.1f} KB/s — ↑ {sent:.1f} KB/s',
        'net_total':     '📊 Total traffic (since boot): ↓ {recv:.2f} GB received — ↑ {sent:.2f} GB sent',
        'temp_critical': '🌡️  {label}: {t:.0f}°C — CRITICAL! Thermal throttling risk.',
        'temp_warning':  '🌡️  {label}: {t:.0f}°C — Getting warm, check cooling.',
        'uptime_long':   '⏰ Uptime: {dur} — system running very long, a reboot may help.',
        'uptime_week':   '⏰ Uptime: {dur} — stable system, running for over a week.',
        'uptime_ok':     '⏰ Uptime: {dur} — freshly started.',
        'proc_header':   '🔍 Top {n} RAM-hungry processes:',
        'proc_suggest':  '💡 Tip: {name} has been using {ram} for {dur} — restarting it could free memory.',
    },
    'fr': {
        'cpu_critical':  '🔥 CPU saturé à {pct:.0f}% — le système est sous pression extrême.',
        'cpu_warning':   '⚡ CPU chargé à {pct:.0f}% — les performances commencent à se dégrader.',
        'cpu_moderate':  '💻 CPU actif à {pct:.0f}% — charge modérée, tout va bien.',
        'cpu_ok':        '✅ CPU tranquille à {pct:.0f}% — votre machine respire.',
        'cpu_hot_cores': '🌡️  Cores en surchauffe : {cores} — charge déséquilibrée.',
        'cpu_freq':      '⚙️  Fréquence CPU : {cur:.0f} MHz (max {mx:.0f} MHz)',
        'ram_critical':  '🚨 RAM critique : {used:.1f} Go / {total:.1f} Go ({pct:.0f}%) — risque de freeze !',
        'ram_warning':   '⚠️  RAM sous pression : {used:.1f} Go / {total:.1f} Go ({pct:.0f}%) — fermez des apps.',
        'ram_moderate':  '📊 RAM à {pct:.0f}% : {used:.1f} Go utilisés sur {total:.1f} Go — usage normal.',
        'ram_ok':        '✅ RAM confortable : {used:.1f} Go / {total:.1f} Go ({pct:.0f}%) — beaucoup de marge.',
        'swap_heavy':    '💾 Swap très utilisé : {used:.1f} Go / {total:.1f} Go — disque compense RAM, système lent.',
        'swap_active':   '💾 Swap actif : {used:.2f} Go utilisés — Linux optimise la mémoire.',
        'disk_critical': '🚨 Disque presque plein : {free:.1f} Go restants sur {total:.0f} Go — urgence !',
        'disk_warning':  '⚠️  Disque à {pct:.0f}% : seulement {free:.1f} Go libres — nettoyage recommandé.',
        'disk_moderate': '💿 Disque à {pct:.0f}% utilisé — {free:.1f} Go disponibles, surveillez.',
        'disk_ok':       '✅ Disque OK : {free:.1f} Go libres sur {total:.0f} Go ({pct:.0f}% utilisé).',
        'net_heavy':     '📡 Trafic réseau élevé : ↓ {recv:.0f} Ko/s — ↑ {sent:.0f} Ko/s — vérifiez les téléchargements.',
        'net_active':    '🌐 Réseau actif : ↓ {recv:.0f} Ko/s — ↑ {sent:.0f} Ko/s',
        'net_quiet':     '✅ Réseau calme : ↓ {recv:.1f} Ko/s — ↑ {sent:.1f} Ko/s',
        'net_total':     '📊 Trafic total (depuis boot) : ↓ {recv:.2f} Go reçus — ↑ {sent:.2f} Go envoyés',
        'temp_critical': '🌡️  {label} : {t:.0f}°C — CRITIQUE ! Risque de throttling thermique.',
        'temp_warning':  '🌡️  {label} : {t:.0f}°C — Ça chauffe, vérifiez le refroidissement.',
        'uptime_long':   '⏰ Uptime : {dur} — machine allumée très longtemps, redémarrage conseillé.',
        'uptime_week':   '⏰ Uptime : {dur} — système stable depuis plus d\'une semaine.',
        'uptime_ok':     '⏰ Uptime : {dur} — démarré récemment.',
        'proc_header':   '🔍 Top {n} processus les plus gourmands en RAM :',
        'proc_suggest':  '💡 Suggestion : {name} consomme {ram} depuis {dur} — redémarrer pourrait libérer de la mémoire.',
    },
    'ar': {
        'cpu_critical':  '🔥 وحدة المعالجة مثقلة بنسبة {pct:.0f}% — النظام تحت ضغط شديد.',
        'cpu_warning':   '⚡ المعالج محمل بنسبة {pct:.0f}% — الأداء يبدأ في التراجع.',
        'cpu_moderate':  '💻 المعالج نشط بنسبة {pct:.0f}% — حمل معتدل، كل شيء بخير.',
        'cpu_ok':        '✅ المعالج هادئ بنسبة {pct:.0f}% — جهازك يعمل بارتياح.',
        'cpu_hot_cores': '🌡️  أنوية ساخنة: {cores} — حمل غير متوازن.',
        'cpu_freq':      '⚙️  تردد المعالج: {cur:.0f} ميغاهرتز (الحد الأقصى {mx:.0f})',
        'ram_critical':  '🚨 ذاكرة RAM حرجة: {used:.1f} GB / {total:.1f} GB ({pct:.0f}%) — خطر التجميد!',
        'ram_warning':   '⚠️  ذاكرة RAM تحت ضغط: {used:.1f} GB / {total:.1f} GB ({pct:.0f}%) — أغلق تطبيقات.',
        'ram_moderate':  '📊 ذاكرة RAM بنسبة {pct:.0f}%: {used:.1f} GB من {total:.1f} GB — استخدام طبيعي.',
        'ram_ok':        '✅ ذاكرة RAM مريحة: {used:.1f} GB / {total:.1f} GB ({pct:.0f}%) — مساحة كافية.',
        'swap_heavy':    '💾 Swap مستخدم بكثافة: {used:.1f} GB / {total:.1f} GB — القرص يعوض RAM.',
        'swap_active':   '💾 Swap نشط: {used:.2f} GB مستخدم — Linux يحسّن الذاكرة.',
        'disk_critical': '🚨 القرص شبه ممتلئ: {free:.1f} GB فقط من {total:.0f} GB — عاجل!',
        'disk_warning':  '⚠️  القرص بنسبة {pct:.0f}%: {free:.1f} GB فقط متاح — يُنصح بالتنظيف.',
        'disk_moderate': '💿 القرص بنسبة {pct:.0f}% مستخدم — {free:.1f} GB متاح.',
        'disk_ok':       '✅ القرص بخير: {free:.1f} GB متاح من {total:.0f} GB ({pct:.0f}% مستخدم).',
        'net_heavy':     '📡 حركة شبكة عالية: ↓ {recv:.0f} KB/s — ↑ {sent:.0f} KB/s',
        'net_active':    '🌐 الشبكة نشطة: ↓ {recv:.0f} KB/s — ↑ {sent:.0f} KB/s',
        'net_quiet':     '✅ الشبكة هادئة: ↓ {recv:.1f} KB/s — ↑ {sent:.1f} KB/s',
        'net_total':     '📊 إجمالي البيانات: ↓ {recv:.2f} GB مستلمة — ↑ {sent:.2f} GB مرسلة',
        'temp_critical': '🌡️  {label}: {t:.0f}°م — خطر! خطر الاختناق الحراري.',
        'temp_warning':  '🌡️  {label}: {t:.0f}°م — يسخن، تحقق من التبريد.',
        'uptime_long':   '⏰ وقت التشغيل: {dur} — الجهاز يعمل منذ وقت طويل، أعد التشغيل.',
        'uptime_week':   '⏰ وقت التشغيل: {dur} — نظام مستقر منذ أكثر من أسبوع.',
        'uptime_ok':     '⏰ وقت التشغيل: {dur} — تم التشغيل مؤخراً.',
        'proc_header':   '🔍 أكثر {n} عمليات استهلاكاً للذاكرة:',
        'proc_suggest':  '💡 نصيحة: {name} يستهلك {ram} منذ {dur} — إعادة تشغيله قد يحرر الذاكرة.',
    },
}

"""Tests for SysNarrator"""
import pytest
from sysnarrator.narrator import Narrator, MESSAGES


class TestNarrator:

    def test_init_default(self):
        n = Narrator()
        assert n.lang == 'en'
        assert n.top_n == 5

    def test_fmt_bytes_mb(self):
        n = Narrator()
        assert 'MB' in n._fmt_bytes(500)

    def test_fmt_bytes_gb(self):
        n = Narrator()
        assert 'GB' in n._fmt_bytes(2048)

    def test_fmt_bytes_fr(self):
        n = Narrator(lang='fr')
        assert 'Go' in n._fmt_bytes(2048)

    def test_fmt_duration_minutes(self):
        n = Narrator()
        assert '45 min' in n._fmt_duration(45)

    def test_fmt_duration_hours(self):
        n = Narrator()
        assert '1h' in n._fmt_duration(90)

    def test_all_languages_have_same_keys(self):
        en_keys = set(MESSAGES['en'].keys())
        for lang in ['fr', 'ar']:
            missing = en_keys - set(MESSAGES[lang].keys())
            assert not missing, f"Missing keys in '{lang}': {missing}"

    def test_narrate_cpu_returns_list(self):
        n = Narrator()
        result = n.narrate_cpu()
        assert isinstance(result, list)
        assert len(result) > 0
        assert all('level' in m and 'text' in m for m in result)

    def test_narrate_memory_returns_list(self):
        n = Narrator()
        result = n.narrate_memory()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_narrate_disk_returns_list(self):
        n = Narrator()
        result = n.narrate_disk()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_narrate_uptime_returns_list(self):
        n = Narrator()
        result = n.narrate_uptime()
        assert len(result) == 1
        assert result[0]['level'] in ('ok', 'info', 'warning', 'critical')

    def test_levels_are_valid(self):
        n = Narrator()
        valid = {'ok', 'info', 'warning', 'critical'}
        for method in [n.narrate_cpu, n.narrate_memory, n.narrate_disk, n.narrate_uptime]:
            for msg in method():
                assert msg['level'] in valid

    def test_french_works(self):
        n = Narrator(lang='fr')
        assert len(n.narrate_uptime()) > 0

    def test_arabic_works(self):
        n = Narrator(lang='ar')
        assert len(n.narrate_uptime()) > 0


class TestCLI:

    def test_build_parser(self):
        from sysnarrator.cli import build_parser
        parser = build_parser()
        assert parser is not None

    def test_watch_flag(self):
        from sysnarrator.cli import build_parser
        args = build_parser().parse_args(['--watch'])
        assert args.watch is True

    def test_default_interval(self):
        from sysnarrator.cli import build_parser
        args = build_parser().parse_args([])
        assert args.interval == 3.0

    def test_lang_flag(self):
        from sysnarrator.cli import build_parser
        args = build_parser().parse_args(['--lang', 'fr'])
        assert args.lang == 'fr'

import unittest
import os
import re

class TestWebsite(unittest.TestCase):
    def setUp(self):
        # O diretório base é o diretório PersonalPage
        self.base_path = os.path.join(os.getcwd(), 'PersonalPage')
        self.index_path = os.path.join(self.base_path, 'index.html')
        self.script_path = os.path.join(self.base_path, 'script.js')

    def test_files_exist(self):
        self.assertTrue(os.path.exists(self.index_path), f"index.html não encontrado em {self.index_path}")
        self.assertTrue(os.path.exists(self.script_path), f"script.js não encontrado em {self.script_path}")

    def test_translations_integrity(self):
        with open(self.script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        languages = ['pt', 'en', 'es']
        keys_by_lang = {}
        
        for lang in languages:
            # Regex para encontrar o bloco de cada idioma
            lang_match = re.search(rf'{lang}: \{{(.*?)\}}', content, re.DOTALL)
            self.assertIsNotNone(lang_match, f"Idioma {lang} não encontrado nas traduções")
            
            # Encontrar todas as chaves dentro do bloco do idioma (dentro de aspas duplas)
            keys = re.findall(r'"(.*?)"\s*:', lang_match.group(1))
            keys_by_lang[lang] = set(keys)

        # Validar que todos os idiomas possuem as mesmas chaves
        pt_keys = keys_by_lang['pt']
        self.assertGreater(len(pt_keys), 0, "Dicionário de tradução PT está vazio")
        
        for lang in ['en', 'es']:
            diff = pt_keys - keys_by_lang[lang]
            self.assertEqual(len(diff), 0, f"As seguintes chaves estão faltando em {lang}: {diff}")
            
            extra = keys_by_lang[lang] - pt_keys
            self.assertEqual(len(extra), 0, f"As seguintes chaves são extras em {lang}: {extra}")

    def test_html_i18n_keys_exist_in_script(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        with open(self.script_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
            
        # Pegar chaves de PT como referência
        pt_match = re.search(r'pt: \{(.*?)\}', js_content, re.DOTALL)
        pt_keys = set(re.findall(r'"(.*?)"\s*:', pt_match.group(1)))
        
        # Encontrar todos os data-i18n no HTML
        html_keys = set(re.findall(r'data-i18n="(.*?)"', html_content))
        
        for key in html_keys:
            self.assertIn(key, pt_keys, f"Chave i18n '{key}' encontrada no HTML mas não no script.js")

    def test_clock_elements_exist(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        self.assertIn('clock', html_content)
        self.assertIn('hour-hand', html_content)
        self.assertIn('minute-hand', html_content)
        self.assertIn('second-hand', html_content)

if __name__ == '__main__':
    unittest.main()

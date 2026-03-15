"""
config.py - Chatbot yapılandırma ayarları
"""

import json
import os

class Config:
    def __init__(self, intents_file="intents.json"):
        # Çalışma dizinini al
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # JSON dosyasının tam yolunu oluştur
        self.intents_file = os.path.join(self.current_dir, intents_file)
        self.intents_data = self.load_intents()
        self.similarity_threshold = 0.6  # Benzerlik eşiği
        self.debug_mode = False  # Hata ayıklama modu
        
    def load_intents(self):
        """JSON dosyasından intentleri yükle"""
        try:
            print(f"🔍 JSON dosyası aranıyor: {self.intents_file}")
            
            if os.path.exists(self.intents_file):
                with open(self.intents_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    intents = data.get('intents', [])
                    print(f"✅ {len(intents)} intent başarıyla yüklendi!")
                    return intents
            else:
                print(f"❌ {self.intents_file} bulunamadı!")
                print(f"📁 Çalışma dizini: {os.getcwd()}")
                print(f"📁 Dosyanın bulunduğu dizin: {self.current_dir}")
                return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON dosyası okunamadı: {e}")
            return []
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return []
    
    def reload_intents(self):
        """Intentleri yeniden yükle (çalışma zamanında güncelleme için)"""
        self.intents_data = self.load_intents()
        return len(self.intents_data) > 0
    
    def get_all_patterns(self):
        """Tüm pattern'leri topla (benzerlik kontrolü için)"""
        patterns = []
        for intent in self.intents_data:
            patterns.extend(intent.get('patterns', []))
        return patterns
    
    def get_intent_by_tag(self, tag):
        """Tag'e göre intent bul"""
        for intent in self.intents_data:
            if intent.get('tag') == tag:
                return intent
        return None

# Global config nesnesi
config = Config()

# Test için
if __name__ == "__main__":
    print(f"✅ Config başarıyla yüklendi!")
    print(f"📊 Toplam intent sayısı: {len(config.intents_data)}")
"""
main.py - MiniChatBot ana programı
JSON tabanlı intent yönetimi
"""

import random
import difflib
from config import config
import functions

# Renkli çıktı için
try:
    from colorama import init, Fore, Style
    init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

class MiniChatBot:
    def __init__(self, name="Asistan"):
        self.name = name
        self.user_name = None
        self.message_count = 0
        self.context = {}
        
        # Intentleri yükle
        self.intents = config.intents_data
        self.all_patterns = config.get_all_patterns()
        
        print(f"\n📁 {len(self.intents)} intent yüklendi")
        self.show_welcome()
    
    def print_colored(self, text, color="white"):
        if COLOR_ENABLED:
            colors = {
                "red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW,
                "blue": Fore.BLUE, "magenta": Fore.MAGENTA, "cyan": Fore.CYAN,
                "white": Fore.WHITE
            }
            print(f"{colors.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}")
        else:
            print(text)
    
    def show_welcome(self):
        """Hoş geldin mesajı"""
        self.print_colored(f"\n{'='*50}", "blue")
        self.print_colored(f"🤖 {self.name} size hoş geldiniz!", "green")
        self.print_colored(f"{'='*50}", "blue")
        print("📝 'yardım' yazarak neler yapabileceğimi görebilirsiniz.")
    
    def find_intent(self, message):
        """
        Mesaja en uygun intent'i bul
        """
        message = message.lower().strip()
        
        # 1. Önce tam eşleşme ara
        for intent in self.intents:
            for pattern in intent.get('patterns', []):
                if pattern.lower() == message:
                    return intent, pattern, 1.0
        
        # 2. Mesaj pattern içinde geçiyor mu?
        for intent in self.intents:
            for pattern in intent.get('patterns', []):
                if pattern.lower() in message:
                    return intent, pattern, 0.9
        
        # 3. Benzerlik kontrolü
        best_match = None
        best_score = 0
        best_pattern = None
        
        for intent in self.intents:
            for pattern in intent.get('patterns', []):
                # difflib ile benzerlik hesapla
                score = difflib.SequenceMatcher(None, message, pattern.lower()).ratio()
                
                # Özel durumlar
                if pattern == "merhaba" and message in ["merhba", "mrhba", "meraba", "mrb", "slm"]:
                    score = 0.8
                if pattern == "nasılsın" and message in ["nslsn", "nasılsn", "nasılsın"]:
                    score = 0.8
                if pattern == "teşekkürler" and message in ["tşk", "thx", "sağol"]:
                    score = 0.8
                
                if score > best_score and score >= config.similarity_threshold:
                    best_score = score
                    best_match = intent
                    best_pattern = pattern
        
        if best_match:
            return best_match, best_pattern, best_score
        
        # 4. Hiçbir şey bulunamadı
        return None, None, 0
    
    def process_message(self, message):
        """
        Gelen mesajı işle ve cevap üret
        """
        message = message.lower().strip()
        self.message_count += 1
        
        # Intent bul
        intent, matched_pattern, score = self.find_intent(message)
        
        if intent:
            # Debug modunda benzerlik skorunu göster
            if config.debug_mode and matched_pattern != message:
                self.print_colored(f"[Debug] '{message}' -> '{matched_pattern}' (benzerlik: {score:.2f})", "yellow")
            
            # Tag'e göre işlem yap
            response = self.generate_response(intent, message)
            return response
        else:
            # Bilinmeyen intent
            unknown_intent = config.get_intent_by_tag("unknown")
            if unknown_intent:
                return random.choice(unknown_intent.get('responses', ["Anlayamadım."]))
            return "Anlayamadım."
    
    def generate_response(self, intent, original_message):
        """
        Intent'e göre cevap üret
        """
        tag = intent.get('tag', 'unknown')
        responses = intent.get('responses', [])
        
        if not responses:
            return "Bu konuda ne diyeceğimi bilemedim."
        
        # Rastgele bir cevap şablonu seç
        response_template = random.choice(responses)
        
        # Fonksiyon çağrısı varsa
        if 'function' in intent:
            function_name = intent['function']
            func = getattr(functions, function_name, None)
            
            if func:
                # Fonksiyonu çağır
                if function_name in ['search_web', 'search_wiki']:
                    result = func(original_message)
                else:
                    result = func()
                
                # Şablona yerleştir
                if tag == 'time':
                    return response_template.format(time=result)
                elif tag == 'date':
                    return response_template.format(date=result)
                elif tag == 'calendar':
                    return response_template.format(calendar=result)
                elif tag == 'web_search':
                    # Sorguyu temizle
                    query = original_message
                    for p in intent.get('patterns', []):
                        query = query.replace(p.lower(), '')
                    query = query.strip()
                    return response_template.format(query=query if query else "bilgi")
                elif tag == 'wiki_search':
                    return result  # Wiki zaten formatlı geliyor
                else:
                    return result
        
        # İsim işleme
        if tag == 'name':
            name = self.extract_name(original_message)
            if name:
                self.user_name = name
                return response_template.format(name=name)
        
        # Basit cevap
        return response_template
    
    def extract_name(self, message):
        """Mesajdan isim çıkar"""
        message = message.lower()
        if "benim adım" in message:
            return message.replace("benim adım", "").strip().split()[0] if message.replace("benim adım", "").strip() else None
        elif "adım" in message:
            return message.replace("adım", "").strip().split()[0] if message.replace("adım", "").strip() else None
        return None
    
    def run(self):
        """Ana çalışma döngüsü"""
        while True:
            try:
                # Kullanıcıdan input al
                prompt = f"\n{self.user_name} > " if self.user_name else "\nSiz > "
                user_input = input(prompt)
                
                if not user_input.strip():
                    continue
                
                # Çıkış kontrolü
                if user_input.lower() in ['çıkış', 'quit', 'exit']:
                    goodbye = config.get_intent_by_tag("goodbye")
                    if goodbye:
                        print(f"\n{self.name}: {random.choice(goodbye['responses'])}")
                    break
                
                # Mesajı işle
                response = self.process_message(user_input)
                
                # Cevabı yazdır
                self.print_colored(f"{self.name}: {response}", "green")
                
                # İstatistik
                if self.message_count % 5 == 0:
                    self.print_colored(f"(📊 {self.message_count} mesaj konuştuk)", "blue")
                    
            except KeyboardInterrupt:
                print("\n\nProgramdan çıkılıyor...")
                break
            except Exception as e:
                self.print_colored(f"Bir hata oluştu: {str(e)}", "red")

if __name__ == "__main__":
    bot = MiniChatBot(name="MiniBot")
    bot.run()
    print("\nProgram sonlandı. Tekrar bekleriz!")
"""
functions.py - Chatbot işlem fonksiyonları
"""

import datetime
import webbrowser
import wikipedia
import random

# ========== ZAMAN FONKSİYONLARI ==========

def get_time():
    """Şu anki saati döndürür"""
    now = datetime.datetime.now()
    return f"{now.strftime('%H')}:{now.strftime('%M')}"

def get_date():
    """Bugünün tarihini Türkçe döndürür"""
    now = datetime.datetime.now()
    days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    
    return f"{now.day} {months[now.month-1]} {now.year}, {days[now.weekday()]}"

def show_calendar():
    """Basit takvim bilgisi"""
    now = datetime.datetime.now()
    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    
    # Ayın kaç gün olduğunu hesapla
    if now.month == 2:
        if (now.year % 400 == 0) or (now.year % 4 == 0 and now.year % 100 != 0):
            days = 29
        else:
            days = 28
    elif now.month in [4, 6, 9, 11]:
        days = 30
    else:
        days = 31
    
    return f"{months[now.month-1]} {now.year} ayı {days} gün çekiyor. Bugün ayın {now.day}. günü."

# ========== ARAMA FONKSİYONLARI ==========

def search_web(query):
    """Google'da arama yap"""
    # Sorguyu temizle
    search_terms = query.lower()
    for phrase in ["ara", "google'da ara", "internette ara", "google", "search"]:
        search_terms = search_terms.replace(phrase, "")
    
    search_terms = search_terms.strip()
    
    if not search_terms:
        search_terms = "chatbot"
    
    # Google'da aç
    url = f"https://www.google.com/search?q={search_terms}"
    webbrowser.open(url)
    
    return f"🔍 '{search_terms}' aranıyor..."

def search_wiki(query):
    """Wikipedia'da arama yap"""
    # Sorguyu temizle
    search_terms = query.lower()
    for phrase in ["wikipedia'da ara", "vikipedi", "wiki", "wikipedia"]:
        search_terms = search_terms.replace(phrase, "")
    
    search_terms = search_terms.strip()
    
    if not search_terms:
        return "Ne aramak istersiniz?"
    
    try:
        wikipedia.set_lang("tr")
        page = wikipedia.page(search_terms)
        summary = wikipedia.summary(search_terms, sentences=2)
        
        return f"📚 **{page.title}**\n{summary}\n🔗 {page.url}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]
        return f"Birden çok sonuç var: {', '.join(options)}"
    except wikipedia.exceptions.PageError:
        return "Wikipedia'da böyle bir sayfa bulamadım."
    except Exception as e:
        return f"Hata: {str(e)}"
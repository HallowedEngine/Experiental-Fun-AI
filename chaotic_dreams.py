#!/usr/bin/env python3
"""
🌌 KAOTİK DÜŞLER MAKİNESİ 🌌
Deneysel ve Eğlenceli AI Projesi

Modüller:
1. 🧬 Evrimsel ASCII Sanat - Genetik algoritma ile ASCII sanat evriltir
2. 🎭 Sürreal Hikaye Üreteci - Absürt ve rüya gibi hikayeler üretir
3. 🎪 Emoji Hayat Simülasyonu - Conway's Game of Life ama emojilerle!
4. 🔮 Dijital Fal Bakıcısı - Metinden mistik yorumlar üretir
5. 🎵 Metin Senfonisi - Metni görsel müziğe dönüştürür
6. 🌀 Düşünce Labirenti - Sonsuz felsefi paradokslar üretir

Yazar: Claude AI
"""

import random
import time
import os
import sys
import hashlib
from collections import defaultdict
from typing import List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 RENK VE GÖRSEL YARDIMCILAR
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Terminal renkleri için ANSI kodları"""
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    END = '\033[0m'

    RAINBOW = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE]

    @staticmethod
    def rainbow_text(text: str) -> str:
        result = ""
        for i, char in enumerate(text):
            if char != ' ':
                result += Colors.RAINBOW[i % len(Colors.RAINBOW)] + char
            else:
                result += char
        return result + Colors.END

    @staticmethod
    def gradient_text(text: str, start_color: str, end_color: str) -> str:
        return start_color + text + Colors.END


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def slow_print(text: str, delay: float = 0.03):
    """Dramatik efekt için yavaş yazdırma"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_box(text: str, color: str = Colors.CYAN):
    """Metin etrafında kutu çizer"""
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    print(color + "╔" + "═" * (max_len + 2) + "╗")
    for line in lines:
        print("║ " + line.ljust(max_len) + " ║")
    print("╚" + "═" * (max_len + 2) + "╝" + Colors.END)


# ═══════════════════════════════════════════════════════════════════════════════
# 🧬 MODÜL 1: EVRİMSEL ASCII SANAT
# ═══════════════════════════════════════════════════════════════════════════════

class EvolutionaryArt:
    """Genetik algoritma ile ASCII sanat evriltir"""

    ASCII_CHARS = " .:-=+*#%@█▓▒░╔╗╚╝║═╬╠╣╦╩●○◐◑◒◓★☆✦✧♠♣♥♦"

    def __init__(self, width: int = 40, height: int = 15):
        self.width = width
        self.height = height
        self.population_size = 20
        self.mutation_rate = 0.1

    def create_individual(self) -> List[List[str]]:
        """Rastgele bir birey (sanat eseri) oluşturur"""
        return [[random.choice(self.ASCII_CHARS)
                 for _ in range(self.width)]
                for _ in range(self.height)]

    def fitness(self, individual: List[List[str]], target_pattern: str) -> float:
        """
        Fitness fonksiyonu - simetri, yoğunluk ve desen uyumu
        """
        score = 0.0

        # Dikey simetri bonusu
        for row in individual:
            for i in range(len(row) // 2):
                if row[i] == row[-(i+1)]:
                    score += 1

        # Merkez yoğunluğu bonusu (ortada daha yoğun karakterler)
        center_y, center_x = self.height // 2, self.width // 2
        for y, row in enumerate(individual):
            for x, char in enumerate(row):
                dist = ((y - center_y) ** 2 + (x - center_x) ** 2) ** 0.5
                char_weight = self.ASCII_CHARS.index(char) / len(self.ASCII_CHARS)
                if dist < min(center_x, center_y):
                    score += char_weight * (1 - dist / min(center_x, center_y))

        # Hedef paterne göre bonus
        flat = ''.join(''.join(row) for row in individual)
        pattern_hash = int(hashlib.md5(target_pattern.encode()).hexdigest()[:8], 16)
        random.seed(pattern_hash)
        target_density = random.random()
        actual_density = sum(self.ASCII_CHARS.index(c) for c in flat) / (len(flat) * len(self.ASCII_CHARS))
        score += (1 - abs(target_density - actual_density)) * 100

        return score

    def crossover(self, parent1: List[List[str]], parent2: List[List[str]]) -> List[List[str]]:
        """İki ebeveyni birleştir"""
        child = []
        for y in range(self.height):
            if random.random() < 0.5:
                child.append(parent1[y][:])
            else:
                child.append(parent2[y][:])
        return child

    def mutate(self, individual: List[List[str]]) -> List[List[str]]:
        """Mutasyon uygula"""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < self.mutation_rate:
                    individual[y][x] = random.choice(self.ASCII_CHARS)
        return individual

    def evolve(self, target: str, generations: int = 50, animate: bool = True):
        """Evrim sürecini çalıştır"""
        population = [self.create_individual() for _ in range(self.population_size)]

        print(f"\n{Colors.GREEN}🧬 '{target}' için sanat evriltiyor...{Colors.END}\n")

        for gen in range(generations):
            # Fitness hesapla ve sırala
            scored = [(ind, self.fitness(ind, target)) for ind in population]
            scored.sort(key=lambda x: x[1], reverse=True)

            if animate and gen % 5 == 0:
                clear_screen()
                print(f"{Colors.YELLOW}Nesil {gen+1}/{generations} - En iyi fitness: {scored[0][1]:.2f}{Colors.END}\n")
                self.display(scored[0][0])
                time.sleep(0.1)

            # Seçim - en iyi %50'yi tut
            survivors = [ind for ind, _ in scored[:self.population_size // 2]]

            # Yeni nesil oluştur
            new_population = survivors[:]
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(survivors, 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        # Final sonuç
        best = max(population, key=lambda x: self.fitness(x, target))
        clear_screen()
        print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
        print(f"{Colors.BOLD}🎨 EVRİLMİŞ SANAT: '{target}'{Colors.END}")
        print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")
        self.display(best, color=True)
        return best

    def display(self, individual: List[List[str]], color: bool = False):
        """Sanat eserini görüntüle"""
        for y, row in enumerate(individual):
            line = ''.join(row)
            if color:
                # Satıra göre renk gradyanı
                color_code = Colors.RAINBOW[y % len(Colors.RAINBOW)]
                print(color_code + line + Colors.END)
            else:
                print(line)


# ═══════════════════════════════════════════════════════════════════════════════
# 🎭 MODÜL 2: SÜRREAL HİKAYE ÜRETECİ
# ═══════════════════════════════════════════════════════════════════════════════

class SurrealStoryGenerator:
    """Sürreal ve rüya gibi hikayeler üretir"""

    def __init__(self):
        self.subjects = [
            "Mor bir fil", "Ters yürüyen saat", "Şeffaf bir gölge",
            "Uçan bir balina", "Ağlayan bir robot", "Dans eden bir matematik denklemi",
            "Buharlaşan bir anı", "Konuşan bir sessizlik", "Donmuş bir alev",
            "Uyuyan bir rüya", "Kaybolan bir ayna", "Düşen bir gökyüzü",
            "Gülen bir boşluk", "Koşan bir dün", "Yüzen bir taş",
            "Eriyen bir gece", "Büyüyen bir küçüklük", "Parlayan bir karanlık"
        ]

        self.verbs = [
            "yuttu", "doğurdu", "çoğalttı", "sardı", "dönüştürdü",
            "fısıldadı", "unuttu", "hatırladı", "böldü", "birleştirdi",
            "dans etti", "eridi", "dondu", "uçtu", "battı",
            "patladı", "büzüldü", "genişledi", "yankılandı", "sustu"
        ]

        self.objects = [
            "zamanın köşelerini", "unutulmuş melodileri", "doğmamış düşünceleri",
            "eski yarınları", "yeni dünleri", "sayıların rüyalarını",
            "renklerin kokusunu", "sesin gölgesini", "boşluğun ağırlığını",
            "sonsuzun kenarını", "hiçliğin merkezini", "her şeyin yokluğunu",
            "paralel evrenlerin kavşağını", "kuantum kedisinin kuyruğunu",
            "evrenin ilk şakasını", "son kahkahanın yankısını"
        ]

        self.locations = [
            "sonsuz bir kütüphanede", "ters akan bir nehirde", "düşen bir gökte",
            "kristal bir düşüncede", "bulanık bir kesinlikte", "keskin bir belirsizlikte",
            "zamanın kıvrımında", "uzayın düğümünde", "rüyanın uyanık yanında",
            "gerçekliğin çatlaklarında", "mantığın dışında", "saçmalığın merkezinde"
        ]

        self.connectors = [
            "Ve böylece,", "Tam o anda,", "Hiç beklenmedik şekilde,",
            "Tüm bunlar olurken,", "Zamanın ötesinde,", "Bir paralel evrende,",
            "Rüyanın derinliklerinde,", "Mantığın terk ettiği yerde,",
            "Sonsuzluğun bir köşesinde,", "Kaosun kalbinde,"
        ]

        self.endings = [
            "ve evren bir an için gülümsedi.",
            "ve hiçbir şey eskisi gibi olmadı, ama aynı kaldı.",
            "ve zaman durdu, ama akışını sürdürdü.",
            "ve tüm sorular cevap oldu, cevaplar ise soru.",
            "ve sessizlik konuştu, kelimeler sustu.",
            "ve her şey başladığı yerde bitti, bittiği yerde başladı.",
            "ve rüya uyanıklığı, uyanıklık rüyayı kucakladı.",
            "ve evren kendi kuyruğunu yutarak gülmeye başladı.",
            "ve sonsuzluk bir anlık oldu, an ise sonsuz.",
            "ve tüm hikayeler bu cümlede birleşti, ayrıldı."
        ]

    def generate_sentence(self) -> str:
        """Tek bir sürreal cümle üret"""
        return f"{random.choice(self.subjects)} {random.choice(self.verbs)} {random.choice(self.objects)} {random.choice(self.locations)}."

    def generate_story(self, paragraphs: int = 3) -> str:
        """Tam bir sürreal hikaye üret"""
        story = []

        # Giriş
        story.append(f"Bir {'gece' if random.random() < 0.5 else 'gündüz'}... hayır, belki de ikisi de değildi... ya da ikisi de birden...")
        story.append("")

        for p in range(paragraphs):
            paragraph = []
            paragraph.append(random.choice(self.connectors))

            for _ in range(random.randint(2, 4)):
                paragraph.append(self.generate_sentence())

            story.append(" ".join(paragraph))
            story.append("")

        # Bitiş
        story.append(random.choice(self.endings))

        return "\n".join(story)

    def dream_interpretation(self, seed_word: str) -> str:
        """Bir kelimeden sürreal yorum üret"""
        random.seed(hash(seed_word))

        interpretations = [
            f"'{seed_word}' kelimesi, evrenin {random.choice(['unuttuğu', 'hatırladığı', 'sakladığı'])} bir sırrı temsil eder.",
            f"Rüyanda {seed_word} gördüğünde, bu {random.choice(['zamanın', 'uzayın', 'bilincin'])} sana mesaj verdiği anlamına gelir.",
            f"{seed_word.upper()} - her harf bir boyutu temsil eder: " + ", ".join([f"'{c}' = {random.choice(['sonsuzluk', 'hiçlik', 'her şey', 'belki'])}" for c in seed_word[:4]]),
            f"Antik {random.choice(['Maya', 'Sümer', 'Atlantis', 'Lemurya'])} kehanetlerine göre, '{seed_word}' kozmik uyanışın {random.randint(1,12)}. aşamasını simgeler."
        ]

        random.seed()  # Reset seed
        return random.choice(interpretations)

    def interactive_story(self):
        """İnteraktif sürreal hikaye deneyimi"""
        clear_screen()
        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")
        print(f"{Colors.BOLD}🎭 SÜRREAL HİKAYE ÜRETECİ{Colors.END}")
        print(f"{Colors.PURPLE}{'═' * 60}{Colors.END}\n")

        print(f"{Colors.CYAN}Bir tohum kelime girin (veya boş bırakın):{Colors.END} ", end="")
        seed = input().strip()

        if seed:
            random.seed(hash(seed))
            print(f"\n{Colors.DIM}'{seed}' tohumundan büyüyen hikaye...{Colors.END}\n")
            time.sleep(1)

        story = self.generate_story(random.randint(2, 4))

        print(f"{Colors.YELLOW}{'─' * 60}{Colors.END}\n")

        for line in story.split('\n'):
            if line.strip():
                slow_print(Colors.GREEN + line + Colors.END, delay=0.02)
            else:
                print()
            time.sleep(0.3)

        print(f"\n{Colors.YELLOW}{'─' * 60}{Colors.END}")

        if seed:
            print(f"\n{Colors.PURPLE}🔮 Rüya Yorumu:{Colors.END}")
            print(Colors.ITALIC + self.dream_interpretation(seed) + Colors.END)

        random.seed()  # Reset


# ═══════════════════════════════════════════════════════════════════════════════
# 🎪 MODÜL 3: EMOJİ HAYAT SİMÜLASYONU
# ═══════════════════════════════════════════════════════════════════════════════

class EmojiLifeSimulation:
    """Conway's Game of Life - Emoji versiyonu!"""

    STATES = {
        'dead': '  ',
        'alive': '██',
        'dying': '▒▒',
        'born': '░░'
    }

    EMOJI_THEMES = {
        'classic': ['  ', '██'],
        'nature': ['🌊', '🌲'],
        'space': ['  ', '⭐'],
        'hearts': ['💔', '❤️'],
        'faces': ['😴', '😊'],
        'cosmic': ['🌑', '🌟'],
        'matrix': ['  ', '01'],
        'quantum': ['◯ ', '◉ '],
    }

    def __init__(self, width: int = 30, height: int = 15, theme: str = 'cosmic'):
        self.width = width
        self.height = height
        self.theme = theme
        self.grid = [[False for _ in range(width)] for _ in range(height)]
        self.generation = 0
        self.history = []

    def randomize(self, density: float = 0.3):
        """Rastgele başlangıç durumu"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = random.random() < density

    def set_pattern(self, pattern: str):
        """Önceden tanımlı patern yükle"""
        patterns = {
            'glider': [(0,1), (1,2), (2,0), (2,1), (2,2)],
            'blinker': [(1,0), (1,1), (1,2)],
            'toad': [(1,1), (1,2), (1,3), (2,0), (2,1), (2,2)],
            'beacon': [(0,0), (0,1), (1,0), (2,3), (3,2), (3,3)],
            'pulsar': [],  # Complex pattern
            'spaceship': [(0,1), (0,4), (1,0), (2,0), (2,4), (3,0), (3,1), (3,2), (3,3)],
        }

        # Glider gun (simplified)
        if pattern == 'glider_gun':
            self.randomize(0.15)
            return

        if pattern in patterns:
            self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
            offset_y, offset_x = self.height // 3, self.width // 3
            for dy, dx in patterns[pattern]:
                if 0 <= offset_y + dy < self.height and 0 <= offset_x + dx < self.width:
                    self.grid[offset_y + dy][offset_x + dx] = True

    def count_neighbors(self, y: int, x: int) -> int:
        """Komşu sayısını hesapla"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = (y + dy) % self.height, (x + dx) % self.width
                if self.grid[ny][nx]:
                    count += 1
        return count

    def step(self):
        """Bir nesil ilerlet"""
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(y, x)
                if self.grid[y][x]:
                    # Canlı hücre
                    new_grid[y][x] = neighbors in [2, 3]
                else:
                    # Ölü hücre
                    new_grid[y][x] = neighbors == 3

        self.history.append([row[:] for row in self.grid])
        if len(self.history) > 10:
            self.history.pop(0)

        self.grid = new_grid
        self.generation += 1

    def display(self):
        """Mevcut durumu göster"""
        dead_char, alive_char = self.EMOJI_THEMES.get(self.theme, self.EMOJI_THEMES['classic'])

        # Üst çerçeve
        print(f"{Colors.CYAN}╔{'═' * (self.width * 2)}╗{Colors.END}")

        for row in self.grid:
            line = ""
            for cell in row:
                line += alive_char if cell else dead_char
            print(f"{Colors.CYAN}║{Colors.END}{Colors.YELLOW}{line}{Colors.END}{Colors.CYAN}║{Colors.END}")

        # Alt çerçeve
        print(f"{Colors.CYAN}╚{'═' * (self.width * 2)}╝{Colors.END}")

    def population(self) -> int:
        """Canlı hücre sayısı"""
        return sum(sum(row) for row in self.grid)

    def is_stable(self) -> bool:
        """Simülasyon kararlı mı kontrol et"""
        if len(self.history) < 2:
            return False
        return self.grid == self.history[-1] or (len(self.history) >= 2 and self.grid == self.history[-2])

    def run_simulation(self, max_generations: int = 100, delay: float = 0.15):
        """Simülasyonu çalıştır"""
        clear_screen()
        print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
        print(f"{Colors.BOLD}🎪 EMOJİ HAYAT SİMÜLASYONU{Colors.END}")
        print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")

        print(f"{Colors.CYAN}Tema: {Colors.END}{self.theme}")
        print(f"{Colors.CYAN}Başlangıç popülasyonu: {Colors.END}{self.population()}")
        print(f"\n{Colors.DIM}Simülasyon başlıyor... (Ctrl+C ile durdurabilirsiniz){Colors.END}\n")
        time.sleep(1)

        try:
            for _ in range(max_generations):
                clear_screen()
                print(f"{Colors.GREEN}Nesil: {self.generation} | Popülasyon: {self.population()}{Colors.END}\n")
                self.display()

                if self.is_stable():
                    print(f"\n{Colors.YELLOW}🔄 Kararlı durum veya döngü tespit edildi!{Colors.END}")
                    break

                if self.population() == 0:
                    print(f"\n{Colors.RED}💀 Tüm yaşam sona erdi...{Colors.END}")
                    break

                self.step()
                time.sleep(delay)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Simülasyon durduruldu.{Colors.END}")

        print(f"\n{Colors.PURPLE}Final - Nesil: {self.generation} | Hayatta kalan: {self.population()}{Colors.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔮 MODÜL 4: DİJİTAL FAL BAKICISI
# ═══════════════════════════════════════════════════════════════════════════════

class DigitalOracle:
    """Dijital mistik yorumlar üretir"""

    def __init__(self):
        self.elements = ['🔥 Ateş', '💧 Su', '🌍 Toprak', '💨 Hava', '⚡ Eter']
        self.planets = ['☉ Güneş', '☽ Ay', '☿ Merkür', '♀ Venüs', '♂ Mars', '♃ Jüpiter', '♄ Satürn']
        self.archetypes = [
            'Kaşif', 'Bilge', 'Savaşçı', 'Yaratıcı', 'Koruyucu',
            'Dönüştürücü', 'Rüya Gören', 'Bağlayıcı', 'Yıkıcı', 'İnşa Eden'
        ]

        self.prophecies = [
            "Karanlık içinde bir ışık parlar, ama asıl aydınlık gölgelerdedir.",
            "Aradığın cevap, sormayı unuttuğun soruda gizli.",
            "Kapılar kapanırken pencereler açılır; ama bazen duvardan geçmek gerekir.",
            "Geçmiş değişmez, ama geçmişe bakış açın değişebilir - ve bu her şeyi değiştirir.",
            "Beklenmedik olan beklenmelidir; beklenen ise çoktan geçmiştir.",
            "Yol seni seçti, sen yolu seçtiğini sanırken.",
            "Her son bir başlangıçtır, her başlangıç ise hiç bitmemiş bir sondur.",
            "Evren seninle konuşuyor; mesele doğru dili anlamakta.",
            "Şans diye bir şey yoktur; sadece fark edilmemiş nedensellik vardır.",
            "Bugün yarının dünüdür; bu anı yaşa, çünkü an'lar sonsuzluğu oluşturur."
        ]

    def analyze_text(self, text: str) -> dict:
        """Metni analiz et ve mistik değerler çıkar"""
        # Basit numeroloji
        letter_sum = sum(ord(c) for c in text.lower() if c.isalpha())
        digit_sum = sum(int(c) for c in text if c.isdigit()) or 1

        # Temel değerler
        life_number = (letter_sum % 9) + 1
        destiny_number = ((letter_sum + digit_sum) % 9) + 1

        # Element ve gezegen
        element = self.elements[letter_sum % len(self.elements)]
        planet = self.planets[digit_sum % len(self.planets)]
        archetype = self.archetypes[(letter_sum + digit_sum) % len(self.archetypes)]

        # Enerji dağılımı
        random.seed(letter_sum)
        energies = {
            'Yaratıcılık': random.randint(40, 100),
            'Sezgi': random.randint(40, 100),
            'Mantık': random.randint(40, 100),
            'Duygu': random.randint(40, 100),
            'Eylem': random.randint(40, 100),
        }
        random.seed()

        return {
            'life_number': life_number,
            'destiny_number': destiny_number,
            'element': element,
            'planet': planet,
            'archetype': archetype,
            'energies': energies,
            'prophecy': random.choice(self.prophecies)
        }

    def generate_mandala(self, seed: str, size: int = 11) -> List[str]:
        """Kişiselleştirilmiş ASCII mandala üret"""
        random.seed(hash(seed))

        symbols = ['◯', '◉', '●', '○', '◐', '◑', '★', '☆', '✦', '✧', '◆', '◇', '∞', '§', '¤']

        half_size = size // 2
        mandala = [[' ' for _ in range(size)] for _ in range(size)]

        # Merkez
        center = size // 2
        mandala[center][center] = '☯'

        # Daireler çiz
        for radius in range(1, half_size + 1):
            symbol = random.choice(symbols)
            points = []

            # Daire üzerindeki noktalar
            for i in range(radius * 8):
                angle = (i / (radius * 8)) * 2 * 3.14159
                y = int(center + radius * 0.7 * (angle / 3.14159 - 1) * (-1 if i % 2 else 1))
                x = int(center + radius * ((i % 4) / 2 - 1))

                if 0 <= y < size and 0 <= x < size:
                    points.append((y, x))

            # Simetrik yerleşim
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    dist = (dy * dy + dx * dx) ** 0.5
                    if abs(dist - radius) < 0.7:
                        y, x = center + dy, center + dx
                        if 0 <= y < size and 0 <= x < size and mandala[y][x] == ' ':
                            mandala[y][x] = symbol

        random.seed()
        return [''.join(row) for row in mandala]

    def draw_energy_bar(self, name: str, value: int) -> str:
        """Enerji çubuğu çiz"""
        bar_length = 20
        filled = int(value / 100 * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        return f"{name:12} [{bar}] {value}%"

    def divine(self, query: str):
        """Fal bak"""
        clear_screen()
        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")
        print(f"{Colors.BOLD}🔮 DİJİTAL FAL BAKICISI{Colors.END}")
        print(f"{Colors.PURPLE}{'═' * 60}{Colors.END}\n")

        print(f"{Colors.DIM}Kozmik enerjiler analiz ediliyor...{Colors.END}")
        time.sleep(0.5)

        # Dramatik animasyon
        symbols = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']
        for i in range(16):
            print(f"\r{symbols[i % 8]} Kehanet oluşturuluyor... {symbols[(i+4) % 8]}", end='', flush=True)
            time.sleep(0.1)
        print("\r" + " " * 40 + "\r", end='')

        analysis = self.analyze_text(query)

        # Sonuçları göster
        print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.BOLD}Sorgunuz:{Colors.END} {query[:45]:45} {Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.END}")

        print(f"\n{Colors.YELLOW}📊 MİSTİK PROFİL:{Colors.END}")
        print(f"   Yaşam Sayısı: {Colors.GREEN}{analysis['life_number']}{Colors.END}")
        print(f"   Kader Sayısı: {Colors.GREEN}{analysis['destiny_number']}{Colors.END}")
        print(f"   Element: {Colors.GREEN}{analysis['element']}{Colors.END}")
        print(f"   Gezegen: {Colors.GREEN}{analysis['planet']}{Colors.END}")
        print(f"   Arketip: {Colors.GREEN}{analysis['archetype']}{Colors.END}")

        print(f"\n{Colors.YELLOW}⚡ ENERJİ DAĞILIMI:{Colors.END}")
        for name, value in analysis['energies'].items():
            color = Colors.GREEN if value > 70 else (Colors.YELLOW if value > 50 else Colors.RED)
            print(f"   {color}{self.draw_energy_bar(name, value)}{Colors.END}")

        print(f"\n{Colors.YELLOW}🌀 KİŞİSEL MANDALA:{Colors.END}")
        mandala = self.generate_mandala(query)
        for line in mandala:
            print(f"   {Colors.PURPLE}{line}{Colors.END}")

        print(f"\n{Colors.YELLOW}📜 KEHANET:{Colors.END}")
        print(f"   {Colors.ITALIC}{Colors.CYAN}\"{analysis['prophecy']}\"{Colors.END}")

        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎵 MODÜL 5: METİN SENFONİSİ
# ═══════════════════════════════════════════════════════════════════════════════

class TextSymphony:
    """Metni görsel müziğe dönüştürür"""

    NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    NOTE_SYMBOLS = ['♩', '♪', '♫', '♬', '𝅗𝅥', '𝅘𝅥', '𝅘𝅥𝅮']

    def __init__(self):
        self.tempo = 120
        self.key = 'C'

    def text_to_melody(self, text: str) -> List[Tuple[str, int, str]]:
        """Metni melodiye çevir: [(nota, oktav, süre), ...]"""
        melody = []

        for char in text.lower():
            if char.isalpha():
                # Harfi notaya çevir
                note_index = (ord(char) - ord('a')) % 7
                note = self.NOTES[note_index]
                octave = 4 + ((ord(char) - ord('a')) // 7)
                duration = '♩' if char.isupper() else '♪'
                melody.append((note, octave, duration))
            elif char.isdigit():
                # Rakamları özel notalara çevir
                note = self.NOTES[int(char) % 7]
                melody.append((note, 5, '♫'))
            elif char == ' ':
                melody.append(('REST', 0, '𝄽'))
            elif char in '.,!?':
                melody.append(('REST', 0, '𝄾'))

        return melody

    def melody_to_staff(self, melody: List[Tuple[str, int, str]], width: int = 60) -> List[str]:
        """Melodiyi nota çizgisine çevir"""
        staff_lines = [
            "─" * width,  # Üst çizgi
            "─" * width,
            "─" * width,
            "─" * width,
            "─" * width,  # Alt çizgi
        ]

        # Nota pozisyonları (basitleştirilmiş)
        note_positions = {'C': 5, 'D': 4, 'E': 4, 'F': 3, 'G': 3, 'A': 2, 'B': 2, 'REST': 3}

        staff = [list(line) for line in staff_lines]

        for i, (note, octave, duration) in enumerate(melody[:width-2]):
            if note == 'REST':
                symbol = '𝄽'
            else:
                symbol = random.choice(self.NOTE_SYMBOLS)

            pos = note_positions.get(note, 3) - 1
            if 0 <= pos < 5 and i + 1 < width:
                staff[pos][i + 1] = symbol

        return [''.join(line) for line in staff]

    def generate_waveform(self, melody: List[Tuple[str, int, str]], width: int = 60) -> List[str]:
        """Dalga formu görselleştirmesi"""
        height = 9
        waveform = [[' ' for _ in range(width)] for _ in range(height)]

        center = height // 2

        for x, (note, octave, _) in enumerate(melody[:width]):
            if note == 'REST':
                y = center
            else:
                note_idx = self.NOTES.index(note) if note in self.NOTES else 0
                amplitude = (note_idx - 3) + (octave - 4) * 2
                y = max(0, min(height - 1, center - amplitude))

            waveform[y][x] = '█'

            # Dikey çizgi
            start, end = min(y, center), max(y, center)
            for fill_y in range(start, end + 1):
                if waveform[fill_y][x] == ' ':
                    waveform[fill_y][x] = '│'

        return [''.join(row) for row in waveform]

    def analyze_mood(self, melody: List[Tuple[str, int, str]]) -> str:
        """Melodinin ruh halini analiz et"""
        if not melody:
            return "Sessiz düşünce"

        notes = [n for n, _, _ in melody if n != 'REST']
        if not notes:
            return "Dingin sessizlik"

        avg_note = sum(self.NOTES.index(n) for n in notes if n in self.NOTES) / len(notes)

        moods = [
            (0, 2, "Melankolik ve derin"),
            (2, 4, "Düşünceli ve sakin"),
            (4, 5, "Dengeli ve huzurlu"),
            (5, 6, "Neşeli ve enerjik"),
            (6, 7, "Coşkulu ve parlak")
        ]

        for low, high, mood in moods:
            if low <= avg_note < high:
                return mood

        return "Gizemli ve karmaşık"

    def visualize(self, text: str):
        """Metni müzik olarak görselleştir"""
        clear_screen()
        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")
        print(f"{Colors.BOLD}🎵 METİN SENFONİSİ{Colors.END}")
        print(f"{Colors.PURPLE}{'═' * 60}{Colors.END}\n")

        print(f"{Colors.CYAN}Metin:{Colors.END} \"{text[:50]}{'...' if len(text) > 50 else ''}\"\n")

        melody = self.text_to_melody(text)
        mood = self.analyze_mood(melody)

        print(f"{Colors.YELLOW}🎼 NOTA ÇİZGİSİ:{Colors.END}")
        print(f"{Colors.DIM}Sol ────────────────────────────────────────────────{Colors.END}")
        staff = self.melody_to_staff(melody)
        for line in staff:
            print(f"{Colors.GREEN}{line}{Colors.END}")
        print(f"{Colors.DIM}────────────────────────────────────────────── Do{Colors.END}")

        print(f"\n{Colors.YELLOW}📊 DALGA FORMU:{Colors.END}")
        waveform = self.generate_waveform(melody)
        for line in waveform:
            print(f"{Colors.CYAN}{line}{Colors.END}")

        print(f"\n{Colors.YELLOW}🎭 MELODİ ANALİZİ:{Colors.END}")
        print(f"   Nota sayısı: {Colors.GREEN}{len([m for m in melody if m[0] != 'REST'])}{Colors.END}")
        print(f"   Sessizlik sayısı: {Colors.GREEN}{len([m for m in melody if m[0] == 'REST'])}{Colors.END}")
        print(f"   Ruh hali: {Colors.GREEN}{mood}{Colors.END}")

        # Nota dizisi göster
        print(f"\n{Colors.YELLOW}🎹 NOTA DİZİSİ:{Colors.END}")
        note_str = " ".join([f"{n}{o}" if n != 'REST' else "—" for n, o, _ in melody[:20]])
        print(f"   {Colors.PURPLE}{note_str}{'...' if len(melody) > 20 else ''}{Colors.END}")

        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🌀 MODÜL 6: DÜŞÜNCE LABİRENTİ
# ═══════════════════════════════════════════════════════════════════════════════

class ThoughtLabyrinth:
    """Sonsuz felsefi paradokslar ve düşünce deneyleri üretir"""

    def __init__(self):
        self.paradoxes = [
            {
                'name': 'Theseus\'un Gemisi',
                'question': 'Bir geminin tüm parçaları yavaş yavaş değiştirilirse, sonunda aynı gemi midir?',
                'variation': lambda x: f"Eğer {x}'ın her parçası değiştirilirse, hâlâ aynı {x} mıdır?"
            },
            {
                'name': 'Büyükbaba Paradoksu',
                'question': 'Zamanda geriye gidip büyükbabanızı engelleseniz, var olabilir miydiniz?',
                'variation': lambda x: f"Eğer {x}'ı yaratan şeyi yok etseydin, {x} var olabilir miydi?"
            },
            {
                'name': 'Omnipotans Paradoksu',
                'question': 'Her şeye gücü yeten biri, kaldıramayacağı bir taş yaratabilir mi?',
                'variation': lambda x: f"Sınırsız {x}, kendi sınırını yaratabilir mi?"
            },
            {
                'name': 'Yalancı Paradoksu',
                'question': '"Bu cümle yanlıştır" cümlesi doğru mu, yanlış mı?',
                'variation': lambda x: f"'{x} hakkındaki bu ifade yanlıştır' - doğru mu, yanlış mı?"
            },
            {
                'name': 'Schrödinger\'in Kedisi',
                'question': 'Gözlemlenmeden önce kedi hem ölü hem diri midir?',
                'variation': lambda x: f"Gözlemlenmeden önce {x} hem var hem yok mudur?"
            },
            {
                'name': 'Simülasyon Argümanı',
                'question': 'Bir simülasyonda yaşamadığımızı nasıl bilebiliriz?',
                'variation': lambda x: f"{x}'ın gerçek olduğunu nasıl kanıtlayabiliriz?"
            },
            {
                'name': 'Çin Odası',
                'question': 'Kuralları takip eden ama anlamayan bir sistem, gerçekten anlıyor mu?',
                'variation': lambda x: f"Eğer bir sistem {x}'ı mükemmel taklit ediyorsa, gerçekten {x} mıdır?"
            },
            {
                'name': 'Kelebek Etkisi',
                'question': 'Küçük bir değişiklik her şeyi değiştirebilir mi?',
                'variation': lambda x: f"Şu an {x} hakkında aldığın karar, evreni nasıl değiştirir?"
            }
        ]

        self.thought_experiments = [
            {
                'name': 'Trolley Problemi',
                'setup': 'Bir tren 5 kişiye doğru gidiyor. Bir kolu çekersen 1 kişiyi öldürür ama 5\'ini kurtarırsın.',
                'question': 'Kolu çeker misin?',
                'extension': 'Peki ya o 1 kişi sevdiğin biriyse?'
            },
            {
                'name': 'Deneyim Makinesi',
                'setup': 'Hayatının geri kalanını mükemmel mutlu hissettiren bir simülasyonda geçirebilirsin.',
                'question': 'Bağlanır mısın?',
                'extension': 'Ya zaten bağlıysan ve bunu bilmiyorsan?'
            },
            {
                'name': 'Teletransportasyon',
                'setup': 'Bir makine seni atomlarına ayırıp başka yerde yeniden oluşturuyor.',
                'question': 'Bu "sen" hâlâ sen misin?',
                'extension': 'Ya orijinal silinmezse ve iki "sen" olursa?'
            },
            {
                'name': 'Sonsuz Maymunlar',
                'setup': 'Sonsuz maymun sonsuz süre yazarsa, Shakespeare\'in tüm eserlerini yazarlar mı?',
                'question': 'Sonsuzluk tüm olasılıkları garanti eder mi?',
                'extension': 'Bu durumda yaratıcılık nedir?'
            }
        ]

        self.koans = [
            "Tek el alkış sesini duydun mu?",
            "Doğmadan önceki yüzün neydi?",
            "Bir ağaç ormanda devrilir ve kimse duymazsa, ses çıkarır mı?",
            "Bir köpek Buda doğasına sahip midir? - Mu!",
            "Rüzgar mı hareket ediyor, bayrak mı?",
            "Hiçliği düşünürken, o hiçlik bir şey midir?",
            "Arayışı bıraktığında, aradığını bulur musun?",
            "Soru cevabı içerir mi?"
        ]

    def generate_custom_paradox(self, topic: str) -> str:
        """Verilen konuya özel paradoks üret"""
        random.seed(hash(topic))
        paradox = random.choice(self.paradoxes)
        result = paradox['variation'](topic)
        random.seed()
        return result

    def infinite_regress(self, concept: str, depth: int = 5) -> List[str]:
        """Sonsuz gerileme zinciri oluştur"""
        chain = []
        current = concept

        templates = [
            "Ama {} neye dayanır?",
            "Peki {} nereden gelir?",
            "{} nasıl mümkün olur?",
            "Kim/ne {} belirler?",
            "{} olmadan ne olurdu?",
        ]

        for i in range(depth):
            question = random.choice(templates).format(current)
            chain.append(question)
            current = f"'{current}'ın temeli"

        chain.append("... ve bu sonsuza kadar devam eder.")
        return chain

    def socratic_dialogue(self, initial_claim: str, rounds: int = 4) -> List[dict]:
        """Sokratik diyalog oluştur"""
        dialogue = []
        claim = initial_claim

        questions = [
            "Bu ne anlama geliyor tam olarak?",
            "Bunu nereden biliyorsun?",
            "Her durumda geçerli mi bu?",
            "Bunun tersi de doğru olabilir mi?",
            "Bu varsayımın temeli nedir?",
            "Bir istisna düşünebilir misin?",
            "Bu sonuca nasıl ulaştın?",
            "Herkes buna katılır mı?"
        ]

        for i in range(rounds):
            dialogue.append({
                'type': 'claim' if i == 0 else 'response',
                'text': claim,
                'speaker': 'Sen' if i == 0 else 'Sen (tekrar düşünerek)'
            })

            question = random.choice(questions)
            dialogue.append({
                'type': 'question',
                'text': question,
                'speaker': 'Sokrates'
            })

            # Basit yanıt simulasyonu
            claim = f"Belki de {claim.lower()} değil, ama bir yönüyle ilgili..."

        dialogue.append({
            'type': 'conclusion',
            'text': "Görüyorsun ki, bildiğini sandığın şey aslında derin sorular barındırıyor.",
            'speaker': 'Sokrates'
        })

        return dialogue

    def explore(self, topic: str = None):
        """Düşünce labirentini keşfet"""
        clear_screen()
        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")
        print(f"{Colors.BOLD}🌀 DÜŞÜNCE LABİRENTİ{Colors.END}")
        print(f"{Colors.PURPLE}{'═' * 60}{Colors.END}\n")

        if not topic:
            print(f"{Colors.CYAN}Bir konu veya kavram girin:{Colors.END} ", end="")
            topic = input().strip() or "gerçeklik"

        print(f"\n{Colors.DIM}'{topic}' kavramı etrafında labirent oluşturuluyor...{Colors.END}\n")
        time.sleep(0.5)

        # Rastgele paradoks
        print(f"{Colors.YELLOW}🔄 KİŞİSEL PARADOKS:{Colors.END}")
        print(f"   {Colors.GREEN}{self.generate_custom_paradox(topic)}{Colors.END}\n")

        # Sonsuz gerileme
        print(f"{Colors.YELLOW}∞ SONSUZ GERİLEME:{Colors.END}")
        regress = self.infinite_regress(topic, depth=4)
        for i, step in enumerate(regress):
            indent = "   " + "  → " * min(i, 3)
            print(f"{indent}{Colors.CYAN}{step}{Colors.END}")

        # Koan
        print(f"\n{Colors.YELLOW}🧘 ZEN KOANI:{Colors.END}")
        print(f"   {Colors.PURPLE}{Colors.ITALIC}\"{random.choice(self.koans)}\"{Colors.END}\n")

        # Düşünce deneyi
        print(f"{Colors.YELLOW}🧪 DÜŞÜNCE DENEYİ:{Colors.END}")
        experiment = random.choice(self.thought_experiments)
        print(f"   {Colors.BOLD}{experiment['name']}{Colors.END}")
        print(f"   {Colors.DIM}{experiment['setup']}{Colors.END}")
        print(f"   {Colors.GREEN}→ {experiment['question']}{Colors.END}")
        print(f"   {Colors.YELLOW}→→ {experiment['extension']}{Colors.END}")

        # Klasik paradoks
        print(f"\n{Colors.YELLOW}🌊 KLASİK PARADOKS:{Colors.END}")
        classic = random.choice(self.paradoxes)
        print(f"   {Colors.BOLD}{classic['name']}{Colors.END}")
        print(f"   {Colors.GREEN}{classic['question']}{Colors.END}")

        print(f"\n{Colors.PURPLE}{'═' * 60}{Colors.END}")
        print(f"{Colors.DIM}\"Tek bildiğim, hiçbir şey bilmediğimdir.\" - Sokrates{Colors.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎮 ANA MENÜ VE UYGULAMA
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Ana banner'ı göster"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██╗  ██╗ █████╗  ██████╗ ████████╗██╗██╗  ██╗              ║
    ║   ██║ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝██║██║ ██╔╝              ║
    ║   █████╔╝ ███████║██║   ██║   ██║   ██║█████╔╝               ║
    ║   ██╔═██╗ ██╔══██║██║   ██║   ██║   ██║██╔═██╗               ║
    ║   ██║  ██╗██║  ██║╚██████╔╝   ██║   ██║██║  ██╗              ║
    ║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝╚═╝  ╚═╝              ║
    ║                                                               ║
    ║          ██████╗ ██╗   ██╗███████╗██╗     ███████╗██████╗    ║
    ║          ██╔══██╗██║   ██║██╔════╝██║     ██╔════╝██╔══██╗   ║
    ║          ██║  ██║██║   ██║███████╗██║     █████╗  ██████╔╝   ║
    ║          ██║  ██║██║   ██║╚════██║██║     ██╔══╝  ██╔══██╗   ║
    ║          ██████╔╝╚██████╔╝███████║███████╗███████╗██║  ██║   ║
    ║          ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ║
    ║                                                               ║
    ║                🌌 M A K İ N E S İ 🌌                         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(Colors.rainbow_text(banner))


def print_menu():
    """Ana menüyü göster"""
    menu = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                      MODÜLLER                                 ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║   [1] 🧬 Evrimsel ASCII Sanat                                 ║
    ║       Genetik algoritma ile benzersiz sanat eserleri üret     ║
    ║                                                               ║
    ║   [2] 🎭 Sürreal Hikaye Üreteci                               ║
    ║       Rüya gibi, absürt hikayeler oluştur                     ║
    ║                                                               ║
    ║   [3] 🎪 Emoji Hayat Simülasyonu                              ║
    ║       Conway's Game of Life - Renkli versiyon!                ║
    ║                                                               ║
    ║   [4] 🔮 Dijital Fal Bakıcısı                                 ║
    ║       Mistik analiz ve kişisel kehanetler                     ║
    ║                                                               ║
    ║   [5] 🎵 Metin Senfonisi                                      ║
    ║       Kelimelerini müziğe dönüştür                            ║
    ║                                                               ║
    ║   [6] 🌀 Düşünce Labirenti                                    ║
    ║       Felsefi paradokslar ve düşünce deneyleri                ║
    ║                                                               ║
    ║   [0] 🚪 Çıkış                                                ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(Colors.CYAN + menu + Colors.END)


def run_evolutionary_art():
    """Evrimsel sanat modülünü çalıştır"""
    clear_screen()
    print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
    print(f"{Colors.BOLD}🧬 EVRİMSEL ASCII SANAT{Colors.END}")
    print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")

    print(f"{Colors.CYAN}Sanat için bir tohum kelime girin:{Colors.END} ", end="")
    seed = input().strip() or "kaos"

    art = EvolutionaryArt(width=50, height=20)
    art.evolve(seed, generations=30, animate=True)


def run_surreal_story():
    """Sürreal hikaye modülünü çalıştır"""
    generator = SurrealStoryGenerator()
    generator.interactive_story()


def run_emoji_life():
    """Emoji hayat simülasyonunu çalıştır"""
    clear_screen()
    print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
    print(f"{Colors.BOLD}🎪 EMOJİ HAYAT SİMÜLASYONU{Colors.END}")
    print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")

    print(f"{Colors.CYAN}Tema seçin:{Colors.END}")
    themes = list(EmojiLifeSimulation.EMOJI_THEMES.keys())
    for i, theme in enumerate(themes, 1):
        print(f"  [{i}] {theme}")

    print(f"\n{Colors.CYAN}Seçiminiz (1-{len(themes)}):{Colors.END} ", end="")
    try:
        choice = int(input().strip() or "6") - 1
        theme = themes[choice] if 0 <= choice < len(themes) else 'cosmic'
    except:
        theme = 'cosmic'

    sim = EmojiLifeSimulation(width=35, height=20, theme=theme)
    sim.randomize(density=0.35)
    sim.run_simulation(max_generations=150, delay=0.12)


def run_oracle():
    """Dijital fal modülünü çalıştır"""
    clear_screen()
    print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
    print(f"{Colors.BOLD}🔮 DİJİTAL FAL BAKICISI{Colors.END}")
    print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")

    print(f"{Colors.CYAN}Sorunuzu veya merak ettiğiniz konuyu yazın:{Colors.END}")
    query = input().strip() or "hayatın anlamı"

    oracle = DigitalOracle()
    oracle.divine(query)


def run_symphony():
    """Metin senfonisi modülünü çalıştır"""
    clear_screen()
    print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
    print(f"{Colors.BOLD}🎵 METİN SENFONİSİ{Colors.END}")
    print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")

    print(f"{Colors.CYAN}Müziğe dönüştürülecek metni girin:{Colors.END}")
    text = input().strip() or "Hayat bir senfoniyse, her an bir notadır"

    symphony = TextSymphony()
    symphony.visualize(text)


def run_labyrinth():
    """Düşünce labirenti modülünü çalıştır"""
    labyrinth = ThoughtLabyrinth()
    labyrinth.explore()


def main():
    """Ana uygulama döngüsü"""
    while True:
        clear_screen()
        print_banner()
        print_menu()

        print(f"{Colors.YELLOW}Seçiminiz:{Colors.END} ", end="")

        try:
            choice = input().strip()

            if choice == '1':
                run_evolutionary_art()
            elif choice == '2':
                run_surreal_story()
            elif choice == '3':
                run_emoji_life()
            elif choice == '4':
                run_oracle()
            elif choice == '5':
                run_symphony()
            elif choice == '6':
                run_labyrinth()
            elif choice == '0':
                clear_screen()
                print(f"\n{Colors.PURPLE}{'═' * 50}{Colors.END}")
                slow_print(Colors.rainbow_text("   Kaotik Düşler Makinesi kapanıyor..."))
                print(f"\n   {Colors.ITALIC}\"Her son yeni bir başlangıçtır.\"{Colors.END}")
                print(f"{Colors.PURPLE}{'═' * 50}{Colors.END}\n")
                break
            else:
                print(f"\n{Colors.RED}Geçersiz seçim. Tekrar deneyin.{Colors.END}")
                time.sleep(1)
                continue

            print(f"\n{Colors.DIM}Devam etmek için Enter'a basın...{Colors.END}")
            input()

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Kaotik Düşler Makinesi kapatılıyor...{Colors.END}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Bir hata oluştu: {e}{Colors.END}")
            time.sleep(2)


if __name__ == "__main__":
    main()

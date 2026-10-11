import heapq

# ==========================================
# 1. EXPERT SYSTEM (Sistem Pakar Diagnosis)
# ==========================================
class ExpertSystem:
    def __init__(self):
        # Basis Pengetahuan (Knowledge Base): Aturan diagnosis
        self.rules = [
            {
                "conditions": {"daya_nyala": False, "indikator_led": False},
                "diagnosis": "Kerusakan pada Adapter Power Supply atau Kabel Utama.",
                "action": "Ganti adapter atau cek stopkontak listrik."
            },
            {
                "conditions": {"daya_nyala": True, "layar_tampil": False, "bunyi_beep": True},
                "diagnosis": "Kerusakan/Ketidakcocokan pada Memory RAM.",
                "action": "Lepas, bersihkan kuningan RAM dengan penghapus, lalu pasang kembali."
            },
            {
                "conditions": {"daya_nyala": True, "suhu_panas": True, "kipas_berisik": True},
                "diagnosis": "Overheating akibat Thermal Paste kering atau Ventilasi Tersumbat.",
                "action": "Bersihkan debu kipas dan ganti thermal paste pada processor."
            },
            {
                "conditions": {"daya_nyala": True, "layar_tampil": True, "sistem_lambat": True},
                "diagnosis": "Kesehatan Storage (HDD/SSD) Menurun atau Kapasitas Penuh.",
                "action": "Lakukan defragmentasi, cek Health SSD dengan tools, atau upgrade ke SSD."
            }
        ]

    def diagnose(self, user_facts):
        for rule in self.rules:
            match = True
            for fact, value in rule["conditions"].items():
                if user_facts.get(fact) != value:
                    match = False
                    break
            if match:
                return rule["diagnosis"], rule["action"]
        return "Diagnosis tidak ditemukan.", "Konsultasikan ke teknisi terdekat."


# ==========================================
# 2. SEARCH ALGORITHM (BFS, DFS, & A*)
# ==========================================
class GridSearch:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Atas, Bawah, Kiri, Kanan
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                neighbors.append((nr, nc))
        return neighbors

    def bfs(self, start, goal):
        """Breadth-First Search"""
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            (curr, path) = queue.pop(0)
            if curr == goal:
                return path
            for neighbor in self.get_neighbors(curr):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def dfs(self, start, goal):
        """Depth-First Search"""
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            (curr, path) = stack.pop()
            if curr == goal:
                return path
            if curr not in visited:
                visited.add(curr)
                for neighbor in self.get_neighbors(curr):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
        return None

    def a_star(self, start, goal):
        """A* Search Algorithm dengan Heuristik Manhattan Distance"""
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        pq = [(0, start, [start])]
        g_score = {start: 0}

        while pq:
            cost, curr, path = heapq.heappop(pq)
            if curr == goal:
                return path

            for neighbor in self.get_neighbors(curr):
                tentative_g = g_score[curr] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(pq, (f_score, neighbor, path + [neighbor]))
        return None


# ==========================================
# PROGRAM UTAMA (CLI INTERFACE)
# ==========================================
def main():
    print("==========================================")
    print(" DEMO: EXPERT SYSTEM & SEARCH ALGORITHMS  ")
    print("==========================================")
    print("1. Expert System (Diagnosis Kerusakan Hardware)")
    print("2. Search Algorithm (BFS, DFS, A* Pathfinding)")
    
    choice = input("\nPilih menu (1/2): ").strip()
    
    if choice == "1":
        print("\n--- EXPERT SYSTEM ---")
        es = ExpertSystem()
        facts = {
            "daya_nyala": input("Apakah perangkat menyala? (y/n): ").lower() == 'y',
            "indikator_led": input("Apakah indikator LED menyala? (y/n): ").lower() == 'y',
            "layar_tampil": input("Apakah layar menampilkan gambar? (y/n): ").lower() == 'y',
            "bunyi_beep": input("Apakah ada bunyi beep berulang? (y/n): ").lower() == 'y',
            "suhu_panas": input("Apakah perangkat terasa sangat panas? (y/n): ").lower() == 'y',
            "kipas_berisik": input("Apakah kipas berputar kencang/berisik? (y/n): ").lower() == 'y',
            "sistem_lambat": input("Apakah sistem operasi sangat lambat? (y/n): ").lower() == 'y'
        }
        diag, act = es.diagnose(facts)
        print(f"\nHasil Diagnosis : {diag}")
        print(f"Tindakan Solusi : {act}")

    elif choice == "2":
        print("\n--- SEARCH ALGORITHM (GRID 5x5) ---")
        # 0 = Jalan, 1 = Tembok/Rintangan
        grid = [
            [0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        start = (0, 0)
        goal = (4, 4)
        
        searcher = GridSearch(grid)
        
        print(f"Titik Awal: {start} -> Titik Tujuan: {goal}\n")
        print("Lintasan BFS   :", searcher.bfs(start, goal))
        print("Lintasan DFS   :", searcher.dfs(start, goal))
        print("Lintasan A*    :", searcher.a_star(start, goal))

    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()

"""
Scraper Hadis Berkaitan Matematika
API: api.myquran.com/v3
Endpoint: GET /hadis/enc/cari/{keyword}?page={page}

Jalankan dari komputer lokal:
    pip install requests
    python scrape_hadis_matematika.py

Output: hadis_matematika.csv
"""

import requests
import csv
import time
import os

BASE_URL = "https://api.myquran.com/v3"

KEYWORDS = [
    "hitung",
    "bilangan",
    "angka",
    "jumlah",
    "timbangan",
    "ukuran",
    "separuh",
    "setengah",
    "sepertiga",
    "dua pertiga",
    "zakat",
    "warisan",
    "waris",
    "nisab",
]

OUTPUT_FILE = "hadis_matematika_1.csv"

FIELDNAMES = [
    "keyword_pencarian",
    "id",
    "teks_indonesia",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_all_pages(keyword: str) -> list:
    """Ambil semua halaman hasil pencarian untuk satu keyword."""
    all_hadis = []
    page = 1

    while True:
        url = f"{BASE_URL}/hadis/enc/cari/{keyword}?page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)

            # Tangani rate limit: tunggu lalu coba lagi
            if resp.status_code == 429:
                print(f"\n   [Rate Limit] Tunggu 10 detik...", end="")
                time.sleep(10)
                continue

            resp.raise_for_status()
            body = resp.json()

            data   = body.get("data", {})
            paging = data.get("paging", {})
            hadis  = data.get("hadis", [])   # ← key yang benar

            all_hadis.extend(hadis)

            total_pages = paging.get("total_pages", 1)
            has_next    = paging.get("has_next", False)

            print(f"\r   halaman {page}/{total_pages} — terkumpul {len(all_hadis)} hadis", end="", flush=True)

            if not has_next:
                print()  # newline setelah selesai
                break

            page += 1
            time.sleep(1.0)   # jeda lebih lama untuk hindari rate limit

        except requests.exceptions.HTTPError as e:
            print(f"\n   [HTTP ERROR] {e}")
            break
        except Exception as e:
            print(f"\n   [ERROR] {e}")
            break

    return all_hadis


def main():
    all_rows = []
    seen_ids: set = set()   # cegah duplikat berdasarkan id hadis

    print("=" * 60)
    print("  Scraper Hadis Matematika — api.myquran.com v3")
    print("=" * 60)
    print(f"  Total keyword: {len(KEYWORDS)}")
    print("-" * 60)

    for kw in KEYWORDS:
        print(f"\n🔍 Keyword: '{kw}'")
        hadis_list = fetch_all_pages(kw)
        new = 0

        for item in hadis_list:
            uid = str(item.get("id", ""))
            if uid in seen_ids:
                continue
            seen_ids.add(uid)
            new += 1

            all_rows.append({
                "keyword_pencarian": kw,
                "id":                item.get("id", ""),
                "teks_indonesia":    item.get("text", ""),
            })

        print(f"   ✔ {len(hadis_list)} ditemukan, {new} baru (tidak duplikat)")
        time.sleep(1.5)   # jeda antar keyword

    # ── Simpan CSV ──────────────────────────────────────────
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(all_rows)

    print("\n" + "=" * 60)
    print(f"✅ Selesai! {len(all_rows)} hadis unik tersimpan di:")
    print(f"   📄 {os.path.abspath(OUTPUT_FILE)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

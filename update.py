from queue_utils import ISO_URLS, fetch_xls, normalize, insert_to_db, init_db

def main():
    init_db()
    for iso, url in ISO_URLS.items():
        try:
            df = fetch_xls(url, iso)
            df_norm = normalize(df)
            insert_to_db(df_norm)
            print(f"✅ Updated {iso}")
        except Exception as e:
            print(f"❌ Failed {iso}: {e}")

if __name__ == '__main__':
    main()

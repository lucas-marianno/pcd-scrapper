from src.pcd_scrapper import PcdScrapper, ScriptConfig

if __name__ == "__main__":
    script_config = ScriptConfig("config.yaml")
    scrapper = PcdScrapper(script_config)

    scrapper.start_scraping()

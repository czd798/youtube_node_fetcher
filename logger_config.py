import logging

def setup_logger(log_file: str = "youtube_video_info.log") -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def log_info(message: str) -> None:
    logging.info(message)


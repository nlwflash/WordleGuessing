import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from source_code.utility.constant.paths import Paths
from source_code.infrastructure.data_set_handler import DataSetHandler
from source_code.domain.word_filtering_service import WordFilteringService
from time import time

from source_code.presentation.view import View
from source_code.application.controller import Controller

def main():
    start = time()
    data_set = DataSetHandler(Paths.WORDS_FILE, Paths.DATA_SET_CACHE, Paths.METADATA_CACHE, True).get_data_set()
    print(f"Data set loaded in {time() - start:.2f} seconds.")
    
    word_filtering_service = WordFilteringService(data_set)
    view = View(on_submit_callback=None)
    backend_callback = word_filtering_service.get_available_words
    controller = Controller(view, backend_callback) # type: ignore
    view.run()

if __name__ == "__main__":
    main()
from collections import defaultdict
from source_code.utility.constant.color import Color
from source_code.utility.constant.types import DataSet
from source_code.infrastructure.data_set_builder import DataSetBuilder
from source_code.utility.helper.io_wrapper import IOWrapper

class DataSetHandler():
    def __init__(self, word_list_path: str, cache_path: str, metadata_path: str, force_build: bool = False):
        resolved_word_list_path = IOWrapper().ensure_existence(word_list_path)
        if not resolved_word_list_path:
            raise FileNotFoundError(f"Word list file does not exist: {word_list_path}")

        self.word_list_path = resolved_word_list_path
        self.cache_path = cache_path
        self.metadata_path = metadata_path
        self.force_build = force_build

    def get_data_set(self) -> DataSet:
        if self.__validate_cached_data_set():
            print("Cache was validated")
            return self.__retrieve_cached_data_set()
        
        else:
            print("Cache was invalid")
            return self.__create_data_set()

    def __validate_cached_data_set(self) -> bool:
        if self.force_build or not (
            self.metadata_path and self.cache_path
        ):
            return False
        
        try:
            self.actual_metadata = IOWrapper().get_metadata_from_file(self.word_list_path)
            return  self.actual_metadata <= IOWrapper().read_as_float(self.metadata_path)          
          
        except:
            return False
        
    def __retrieve_cached_data_set(self) -> DataSet:
        try:
            cached_file_content = IOWrapper().load_pickle(self.cache_path)
            if self.__is_valid_data_set(cached_file_content):
                return cached_file_content
            
        except Exception:
            pass # Absorb exception and make new data set
        
        print("Content loaded from pickle file was not of DataSet type")
        print("Creating new DataSet")
        return self.__create_data_set()
    
    def __create_data_set(self) -> DataSet:
        data_set = DataSetBuilder(IOWrapper().read_from_file(self.word_list_path)).build()
        if data_set:
            self.__save_to_cache(data_set)
            return data_set
        
        raise Exception("Critical Error: Unable to create DataSet")

    def __save_to_cache(self, data_set: DataSet) -> None:
        IOWrapper().save_pickle(self.cache_path, data_set)
        IOWrapper().write_to_file(self.metadata_path, str(IOWrapper().get_metadata_from_file(self.word_list_path)))

    def __is_valid_data_set(self, data_set: object) -> bool:
        if not isinstance(data_set, defaultdict):
            return False

        for color in Color:
            index = data_set.get(color)
            if not isinstance(index, defaultdict):
                return False

            for raw_key, words in index.items():
                if not isinstance(raw_key, tuple) or len(raw_key) != 2:
                    return False

                letter, position = raw_key
                if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha():
                    return False

                if not isinstance(position, int) or position not in range(5):
                    return False

                if not isinstance(words, set) or not all(isinstance(word, str) for word in words):
                    return False

        return True

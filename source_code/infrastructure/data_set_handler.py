from collections import defaultdict
from source_code.utility.constant.types import DataSet
from source_code.infrastructure.data_set_builder import DataSetBuilder
from source_code.utility.helper.io_wrapper import IOWrapper

class DataSetHandler():
    def __init__(self, word_list_path: str, cache_path: str, metadata_path: str, force_build: bool = False):
        self.word_list_path = IOWrapper().ensure_existence(word_list_path)
        self.cache_path = cache_path
        self.metadata_path = metadata_path
        self.force_build = force_build

    def get_data_set(self):
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
            if isinstance(cached_file_content, defaultdict):
                return cached_file_content
            
        except:
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
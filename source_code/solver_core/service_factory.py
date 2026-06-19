from source_code.domain.word_filtering_service import WordFilteringService
from source_code.infrastructure.data_set_handler import DataSetHandler, WordListSource
from source_code.utility.helper.app_paths import AppPaths


def create_word_filtering_service(word_list_source: WordListSource) -> WordFilteringService:
    return WordFilteringService(DataSetHandler(word_list_source).get_data_set())


def create_default_word_filtering_service(app_paths: AppPaths | None = None) -> WordFilteringService:
    resolved_paths = app_paths or AppPaths()
    return create_word_filtering_service(resolved_paths.word_list_resource)

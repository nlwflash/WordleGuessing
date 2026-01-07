from collections import defaultdict
from source_code.utility.constant.color import Color
from source_code.utility.constant.types import DataSet
from typing import Final


TEST_DATA_SET: Final[DataSet] = defaultdict(
        lambda: defaultdict(set),
        {
            Color.GRAY: defaultdict(set, {
                ("a", 0): {"word1", "otherword1"},
                ("a", 1): {"word2", "otherword2"},
                ("a", 2): {"word3", "otherword3"},
                ("a", 3): {"word4", "otherword4"},
                ("a", 4): {"word5", "otherword5"}
            }),
            Color.GREEN: defaultdict(set, {
                ("a", 0): {"word", "otherword"},
                ("a", 1): {"word", "otherword"},
                ("a", 2): {"word", "otherword"},
                ("a", 3): {"word", "otherword"},
                ("a", 4): {"word", "otherword"}
            }),
            Color.YELLOW: defaultdict(set, {
                ("a", 0): {"word", "otherword"},
                ("a", 1): {"word", "otherword"},
                ("a", 2): {"word", "otherword"},
                ("a", 3): {"word", "otherword"},
                ("a", 4): {"word", "otherword"}
            }),
        }
    )
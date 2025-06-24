from collections import defaultdict
from source_code.utility.constant.color import Color
from source_code.utility.constant.types import DataSet
from typing import Final


TEST_DATA_SET: Final[DataSet] = defaultdict(
        lambda: defaultdict(set),
        {
            Color.GRAY: defaultdict(set, {
                ("a", 0): {"word", "otherword"},
                ("a", 1): {"word", "otherword"},
                ("a", 2): {"word", "otherword"},
                ("a", 3): {"word", "otherword"},
                ("a", 4): {"word", "otherword"}
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
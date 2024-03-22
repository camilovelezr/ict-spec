
from pathlib import Path
from ict import ICT
import pytest 

files = [
"https://raw.githubusercontent.com/PolusAI/image-tools/master/regression/theia-bleedthrough-estimation-tool/plugin.json"
]

@pytest.mark.parametrize("wipp_spec", files)
def test_load_and_save_remote_wipp_spec(wipp_spec: str) -> None:

    ict1 = ICT.from_wipp(wipp_spec)
    ict1.save_yaml(Path.cwd()  / "tmp" / "ict1.yaml")
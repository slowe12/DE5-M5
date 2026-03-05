from pathlib import Path
from datetime import datetime

out = Path("data/hello.txt")

with out.open("w") as f:
    f.write(f"Hello to the docker volume! ({datetime.now()})\n")

    print("print this file")
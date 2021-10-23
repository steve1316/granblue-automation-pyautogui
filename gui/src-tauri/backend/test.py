import time
import sys

tries = 30
while tries > 0:
    tries -= 1
    sys.stdout.write("\n")
    sys.stdout.write(f"Test {tries}")
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write(f"\n")
sys.stdout.write(f"Test ended")
sys.stdout.flush()
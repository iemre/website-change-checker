import glob
import imageio
import sys
from PIL import Image

def run(*, dir, l, t, r, b):
    diff_threshold = 0.01  # difference in percentage from previous screenshot

    # crop images for regions of interest
    for new_fpath in glob.glob(f"{dir}/*.png"):
        with Image.open(new_fpath) as im:
            im.crop((l, t, r, b)).save(new_fpath)
    for new_fpath in glob.glob(f"{dir}/*.png"):
        new_fname = new_fpath.split("/")[1]
        old_im = imageio.imread(f"{dir}_old/{new_fname}")
        new_im = imageio.imread(new_fpath)
        diff_count = 0
        old_bytes = old_im.tobytes()
        new_bytes = new_im.tobytes()
        total_bytes = len(old_bytes)
        for i in range(total_bytes):
            if old_bytes[i] != new_bytes[i]:
                diff_count += 1
        diff_pct = diff_count / total_bytes
        # based on trial & error, 3% seems like a good value for a true positive
        if diff_pct > diff_threshold:
            print(f"* {new_fname} different ({diff_pct}) image")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("required directory name for the screenshots")
    run(dir=sys.argv[1], l=int(sys.argv[2]), t=int(sys.argv[3]), r=int(sys.argv[4]), b=int(sys.argv[5]))


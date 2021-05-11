import glob
import imageio

result = ""

diff_threshold = 0.01  # difference in percentage from previous screenshot

for new_fpath in glob.glob("screenshots/*.png"):
    new_fname = new_fpath.split("/")[1]
    old_im = imageio.imread(f"oldscreenshots/{new_fname}")
    new_im = imageio.imread(new_fpath)
    diff_count = 0
    offset_x = 100  # no of pixels we're ignoring from the top
    offset_y = 100  # no of pixels we're ignoring from the left

    # special case for Amazon
    if "amazon" in new_fname:
        # use the 80% of the page after the initial 20% if Amazon
        # as there are some changing banners at the top that would
        # otherwise give us false positives
        offset_x = int(len(old_im.tobytes())*20/100)
        diff_threshold = 0.13

    old_bytes = old_im.tobytes()[offset_x:][offset_y:]
    new_bytes = new_im.tobytes()[offset_x:][offset_y:]
    total_bytes = len(old_bytes)
    for i in range(total_bytes):
        if old_bytes[i] != new_bytes[i]:
            diff_count += 1
    diff_pct = diff_count / total_bytes
    # based on trial & error, 3% seems like a good value for a true positive
    if diff_pct > diff_threshold:
        print(f"* {new_fname} different ({diff_pct}) image")
        break


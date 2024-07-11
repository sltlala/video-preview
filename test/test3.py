skip = 90
duration = 1260
screenshot_list = []
num = 20 + 1
if not skip:
    parts = [duration / num] * num
else:
    parts = [duration - 180 / num] * num

for i, part in enumerate(parts):
    if i == 0:
        continue

    if not skip:
        screenshot_list.append(round(part * i, 3))
    else:
        if part * i < skip:
            screenshot_list.append(round(part * i, 3))
        else:
            screenshot_list.append(round(part * i+90, 3))

print(screenshot_list)
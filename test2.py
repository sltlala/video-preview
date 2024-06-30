import datetime

def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"

time = 502.347
# print(str(datetime.time(time)))
print(convert_seconds(time))

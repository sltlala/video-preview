import datetime

def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"

time = 502.347
# print(str(datetime.time(time)))
print(convert_seconds(time))

def calculate_segments(total_duration, skip_time, skip_duration, segments):
    # Total effective duration without the skipped duration
    effective_duration = total_duration - skip_duration

    # Length of each segment without considering the skipped duration
    segment_length = effective_duration / segments

    time_points = []
    current_time = 0
    for i in range(segments + 1):
        if current_time < skip_time:
            time_points.append(current_time)
        else:
            time_points.append(current_time + skip_duration)

        current_time += segment_length

    return time_points

# Example usage
total_duration = 1260  # Total duration of the video in seconds (21 minutes for example)
skip_time = 600  # The time node to skip 90 seconds (10 minutes)
skip_duration = 90  # Duration to skip in seconds
segments = 21  # Number of segments

time_points = calculate_segments(total_duration, skip_time, skip_duration, segments)
for i, time_point in enumerate(time_points):
    print(f"Segment {i}: {time_point} seconds")


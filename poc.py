#Nathan Touati
import uuid
import sys
from datetime import datetime, timedelta

# Constant for UUID datetime origin (1582-10-15)
UUID1_DATETIME_ORIGIN = 0x01b21dd213814000

def uuid1_time(uuid1):
    timestamp = uuid1.time - UUID1_DATETIME_ORIGIN
    return datetime(1582, 10, 15) + timedelta(microseconds=timestamp//10)

def uuid1_real_time(uuid1):
    timestamp = uuid1.time - UUID1_DATETIME_ORIGIN
    return datetime(1970, 1, 1) + timedelta(microseconds=timestamp//10)

def uuid1_from_time(node, clock_seq, time):
    time_low = time & 0xffffffff
    time_mid = (time >> 32) & 0xffff
    time_hi_version = ((time >> 48) & 0x0fff) | 0x1000  # Set the version to 1
    clock_seq_low = clock_seq & 0xff
    clock_seq_hi_variant = ((clock_seq >> 8) & 0x3f) | 0x80  # Set the variant to 1
    return uuid.UUID(fields=(time_low, time_mid, time_hi_version,
                             clock_seq_hi_variant, clock_seq_low, node))

def generate_uuids_between(uuid1, uuid2, filename):
    time1 = (uuid1.time - UUID1_DATETIME_ORIGIN) // 10
    time2 = (uuid2.time - UUID1_DATETIME_ORIGIN) // 10

    if time2 <= time1:
        raise ValueError("Second UUID must have a later timestamp than the first UUID")

    with open(filename, 'w') as f:
        # Generate an UUID every second instead of every microsecond
        for fake_timestamp in range(time1, time2, 1):
            generated_uuid = uuid1_from_time(uuid1.node, uuid1.clock_seq, fake_timestamp * 10 + UUID1_DATETIME_ORIGIN)
            f.write(str(generated_uuid) + '\n')

# Check if we have enough command line arguments
if len(sys.argv) < 3:
    print("Usage: python script.py <UUID1> <UUID2>")
    sys.exit(1)

# Parse the UUIDs from the command line arguments
uuid1 = uuid.UUID(sys.argv[1])
uuid2 = uuid.UUID(sys.argv[2])

print(f"Date and time for UUID1: {uuid1_real_time(uuid1)}")
print(f"Date and time for UUID2: {uuid1_real_time(uuid2)}")

generate_uuids_between(uuid1, uuid2, 'generated_uuids.txt')

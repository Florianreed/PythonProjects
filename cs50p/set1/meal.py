def main():
    t = input("What time is it?")
    t0 = convert(t)
    if 7 <= t0 <= 8:
        print("breakfast time")
    
def convert(time):
    hours, minutes = time.split(":")
    return int(hours) + float(int(minutes) / 60)
if __name__ == "__main__":
    main()
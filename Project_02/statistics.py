import GameManager_3
import time

def main2():
    results = []
    f = open("statistics.txt", "w")  # opens file with name of "test.txt"

    for i in range(10):
        results.append(GameManager_3.play())

        scores = " ".join(str(x) for x in results)
        f.write(scores)
        f.write("\n\n")
        avg = sum(results)/len(results)
    f.write("Average: ")
    f.write(avg)

    print("Results:")
    for score in results:
        print(score)
    print("Average: ", avg)

    f.close()
    time.sleep(999999)

def main():
    results = []
    f = open("optimization.txt", "w")  # opens file with name of "test.txt"

    for i in range(2):
        results.append(GameManager_3.play())

        scores = " ".join(str(x) for x in results)
        f.write(scores)
        f.write("\n\n")
        avg = sum(results)/len(results)
    f.write("Average: ")
    f.write(str(avg))

    print("Results:")
    for score in results:
        print(score)
    print("Average: ", avg)

    f.close()
    time.sleep(999999)

if __name__ == '__main__':
    main()
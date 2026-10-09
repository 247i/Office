# import

def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    with open("combined.lng", "w") as tar:
        with open("new22.txt", "r") as r_f, open("Tamil11.lng", "r") as l_f:
            for d in l_f.readlines():
                data = d.rstrip() + r_f.readline()
                tar.write(data)

if __name__ == '__main__':
    print_hi()

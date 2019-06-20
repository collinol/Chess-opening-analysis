import datetime
import time


class FileTrie:
    def __init__(self):
        self.root = Node("")

    def add(self, filename):
        filename = filename.replace(".html", "")
        if not self.lookup(filename):
            curr = self.root
            for char in filename.split("_")[0]:
                if char not in curr.child:
                    curr.child[char] = Node(char)
                curr = curr.child[char]
            filetime = datetime.datetime.strptime(filename.split("_")[1].replace("-", " "), "%Y %m %d %H:%M:%S.%f")
            curr.time = Node(char=None, time=filetime)

    def lookup(self, filename):
        curr = self.root
        user = self.root.char
        for char in filename.split("_")[0]:
            if char in curr.child:
                curr = curr.child[char]
                user += curr.char
            else:
                return False
        return {"user":user+"_"+str(curr.time.time).replace(" ", "-")+".html", "last_updated":curr.time.time}


class Node:
    def __init__(self, char, time=None):
        self.char = char
        self.child = {}
        self.time = time


if __name__ == '__main__':
    f = FileTrie()
    f.add("GetSchwifty10_2019-06-20-13:40:38.534648")
    f.add("User1_"+str(datetime.datetime.now()).replace(" ","-"))
    time.sleep(3)
    f.add("User2_"+str(datetime.datetime.now()).replace(" ","-"))
    print(f.lookup("GetSchwifty10_2019-06-20-13:40:38.534648"))
    print(f.lookup("User1_"+str(datetime.datetime.now()).replace(" ","-")))
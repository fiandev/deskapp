from lib.Socialist import Socialist

if __name__ == '__main__':
    url = input("post url: ")
    socialist = Socialist("./test/results")
    socialist.download(url)
import sys

from borb.pdf import Document


def main():
    if len(sys.argv) < 2:
        print("usage: python note")
        raise Exception("please provide music file!")

    # create an empty Document
    pdf = Document()
    print(dir(pdf))
    print(f"hello_borb_doc={pdf}")


if __name__ == "__main__":
    main()

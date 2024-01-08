class Book:
    def __init__(self,BookName):
        self.Bookname = BookName
        self.readBook()
    
    def readBook(self):
        with open(f'{self.Bookname}', 'r') as file:
            BookInLines = file.readlines()
        return BookInLines
    def getbookframe(self, start_line, end_line):
        bookframe = ''.join(self.readBook()[start_line:end_line])
        return bookframe
        





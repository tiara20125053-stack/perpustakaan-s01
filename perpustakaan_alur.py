"""
Sistem Alur Perpustakaan (setara alur Simple Banking pada S01)

Banking : Create Account -> Deposit -> Withdraw -> Check balance -> Close
Library : Create Book/Member -> Borrow -> Return -> Check status -> Retire

Entity     : Book, Member
Identity   : book_id, member_id
State      : Book.status, Member.borrowed
Behavior   : borrow(), give_back(), retire()
Belum perlu: inheritance, database, UI, framework.
"""


class Book:
    """Responsibility: menyimpan identitas buku dan status ketersediaannya."""

    def __init__(self, book_id, title):
        self.book_id = book_id          # IDENTITY
        self.title = title
        self.status = "available"       # STATE: available | borrowed | retired

    def borrow(self):
        if self.status != "available":
            print(f"  ! Gagal: '{self.title}' tidak bisa dipinjam ({self.status})")
            return False
        self.status = "borrowed"
        return True

    def give_back(self):
        if self.status != "borrowed":
            print(f"  ! Gagal: '{self.title}' tidak sedang dipinjam")
            return False
        self.status = "available"
        return True

    def retire(self):
        if self.status == "borrowed":
            print(f"  ! Gagal: '{self.title}' masih dipinjam, belum bisa ditarik")
            return False
        self.status = "retired"
        return True

    def __str__(self):
        return f"{self.book_id} | {self.title} | {self.status}"


class Member:
    """Responsibility: menyimpan identitas anggota dan buku yang sedang dipinjam."""

    MAX_LOAN = 2

    def __init__(self, member_id, name):
        self.member_id = member_id      # IDENTITY
        self.name = name
        self.borrowed = []              # STATE: daftar Book yang dipinjam

    def borrow_book(self, book):
        if len(self.borrowed) >= self.MAX_LOAN:
            print(f"  ! Gagal: {self.name} sudah meminjam {self.MAX_LOAN} buku")
            return False
        if book.borrow():
            self.borrowed.append(book)
            return True
        return False

    def return_book(self, book):
        if book not in self.borrowed:
            print(f"  ! Gagal: {self.name} tidak meminjam '{book.title}'")
            return False
        if book.give_back():
            self.borrowed.remove(book)
            return True
        return False

    def __str__(self):
        titles = [b.title for b in self.borrowed] or "-"
        return f"{self.member_id} | {self.name} | dipinjam: {titles}"


def langkah(nomor, teks):
    print(f"\n[{nomor}] {teks}")


if __name__ == "__main__":
    # 1. CREATE (setara Create Account)
    langkah(1, "Create: buat 2 buku dan 2 anggota")
    b1 = Book("B001", "Clean Code")
    b2 = Book("B002", "Python Crash Course")
    alya = Member("M001", "Alya")
    bima = Member("M002", "Bima")
    print(b1)
    print(b2)
    print(alya)
    print(bima)

    # 2. BORROW (setara Withdraw: mengurangi ketersediaan)
    langkah(2, "Borrow: Alya meminjam Clean Code")
    alya.borrow_book(b1)
    print(b1)
    print(alya)

    langkah(2, "Borrow: Bima mencoba meminjam buku yang sama (harus ditolak)")
    bima.borrow_book(b1)

    # 3. RETURN (setara Deposit: mengembalikan ketersediaan)
    langkah(3, "Return: Alya mengembalikan Clean Code")
    alya.return_book(b1)
    print(b1)

    langkah(3, "Return: Bima mencoba mengembalikan buku yang tidak ia pinjam")
    bima.return_book(b1)

    # 4. CHECK STATUS (setara Check balance)
    langkah(4, "Check status: semua buku dan anggota")
    bima.borrow_book(b1)
    for item in (b1, b2, alya, bima):
        print(item)

    # 5. RETIRE (setara Close Account)
    langkah(5, "Retire: tarik buku dari koleksi")
    print("Coba tarik buku yang sedang dipinjam:")
    b1.retire()
    print("Tarik buku yang tersedia:")
    b2.retire()
    print(b2)

    langkah(5, "Borrow buku yang sudah retired (harus ditolak)")
    alya.borrow_book(b2)

    # Bukti: dua object dari class sama, state terpisah
    langkah("*", "Bukti: state antar object terpisah")
    print("b1 =", b1.status, "| b2 =", b2.status)

-- USE petHotel;
CREATE TABLE guests(
guestID INT PRIMARY KEY AUTO_INCREMENT,
guestName VARCHAR(20),
guestPhone VARCHAR(20),
guestEmail VARCHAR(100)
);

CREATE TABLE bookings(
bookingID INT PRIMARY KEY AUTO_INCREMENT,
checkInDate DATE,
checkOutDate DATE,
numberOfGuest INT,
numberOfpet INT,
guestID INT,
roomID INT,
FOREIGN KEY (guestID) REFERENCES guests(guestID)
);

CREATE TABLE rooms(
roomID INT PRIMARY KEY AUTO_INCREMENT,
roomtype VARCHAR(50),
roomMaxGuest INT,
roomMaxPet INT,
bookingID INT,
FOREIGN KEY (bookingID) REFERENCES bookings(bookingID)
);

CREATE TABLE services( 
serviceID INT PRIMARY KEY AUTO_INCREMENT,
showerService BOOLEAN DEFAULT False,
haircutService BOOLEAN DEFAULT False,
roomService BOOLEAN DEFAULT False,
bookingID INT,
FOREIGN KEY (bookingID) REFERENCES bookings(bookingID)
);

CREATE TABLE payments(
paymentID INT PRIMARY KEY AUTO_INCREMENT,
payway ENUM ('card','cash'),
amount INT,
bookingID INT,
FOREIGN KEY (bookingID) REFERENCES bookings(bookingID)
);

-- 예약내역 조회하기
SELECT g.guestName, 
b.checkInDate,b.checkOutDate,b.numberOfGuest,b.numberOfPet,
r.roomType,
s.showerService,s.haircutService,s.roomService,
p.payway,p.amount
FROM guests g 
JOIN bookings b ON g.guestID = b.guestID
JOIN rooms r ON b.bookingID = r.bookingID
JOIN services s ON b.bookingID = s.bookingID
JOIN payments p ON b.bookingID = p.bookingID
ORDER BY g.guestName;

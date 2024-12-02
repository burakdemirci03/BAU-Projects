from mysql import connector

my_connection = connector.connect(
    host="localhost",
    user="root",
    password="########")

my_cursor = my_connection.cursor(buffered=True)

my_cursor.execute("DROP DATABASE banking")

my_cursor.execute("CREATE DATABASE IF NOT EXISTS banking")
my_cursor.execute("USE banking")

# 1)
my_cursor.execute("""
CREATE TABLE IF NOT EXISTS doctor(
    dr_code int AUTO_INCREMENT,
    name varchar(32),
    fname varchar(32),
    gender varchar(16),
    address text,
    designation varchar(32),
    PRIMARY KEY (dr_code)
) ENGINE=InnoDB;
""")
my_cursor.execute("ALTER TABLE doctor AUTO_INCREMENT=10;")

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS patient(
    pat_id int AUTO_INCREMENT,
    name varchar(32),
    fname varchar(32),
    gender varchar(16),
    address text,
    tel_num varchar(15),
    dr_code int,
    PRIMARY KEY (pat_id),
    FOREIGN KEY (dr_code) REFERENCES doctor(dr_code)
) ENGINE=InnoDB;
""")
my_cursor.execute("ALTER TABLE patient AUTO_INCREMENT=1000;")

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS staff(
    staf_id int AUTO_INCREMENT,
    name varchar(64),
    dept varchar(64),
    address text,
    cell_num varchar(15),
    dr_code int,
    PRIMARY KEY (staf_id),
    FOREIGN KEY (dr_code) REFERENCES doctor(dr_code)
) ENGINE=InnoDB;
""")
my_cursor.execute("ALTER TABLE staff AUTO_INCREMENT=100;")

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_diagnosis(
    diag_no int AUTO_INCREMENT,
    diag_detail varchar(64),
    remark text,
    diag_date timestamp,
    other text,
    pat_id int,
    PRIMARY KEY (diag_no),
    FOREIGN KEY (pat_id) REFERENCES patient(pat_id)
) ENGINE=InnoDB;
""")
my_cursor.execute("ALTER TABLE patient_diagnosis AUTO_INCREMENT=1;")

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS bill(
    bill_no int AUTO_INCREMENT,
    pat_name varchar(64),
    dr_name varchar(64),
    datetime timestamp,
    amount float(6,2),
    pat_id int,
    PRIMARY KEY (bill_no),
    FOREIGN KEY (pat_id) REFERENCES patient(pat_id)
) ENGINE=InnoDB;
""")
my_cursor.execute("ALTER TABLE bill AUTO_INCREMENT=1;")

my_cursor.execute("USE banking")

# 2)
my_cursor.execute("""
INSERT INTO doctor (name, fname, gender, address, designation)
VALUES
    ("Körpe", "Beyza", "F", "Ataşehir", "Gynaecologist"),
    ("Demirci", "Neslihan", "F", "Beşiktaş", "Otolaryngologist"),
    ("Çevik", "Mete", "M", "Üsküdar", "Neurologist"),
    ("Sezer", "Bilge", "F", "Maltepe", "Endocrinologist"),
    ("Şahin", "Gökçe", "F", "Sarıyer", "Ophthalmologist"),
    ("Sinan", "Can", "M", "Beyoğlu", "Gastroenterologist"),
    ("Duran", "Deren", "F", "Beşiktaş", "Urologist"),
    ("Özdemir", "Nehir", "F", "Kadıköy", "Psychiatrist"),
    ("Dereci", "Mustafa", "M", "Maltepe", "Cardiologist"),
    ("Enöz", "Murat", "M", "Bakırköy", "Otolaryngologist"),
    ("Şatıroğlu", "Cemal", "M", "Sultangazi", "Immunologist"),
    ("Ercan", "Ceylan", "F", "Şişli", "Hematologist");
""")
#12 Value

my_cursor.execute("""
INSERT INTO staff (name, dept, address, cell_num, dr_code)
VALUES
    ("Arda Edepoğlu", "Neurology", "Fatih", "905554233031",
        (SELECT dr_code FROM doctor WHERE name="Çevik" AND fname="Mete")),
    ("Ceren Aydın", "Gynaecology", "Maltepe", "905128442545",
        (SELECT dr_code FROM doctor WHERE name="Körpe" AND fname="Beyza")),
    ("Asiye Dereci", "Cardiology", "Maltepe", "905283123706",
        (SELECT dr_code FROM doctor WHERE name="Dereci" AND fname="Mustafa")),
    ("Berra Bodur", "Otolaryngology", "Üsküdar", "905553104540",
        (SELECT dr_code FROM doctor WHERE name="Demirci" AND fname="Neslihan")),
    ("Duygu Gönül", "Endocrinology", "Maltepe", "905442167515",
        (SELECT dr_code FROM doctor WHERE name="Sezer" AND fname="Bilge")),
    ("Burak Enöz", "Otolaryngology", "Sancaktepe", "905279601373",
        (SELECT dr_code FROM doctor WHERE name="Enöz" AND fname="Murat")),
    ("Zeynep Aydoğan", "Ophthalmology", "Şişli", "905314720208",
        (SELECT dr_code FROM doctor WHERE name="Şahin" AND fname="Gökçe")),
    ("Ozan Kozan", "Endocrinology", "Kartal", "905051246886",
        (SELECT dr_code FROM doctor WHERE name="Sezer" AND fname="Bilge")),
    ("Sinan Fidan", "Gastroenterology", "Esenler", "905123968776",
        (SELECT dr_code FROM doctor WHERE name="Sinan" AND fname="Can")),
    ("Ezel Yüksel", "Otolaryngology", "Ümraniye", "905365257815",
        (SELECT dr_code FROM doctor WHERE name="Demirci" AND fname="Neslihan")),
    ("Sevim Yeşilyurt", "Janitor", "Tuzla", "905273421345", NULL),
    ("Özgür Yıldırım", "Janitor", "Çekmeköy", "905433167244", NULL),
    ("Süreyya Cengiz", "Janitor", "Beykoz", "905147369341", NULL),
    ("Sezai Nizam", "Security", "Büyükçekmece", "905053761842", NULL),                        
    ("Mehtap Sonay", "Security", "Güngören", "905222073377", NULL);
""")
#15 Value

my_cursor.execute("""
INSERT INTO patient (name, fname, gender, address, tel_num, dr_code)
VALUES
    ("Demirci", "Burak", "M", "Maltepe", "905495607281",
        (SELECT dr_code FROM doctor WHERE name="Demirci" AND fname="Neslihan")),
    ("Çalış", "Azra", "F", "Ataşehir", "90524436074",
        (SELECT dr_code FROM doctor WHERE name="Körpe" AND fname="Beyza")),
    ("Üresin", "Asya", "F", "Maltepe", "905377199240",
        (SELECT dr_code FROM doctor WHERE name="Körpe" AND fname="Beyza")),
    ("Mohain", "Nada", "F", "Bakırköy", "905082161845",
        (SELECT dr_code FROM doctor WHERE name="Ercan" AND fname="Ceylan")),
    ("Aslan", "İrem", "F", "Beşiktaş", "905543754276",
        (SELECT dr_code FROM doctor WHERE name="Şahin" AND fname="Gökçe")),
    ("Yalman", "Kaan", "M", "Sarıyer", "905103041945",
        (SELECT dr_code FROM doctor WHERE name="Enöz" AND fname="Murat")),
    ("Toptan", "Serenay", "F", "Beşiktaş", "905058137982",
        (SELECT dr_code FROM doctor WHERE name="Sinan" AND fname="Can")),
    ("Dereci", "Beyza", "F", "Maltepe", "905381047256",
        (SELECT dr_code FROM doctor WHERE name="Dereci" AND fname="Mustafa")),
    ("Yıldız", "Arven", "F", "Kadıköy", "905142963444",
        (SELECT dr_code FROM doctor WHERE name="Demirci" AND fname="Neslihan")),
    ("Yücel", "Cem", "M", "Beykoz", "905555005055",
        (SELECT dr_code FROM doctor WHERE name="Çevik" AND fname="Mete")),
    ("Atay", "Sezen", "F", "Üsküdar", "905504001090",
        (SELECT dr_code FROM doctor WHERE name="Duran" AND fname="Deren")),
    ("Bilgin", "Haluk", "M", "Beyoğlu", "905024783492",
        (SELECT dr_code FROM doctor WHERE name="Şahin" AND fname="Gökçe")),
    ("Karaca", "Barış", "M", "Adalar", "905117306101",
        (SELECT dr_code FROM doctor WHERE name="Sinan" AND fname="Can")),
    ("Öztürk", "Eslem", "F", "Zeytinburnu", "905347014321",
        (SELECT dr_code FROM doctor WHERE name="Özdemir" AND fname="Nehir")),
    ("Tevfik", "Fikret", "M", "Beşiktaş", "905811850990",
        (SELECT dr_code FROM doctor WHERE name="Sezer" AND fname="Bilge")),
    ("Harman", "Alya", "F", "Şişli", "905430731",
        (SELECT dr_code FROM doctor WHERE name="Demirci" AND fname="Neslihan")),
    ("Kocabaş", "Alp", "M", "Pendik", "905334453443",
        (SELECT dr_code FROM doctor WHERE name="Özdemir" AND fname="Nehir")),
    ("Oğuzsoy", "Oğuz", "M", "Kartal", "905163320680",
        (SELECT dr_code FROM doctor WHERE name="Çevik" AND fname="Mete")),
    ("Öz", "Lara", "F", "Kağıthane", "905481052005",
        (SELECT dr_code FROM doctor WHERE name="Dereci" AND fname="Mustafa")),
    ("Özkurt", "Şevval", "F", "Maltepe", "905384402466",
        (SELECT dr_code FROM doctor WHERE name="Özdemir" AND fname="Nehir"));
""")
#20 Value

my_cursor.execute("""
INSERT INTO patient_diagnosis (diag_detail, remark, diag_date, other, pat_id)
VALUES
    ("Strep Throat", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Demirci" AND fname="Burak")),
    ("Endometrial Cancer", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Çalış" AND fname="Azra")),
    ("HPV", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Üresin" AND fname="Asya")),
    ("Anemia", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Mohain" AND fname="Nada")),
    ("Moderate Myopia", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Aslan" AND fname="İrem")),
    ("Ear Congestion", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Yalman" AND fname="Kaan")),
    ("Gastralgia", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Toptan" AND fname="Serenay")),
    ("Hypotension", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Dereci" AND fname="Beyza")),        
    ("Vertigo", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Yıldız" AND fname="Arven")),
    ("Meningitis", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Yücel" AND fname="Cem")),
    ("Urinary Tract Infection", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Atay" AND fname="Sezen")),
    ("Glaucoma", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Bilgin" AND fname="Haluk")),
    ("Reflux", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Karaca" AND fname="Barış")),
    ("Attention-Deficit Hyperactivity Disorder", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Öztürk" AND fname="Eslem")),
    ("Type 1 Diabetes", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Tevfik" AND fname="Fikret")),
    ("Sinusitis", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Harman" AND fname="Alya")),
    ("Major Depressive Disorder", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Kocabaş" AND fname="Alp")),
    ("Narcolepsy", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Oğuzsoy" AND fname="Oğuz")),
    ("Aneurysm", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Öz" AND fname="Lara")),  
    ("Post-Traumatic Stress Disorder", "NULL", CURRENT_TIMESTAMP + INTERVAL (RAND()*21600) SECOND, "NULL",
        (SELECT pat_id FROM patient WHERE name="Özkurt" AND fname="Şevval"));
""")
#20 Value

my_cursor.execute("""
INSERT INTO bill (pat_name, dr_name, datetime, amount, pat_id)
VALUES
    ("Burak Demirci", "Neslihan Demirci",(SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Demirci" AND fname="Burak")),
        72.5, (SELECT pat_id FROM patient WHERE name="Demirci" AND fname="Burak")),
    ("Azra Çalış", "Beyza Körpe",(SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Çalış" AND fname="Azra")),
        177.75, (SELECT pat_id FROM patient WHERE name="Çalış" AND fname="Azra")),
    ("Asya Üresin", "Beyza Körpe", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Üresin" AND fname="Asya")),
        152.25, (SELECT pat_id FROM patient WHERE name="Üresin" AND fname="Asya")),
    ("Nada Mohain", "Ceylan Ercan", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Mohain" AND fname="Nada")),
        77.75, (SELECT pat_id FROM patient WHERE name="Mohain" AND fname="Nada")),
    ("İrem Aslan", "Gökçe Şahin", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Aslan" AND fname="İrem")),
        90.0, (SELECT pat_id FROM patient WHERE name="Aslan" AND fname="İrem")),
    ("Kaan Yalman", "Murat Enöz", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Yalman" AND fname="Kaan")),
        92.5, (SELECT pat_id FROM patient WHERE name="Yalman" AND fname="Kaan")),
    ("Serenay Toptan", "Can Sinan", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Toptan" AND fname="Serenay")),
        87.5, (SELECT pat_id FROM patient WHERE name="Toptan" AND fname="Serenay")),
    ("Beyza Dereci", "Mustafa Dereci", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Dereci" AND fname="Beyza")),
        75.0, (SELECT pat_id FROM patient WHERE name="Dereci" AND fname="Beyza")),
    ("Arven Yıldız", "Neslihan Demirci", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Yıldız" AND fname="Arven")),
        67.5, (SELECT pat_id FROM patient WHERE name="Yıldız" AND fname="Arven")),
    ("Cem Yücel", "Mete Çevik", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Yücel" AND fname="Cem")),
        157.5, (SELECT pat_id FROM patient WHERE name="Yücel" AND fname="Cem")),
    ("Sezen Atay", "Deren Duran", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Atay" AND fname="Sezen")),
        137.5, (SELECT pat_id FROM patient WHERE name="Atay" AND fname="Sezen")),
    ("Haluk Bilgin", "Gökçe Şahin", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Bilgin" AND fname="Haluk")),
        120.0, (SELECT pat_id FROM patient WHERE name="Bilgin" AND fname="Haluk")),
    ("Barış Karaca", "Can Sinan", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Karaca" AND fname="Barış")),
        82.5, (SELECT pat_id FROM patient WHERE name="Karaca" AND fname="Barış")),
    ("Eslem Öztürk", "Nehir Özdemir", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Öztürk" AND fname="Eslem")),
        147.5, (SELECT pat_id FROM patient WHERE name="Öztürk" AND fname="Eslem")),
    ("Fikret Tevfik", "Bilge Sezer", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Tevfik" AND fname="Fikret")),
        122.5, (SELECT pat_id FROM patient WHERE name="Tevfik" AND fname="Fikret")),
    ("Alya Harman", "Neslihan Demirci", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Harman" AND fname="Alya")),
        80.0, (SELECT pat_id FROM patient WHERE name="Harman" AND fname="Alya")),
    ("Alp Kocabaş", "Nehir Özdemir", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Kocabaş" AND fname="Alp")),
        120.25, (SELECT pat_id FROM patient WHERE name="Kocabaş" AND fname="Alp")),
    ("Oğuz Oğuzsoy", "Mete Çevik", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Oğuzsoy" AND fname="Oğuz")),
        95.75, (SELECT pat_id FROM patient WHERE name="Oğuzsoy" AND fname="Oğuz")),
    ("Lara Öz", "Mustafa Dereci", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Öz" AND fname="Lara")),
        155.50, (SELECT pat_id FROM patient WHERE name="Öz" AND fname="Lara")),
    ("Şevval Özkurt", "Nehir Özdemir", (SELECT diag_date FROM patient_diagnosis WHERE pat_id=(SELECT pat_id FROM patient WHERE name="Özkurt" AND fname="Şevval")),
        127.25, (SELECT pat_id FROM patient WHERE name="Özkurt" AND fname="Şevval"));
""")
#20 Value

# 3)
my_cursor.execute("""
SELECT d.fname AS "Doctor Name", d.name AS "Doctor Surname", p.fname AS "Patient Name", p.name AS "Patient Surname"
FROM doctor AS d
LEFT OUTER JOIN patient AS p ON d.dr_code = p.dr_code
ORDER BY d.fname;
""")

res = my_cursor.fetchall()

print(f"{'DOCTOR':^20} {'PATIENT':^20}")
for row in res:
    doctor = f"{row[0]} {row[1]}"
    patient = f"{row[2]} {row[3]}"

    if row[2] is None and row[3] is None:
        print(f"{doctor:^20}")
    else:
        print(f"{doctor:^20} {patient:^20}")

print("\n")

# 4)
my_cursor.execute("""
SELECT dr_name AS "Doctor Name", pat_name AS "Patient Name", SUM(amount) AS "Total Debt"
FROM bill
GROUP BY bill_no
HAVING SUM(amount) >= 100
ORDER BY SUM(amount) DESC;
""")

res = my_cursor.fetchall()

print(f"{'DOCTOR':^20} {'PATIENT':^20} {'TOTAL DEBT':^10}")
for row in res:
    print(f"{row[0]:^20} {row[1]:^20} {row[2]:^10}")

print("\n")

# 5)
my_cursor.execute("""
SELECT d.fname AS "Doctor Name", d.name AS "Doctor Surname", COUNT(p.pat_id) AS "# of Patients"
FROM doctor AS d
LEFT OUTER JOIN patient AS p ON d.dr_code = p.dr_code
GROUP BY d.dr_code
ORDER BY COUNT(p.pat_id) DESC;
""")

res = my_cursor.fetchall()

print(f"{'DOCTOR':^20} {'# OF PATIENTS':^10}")
for row in res:
    doctor = f"{row[0]} {row[1]}"

    print(f"{doctor:^20} {row[2]:^10}")

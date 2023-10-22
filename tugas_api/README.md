# Flask API - Online Course 📖
## Tentang
API ini adalah api untuk sistem online course di mana seorang user dapat melakukan pendaftaran ke online course yang diinginkan.
Desain dari database yang dibuat adalah sebagai berikut.

![image](https://github.com/rosaamalia/belajar-python/assets/68428942/c5931cb9-a0e1-44e6-874d-8c875eb82178)

Relationship yang ada pada pada database adalah sebagai berikut.
1. Users (role: Student) dan Courses - many-to-many - dengan Enrollments sebagai tabel penghubung di antara keduanya. Satu User (Student) dapat mendaftar banyak Course, begitu pun Course dapat memiliki banyak User (Student)
2. Users (role: Instructor) dan Courses - one-to-many. Satu User (Instructor) dapat memiliki banyak Course yang diajar, namun satu Course hanya diajar oleh satu User (Instructor)
3. Courses dan Categories - one-to-many. Satu Course dapat memiliki satu Category, dan satu Category dapat memiliki banyak Course
4. Courses dan Modules - one-to-many. Satu Course dapat memiliki banyak Module, sedangkan satu Module hanya memiliki satu Course

## Fitur yang tersedia
- Fitur login dan keamanan menggunakan JWT (JSON Web Token)
- Fitur log menggunakan library logging

## Endpoint
- Semua endpoint menggunakan Authorization Bearer Token
- Setiap endpoint memiliki beberapa validasi yang sesuai dengan kebutuhan, beberapa di antaranya:
  - Untuk menambahkan Course hanya dapat menggunakan User dengan role Instructor
  - Untuk menambahkan Enrollment hanya dapat menggunakan User dengan role Student
  - Yang dapat mengedit dan menghapus Course, serta menambahkan, mengedit, dan menghapus Module hanya User (Instructor) yang berkaitan
  - Masing-masing User hanya dapat mengedit dan menghapus datanya sendiri

### Authentication
| Endpoint | HTTP Method | Fungsi |
| :---:   | :---: | :---: |
| /auth/signup | POST | Melakukan pendaftaran akun |
| /auth/signin | POST | Melakukan login ke akun yang sudah terdaftar |
| /auth/refresh | POST | Mendapatkan access token baru menggunakan refresh token |

### Users
| Endpoint | HTTP Method | Fungsi |
| :---:   | :---: | :---: |
| /users | GET | Mendapatkan semua data users |
| /users | POST | Menmabahkan data user |
| /users/{user_id} | GET | Mendapatkan data user berdasarkan id |
| /users/{user_id} | PUT | Mengedit data user berdasarkan id |
| /users/{user_id} | DELETE | Menghapus data user berdasarkan id |

### Courses
| Endpoint | HTTP Method | Fungsi |
| :---:   | :---: | :---: |
| /courses | GET | Mendapatkan semua data courses |
| /courses | POST | Menmabahkan data course |
| /courses/{course_id} | GET | Mendapatkan data course berdasarkan id |
| /courses/{course_id} | PUT | Mengedit data course berdasarkan id |
| /courses/{course_id} | DELETE | Menghapus data course berdasarkan id |

### Enrollments
| Endpoint | HTTP Method | Fungsi |
| :---:   | :---: | :---: |
| /enrollments | POST | Menmabahkan data enrollment |
| /enrollments/{enrollment_id} | GET | Mendapatkan data enrollment berdasarkan id |
| /enrollments/{enrollment_id} | PUT | Mengedit data enrollment berdasarkan id |
| /enrollments/{enrollment_id} | DELETE | Menghapus data enrollment berdasarkan id |

### Modules
| Endpoint | HTTP Method | Fungsi |
| :---:   | :---: | :---: |
| /modules | GET | Mendapatkan semua data modules |
| /modules | POST | Menmabahkan data module |
| /modules/{module_id} | GET | Mendapatkan data module berdasarkan id |
| /modules/{module_id} | PUT | Mengedit data module berdasarkan id |
| /modules/{module_id} | DELETE | Menghapus data module berdasarkan id |

### Categories
| Endpoint | HTTP Method | Fungsi |
| :---:   | :---: | :---: |
| /categories | GET | Mendapatkan semua data categories |
| /categories | POST | Menmabahkan data category |
| /categories/{category_id} | GET | Mendapatkan data category berdasarkan id |
| /categories/{category_id} | PUT | Mengedit data category berdasarkan id |
| /categories/{category_id} | DELETE | Menghapus data category berdasarkan id |

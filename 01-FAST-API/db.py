import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="abc123",
        dbname="pydb",
        port=5432
    )

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS STUDENTS(
            ID INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            NAME VARCHAR(100) NOT NULL,
            COURSE VARCHAR(100) NOT NULL,
            FEE NUMERIC(10,2) NOT NULL CHECK (FEE > 0) 
        )
    """

    cursor.execute(query)
    cursor.close()
    connection.commit()
    connection.close()
    print("Table created successfully")

def insert_student(student):
    connection = get_connection()
    cursor = connection.cursor()
    query = "insert into students(name, course, fee) values (%s, %s, %s)"

    cursor.execute(query, (student.name, student.course, student.fee))
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "success": True,
        "message": "Student table created !",
        "data": student
    }

def get_all_students():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = "select * from students"   
    cursor.execute(query);
    students = cursor.fetchall();

    cursor.close();
    connection.close();

    return {
        "success": True,
        "message": "Student records fetched successfully !",
        "data": students
    }

def get_student_by_id(id):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query = "select * from students where id=%s"
    cursor.execute(query, (id,))

    student = cursor.fetchone()
    if student is None:
        return {
            "success": False,
            "message": "No records found !",
            "data": None
        }

    cursor.close()
    connection.close()

    
    return {
        "success": True,
        "message": "Student fetched succesfully !",
        "data": student
    }

def update_student(id, student):
    connection = get_connection()
    cursor = connection.cursor()
    query = "update students set name=%s, course=%s, fee=%s where id=%s"
    cursor.execute(query, (student.name, student.course, student.fee, id))
    connection.commit()
    cursor.close()
    return {
        "success": True,
        "message": "Student record updated successfully !!"
    }

def delete_student_by_id(id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "delete from students where id=%s"
    cursor.execute(query, (id,))    # the comma here creates the tuple
    connection.commit()
    cursor.close()
    return {
        "success": True,
        "message": "Student record deleted successfully !!"
    }


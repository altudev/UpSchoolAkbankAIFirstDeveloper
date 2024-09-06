import streamlit as st
from sqlalchemy.orm import sessionmaker
from data.database import engine, Base
from models.student import Student
from models.teacher import Teacher

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def student_page():
    """Displays the page for managing students."""
    # Create a database session
    db = SessionLocal()

    st.title("Students")

    # Add a new student
    st.header("Add a new student")
    name = st.text_input("Name", key="student_name")
    grade = st.number_input("Grade", min_value=1, max_value=12, key="student_grade")
    student_id = st.text_input("Student ID", key="student_id")
    if st.button("Add student"):
        student = Student(name=name, grade=grade, student_id=student_id)
        db.add(student)
        db.commit()
        st.success("Student added successfully!")

    # View all students
    st.header("View all students")
    students = db.query(Student).all()
    if students:
        st.table([
            {"ID": student.id, "Name": student.name, "Grade": student.grade, "Student ID": student.student_id}
            for student in students
        ])
    else:
        st.info("No students found.")

    # Delete a student
    st.header("Delete a student")
    student_id_to_delete = st.text_input("Student ID to delete", key="student_id_delete")
    if st.button("Delete student"):
        student = db.query(Student).filter(Student.student_id == student_id_to_delete).first()
        if student:
            db.delete(student)
            db.commit()
            st.success("Student deleted successfully!")
        else:
            st.error("Student not found.")

    # Close the database session
    db.close()

def teacher_page():
    """Displays the page for managing teachers."""
    # Create a database session
    db = SessionLocal()

    st.title("Teachers")

    # Add a new teacher
    st.header("Add a new teacher")
    name = st.text_input("Name", key="teacher_name")
    subject = st.text_input("Subject", key="teacher_subject")
    teacher_id = st.text_input("Teacher ID", key="teacher_id")
    if st.button("Add teacher"):
        teacher = Teacher(name=name, subject=subject, teacher_id=teacher_id)
        db.add(teacher)
        db.commit()
        st.success("Teacher added successfully!")

    # View all teachers
    st.header("View all teachers")
    teachers = db.query(Teacher).all()
    if teachers:
        st.table([
            {"ID": teacher.id, "Name": teacher.name, "Subject": teacher.subject, "Teacher ID": teacher.teacher_id}
            for teacher in teachers
        ])
    else:
        st.info("No teachers found.")

    # Delete a teacher
    st.header("Delete a teacher")
    teacher_id_to_delete = st.text_input("Teacher ID to delete", key="teacher_id_delete")
    if st.button("Delete teacher"):
        teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id_to_delete).first()
        if teacher:
            db.delete(teacher)
            db.commit()
            st.success("Teacher deleted successfully!")
        else:
            st.error("Teacher not found.")

    # Close the database session
    db.close()

# Define the pages
pages = {
    "Students": student_page,
    "Teachers": teacher_page,
}

# Select the page to display
page = st.sidebar.selectbox("Select a page", list(pages.keys()))

# Display the selected page
pages[page]()

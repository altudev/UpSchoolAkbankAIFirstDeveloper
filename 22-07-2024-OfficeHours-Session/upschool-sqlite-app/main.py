# File: streamlit_app.py
import base64

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Cat

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_cats.db')

# Create all tables in the engine
Base.metadata.create_all(engine)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def add_cat(name, breed, age, colour):
    new_cat = Cat(name=name, breed=breed, age=age, colour=colour)
    session.add(new_cat)
    session.commit()
    return f"Cat '{name}' added successfully."


def get_all_cats():
    return session.query(Cat).all()


def get_cat_by_id(cat_id):
    return session.query(Cat).filter_by(id=cat_id).first()


def update_cat_age(cat_id, new_age):
    cat = get_cat_by_id(cat_id)
    if cat:
        cat.age = new_age
        session.commit()
        return f"Cat '{cat.name}' (ID: {cat_id}) age updated to {new_age}."
    else:
        return f"Cat with ID {cat_id} not found."


def delete_cat(cat_id):
    cat = get_cat_by_id(cat_id)
    if cat:
        session.delete(cat)
        session.commit()
        return f"Cat with ID {cat_id} (name: '{cat.name}') deleted successfully."
    else:
        return f"Cat with ID {cat_id} not found."


def add_favicon(icon_path):
    # Read the image file and encode it to base64
    with open(icon_path, "rb") as f:
        icon_data = f.read()
    icon_b64 = base64.b64encode(icon_data).decode("utf-8")

    # Determine the MIME type based on the file extension
    if icon_path.endswith('.svg'):
        mime_type = 'image/svg+xml'
    elif icon_path.endswith('.png'):
        mime_type = 'image/png'
    else:
        raise ValueError("Icon file must be either SVG or PNG")

    # Inject the favicon into the HTML head
    st.markdown(
        f"""
        <head>
            <link rel="icon" href="data:{mime_type};base64,{icon_b64}" type="image/x-icon">
        </head>
        """,
        unsafe_allow_html=True,
    )

def main():
    # Use SVG or PNG file as favicon
    add_favicon("assets/favicon.svg")  # or "assets/favicon.png"

    # Create two columns for logo and title
    col1, col2 = st.columns([1, 4])

    # Add logo to the first column
    col1.image("assets/logo.png", width=100)

    # Add title to the second column
    col2.title("Cat Database Management")

    menu = ["View Cats", "Add Cat", "Update Cat Age", "Delete Cat"]
    choice = st.sidebar.selectbox("Select Operation", menu)

    if choice == "View Cats":
        st.subheader("All Cats")
        cats = get_all_cats()
        for cat in cats:
            st.write(f"ID: {cat.id}, Name: {cat.name}, Breed: {cat.breed}, Age: {cat.age}, Colour: {cat.colour}")

    elif choice == "Add Cat":
        st.subheader("Add New Cat")
        name = st.text_input("Cat's Name")
        breed = st.text_input("Cat's Breed")
        age = st.number_input("Cat's Age", min_value=0, max_value=30, value=0, step=1)
        colour = st.text_input("Cat's Colour")
        if st.button("Add Cat"):
            result = add_cat(name, breed, age, colour)
            st.success(result)

    elif choice == "Update Cat Age":
        st.subheader("Update Cat's Age")
        cat_id = st.number_input("Cat's ID", min_value=1, value=1, step=1)
        new_age = st.number_input("New Age", min_value=0, max_value=30, value=0, step=1)
        if st.button("Update Age"):
            result = update_cat_age(cat_id, new_age)
            st.success(result)

    elif choice == "Delete Cat":
        st.subheader("Delete Cat")
        cat_id = st.number_input("Cat's ID", min_value=1, value=1, step=1)
        if st.button("Delete Cat"):
            result = delete_cat(cat_id)
            st.success(result)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from app import create_app, db
from app.models import User
import os

app = create_app()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("====================================")
    print("       Admin Management Tool        ")
    print("====================================")

def create_admin():
    print("\n--- Create Admin User ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    with app.app_context():
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"\nError: User '{username}' already exists!")
            return
        
        # Create new admin user
        user = User(username=username, is_admin=1)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"\nAdmin user '{username}' created successfully!")

def list_admins():
    print("\n--- Admin Users List ---")
    with app.app_context():
        admins = User.query.filter_by(is_admin=1).all()
        if not admins:
            print("No admin users found.")
            return
        
        for admin in admins:
            print(f"- {admin.username}")

def delete_admin():
    print("\n--- Delete Admin User ---")
    username = input("Enter username to delete: ")
    
    with app.app_context():
        # Find the user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"\nError: User '{username}' not found!")
            return
        
        # Check if user is admin
        if not user.is_admin:
            print(f"\nError: User '{username}' is not an admin!")
            return
        
        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete admin user '{username}'? (y/n): ")
        if confirm.lower() != 'y':
            print("\nDeletion cancelled.")
            return
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        print(f"\nAdmin user '{username}' deleted successfully!")

def main_menu():
    while True:
        print_header()
        print("\nOptions:")
        print("1. Create admin user")
        print("2. Show all admin users")
        print("3. Delete admin user")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            create_admin()
        elif choice == '2':
            list_admins()
        elif choice == '3':
            delete_admin()
        elif choice == '4':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main_menu()

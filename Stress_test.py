import os
import logging
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import time
import subprocess

load_dotenv()

logging.basicConfig(
    filename='stress_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def memory_stress():
    try:
        logging.info("Starting memory stress test...")
        os.system("stress-ng --vm 1 --vm-bytes 80% -t 60s")
        logging.info("Memory stress test completed.")
    except Exception as e:
        logging.error(f"Memory stress test failed: {e}")

def disk_stress():
    try:
        logging.info("Starting disk stress test...")
        os.system("stress-ng --hdd 1 --hdd-bytes 80% -t 60s")
        logging.info("Disk stress test completed.")
    except Exception as e:
        logging.error(f"Disk stress test failed: {e}")

def network_stress():
    try:
        logging.info("Starting network stress test...")
        os.system("iperf3 -c 192.168.0.116")
        logging.info("Network stress test completed.")
    except Exception as e:
        logging.error(f"Network stress test failed: {e}")

def cpu_stress():
    try:
        logging.info("Starting CPU stress test...")
        os.system("stress-ng --cpu 1 --cpu-load 5 --cpu-method matrixprod -t 60s")
        logging.info("CPU stress test completed.")
    except Exception as e:
        logging.error(f"CPU stress test failed: {e}")

def mysql_stress():
    try:
        logging.info("Starting MySQL stress test...")
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = connection.cursor()

        start_time = time.time()
        query_count = 0
        duration = 60

        while time.time() - start_time < duration:
            cursor.execute("SELECT * FROM sbtest1 LIMIT 1")
            cursor.fetchall()
            query_count += 1

        elapsed_time = time.time() - start_time
        qps = query_count / elapsed_time
        logging.info(f"MySQL QPS stress test completed. Approximate QPS: {qps:.2f}")

    except Error as e:
        logging.error(f"Error during MySQL QPS stress test: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.info("MySQL connection closed after stress test.")

def show_menu():
    while True:
        print("\n--- Stress Testing Menu ---")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            logging.info("User selected Memory Stress Testing.")
            memory_stress()
        elif choice == '2':
            logging.info("User selected Disk Stress Testing.")
            disk_stress()
        elif choice == '3':
            logging.info("User selected Network Stress Testing.")
            network_stress()
        elif choice == '4':
            logging.info("User selected CPU Stress Testing.")
            cpu_stress()
        elif choice == '5':
            logging.info("User selected MySQL Stress Testing.")
            mysql_stress()
        elif choice == '0':
            logging.info("User exited the stress testing menu.")
            print("Exiting...")
            break
        else:
            logging.warning("Invalid option selected.")
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    logging.info("Starting the Stress Test Script")
    show_menu()
    logging.info("Stress Test Script Ended")
    subprocess.Popen(['python3', 'gemini.py'])

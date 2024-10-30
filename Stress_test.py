import os
import logging
import mysql.connector
from mysql.connector import Error
import threading
import time
# This is a change
# Set up logging configuration
logging.basicConfig(
    filename='stress_test.log',  # Log output file
    level=logging.INFO,           # Logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

# Stress Test Functions
def memory_stress():
    logging.info("Starting memory stress test...")
    os.system("stress-ng --vm 1 --vm-bytes 80% -t 60s")
    logging.info("Memory stress test completed.")

def disk_stress():
    logging.info("Starting disk stress test...")
    os.system("stress-ng --hdd 1 --hdd-bytes 80% -t 60s")
    logging.info("Disk stress test completed.")

def network_stress():
    logging.info("Starting network stress test...")
    os.system("iperf3 -c 192.168.0.116")  # Replace with an actual target IP
    logging.info("Network stress test completed.")

def cpu_stress():
    logging.info("Starting CPU stress test...")
    os.system("stress-ng --cpu 1 --cpu-load 5 --cpu-method matrixprod -t 60s")
    logging.info("CPU stress test completed.")

def mysql_stress():
#    logging.info("Starting MySQL stress test...")
 #   os.system("mysqlslap --concurrency=10 --iterations=80 --number-int-cols=2 --auto-generate-sql --number-of-queries=100 --host=192.168.0.116 --user=exporter1 --password=Vaibhav@1909")
  #  logging.info("MySQL stress test completed.")
    try:
        connection = mysql.connector.connect(
            host='192.168.0.116',
            database='testdb',
            user='exporter1',
            password='Vaibhav@1909'
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
        print(f"MySQL QPS stress test completed. Approximate QPS: {qps:.2f}")

    except Error as e:
        print("Error during MySQL QPS stress test:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


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

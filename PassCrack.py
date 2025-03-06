import multiprocessing
import time
import pypdf
import sys

def try_password_batch(pdf_path, start, end, length, result_queue, progress_interval=1000000):
    """Attempts a batch of passwords of a specific length."""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for num in range(start, end):
            attempt = str(num).zfill(length)  # Pad to desired length (e.g., "1" or "00000001")
            try:
                if reader.decrypt(attempt):  # If decryption succeeds
                    result_queue.put(attempt)
                    return
            except Exception:
                pass  # Ignore incorrect attempts
            if num % progress_interval == 0 and num > start:
                print(f"ℹ️ Testing length {length}: {attempt}", flush=True)
    except Exception as e:
        print(f"❌ Error in process: {e}", flush=True)

def start_pdf_cracking(pdf_path):
    """Cracks the PDF password, starting with short passwords."""
    try:
        # Check if the PDF is encrypted
        reader = pypdf.PdfReader(pdf_path)
        if not reader.is_encrypted:
            print("ℹ️ PDF is not encrypted. No password needed.")
            return

        start_time = time.time()
        result_queue = multiprocessing.Queue()

        # Step 1: Try single-digit passwords (0-9) in a single process
        print("ℹ️ Checking single-digit passwords (0-9)...")
        quick_process = multiprocessing.Process(
            target=try_password_batch,
            args=(pdf_path, 0, 10, 1, result_queue, 1)  # Length 1, progress every 1
        )
        quick_process.start()
        quick_process.join()

        if not result_queue.empty():
            password = result_queue.get()
            print(f"\n🔥 Password found: {password}")
            print(f"⏳ Time taken: {time.time() - start_time:.2f} seconds")
            return

        # Step 2: Try lengths 2 to 8 with multiprocessing
        num_processes = multiprocessing.cpu_count()
        chunk_size = 500000

        for length in range(2, 9):  # Lengths 2 to 8
            max_value = 10 ** length  # e.g., 100 for length 2, 100000000 for length 8
            print(f"ℹ️ Trying passwords of length {length} (0-{max_value-1}) with {num_processes} processes...")
            processes = []

            for start in range(0, max_value, chunk_size * num_processes):
                for i in range(num_processes):
                    thread_start = start + (i * chunk_size)
                    thread_end = min(thread_start + chunk_size, max_value)
                    process = multiprocessing.Process(
                        target=try_password_batch,
                        args=(pdf_path, thread_start, thread_end, length, result_queue)
                    )
                    processes.append(process)
                    process.start()

                while not result_queue.empty():
                    password = result_queue.get()
                    for p in processes:
                        p.terminate()
                        p.join()
                    print(f"\n🔥 Password found: {password}")
                    print(f"⏳ Time taken: {time.time() - start_time:.2f} seconds")
                    return

                for p in processes:
                    p.join()
                processes.clear()

            if length == 8:
                print(f"❌ Password not found up to 8 digits (0-{max_value-1})")
                print(f"⏳ Time taken: {time.time() - start_time:.2f} seconds")

    except FileNotFoundError:
        print(f"❌ Error: File '{pdf_path}' not found.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    pdf_path = "1.pdf"  # Replace with your PDF file path if different
    print(f"ℹ️ Starting password cracking for '{pdf_path}'...")
    try:
        start_pdf_cracking(pdf_path)
    except KeyboardInterrupt:
        print("\n🛑 Cracking interrupted by user.")
        sys.exit(1)
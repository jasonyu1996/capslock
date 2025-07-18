
# AddressSanitizer
echo "Building for AddressSanitizer..."
python3 build-san.py address > /dev/null 2>&1
echo "Running AddressSanitizer..."
python3 run-san.py address 2>&1 | grep -F -e "Running RUSTSEC" -e "SUMMARY: AddressSanitizer" | tee log-asan.txt

# ThreadSanitizer
echo "Building for ThreadSanitizer..."
python3 build-san.py thread > /dev/null 2>&1
echo "Running ThreadSanitizer..."
python3 run-san.py thread 2>&1 |  grep -F -e "Running RUSTSEC" -e "SUMMARY: ThreadSanitizer" | tee log-tsan.txt

# Miri
echo "Running Miri..."
python3 run-miri.py 2>&1 | grep -F -e "Running RUSTSEC" -e "error: Undefined Behavior" | tee log-miri.txt

# CapsLock
echo "Building for CapsLock..."
python3 build.py > /dev/null 2>&1
echo "Running CapsLock..."
sh run-all.sh > /dev/null 2>&1
grep -r -F "Attempting" run-logs | sort | tee log-capslock.txt

echo "=== SUMMARY ==="
echo "CapsLock found $(cat log-capslock.txt | wc -l) violations"
echo "MIRI found $(awk -f count.awk log-miri.txt) violations"
echo "AddressSanitizer found $(awk -f count.awk log-asan.txt) violations"
echo "ThreadSanitizer found $(awk -f count.awk log-tsan.txt) violations"

import subprocess, os

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

out = run('git ls-files --others --exclude-standard "Plumber works"')
untracked = [f for f in out.stdout.strip().split('\n') if f]

out2 = run('git ls-files -m "Plumber works"')
modified = [f for f in out2.stdout.strip().split('\n') if f]

all_files = untracked + modified
all_files = [f for f in all_files if f]

print(f"Files to push: {len(all_files)}")

batch_size = 8
for i in range(0, len(all_files), batch_size):
    batch = all_files[i:i+batch_size]
    if not batch: continue
    for file in batch:
        run(f'git add "{file}"')
    res = run('git commit -m "Compress images for faster loading"')
    print(f"Batch {i//batch_size+1} committed")
    for attempt in range(3):
        res = run('git push -u origin main')
        if res.returncode == 0:
            print(f"  Pushed!")
            break
        print(f"  Retry {attempt+1}...")
        import time; time.sleep(2)

print("All done!")

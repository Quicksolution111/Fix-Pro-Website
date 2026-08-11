import os, subprocess, time

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

out = run('git ls-files --others --exclude-standard')
files = out.stdout.strip().split('\n')
files = [f for f in files if f]

batch_size = 5
for i in range(0, len(files), batch_size):
    batch = files[i:i+batch_size]
    if not batch: continue
    print(f'Pushing batch {i//batch_size + 1}...')
    for file in batch:
        run(f'git add "{file}"')
    
    run('git commit -m "Add batch of images"')
    for attempt in range(3):
        res = run('git push -u origin main')
        if res.returncode == 0:
            print('Success')
            break
        print('Retrying push...')
        time.sleep(2)

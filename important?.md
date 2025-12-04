Yes. Here are all three in one place.

  

GIT RULES ONE-SHEET – TREVOROS_V41

1. Locations
    

  

- Main repo directory:
    
    ~/Downloads/trevoros_repo
    
- Obsidian vault worktree:
    
    /Library/Mobile Documents/iCloudmd~obsidian/Documents/TrevorOS_v41
    

  

2. Golden rules
    

  

- Do not run git commands inside Obsidian itself.
    
- Run git only in ~/Downloads/trevoros_repo.
    
- Keep branch trevoros_v41 in sync with origin/trevoros_v41.
    
- One vault = one branch = trevoros_v41.
    
- Commit small, descriptive, often.
    
- Avoid manual edits of .git directories.
    

  

3. Daily workflow
    

  

- Edit notes in Obsidian.
    
- Let Obsidian Git auto commit every 5 minutes and push.
    
- Once or twice a day run in Terminal:
    
    cd ~/Downloads/trevoros_repo
    
    git status
    
    git pull
    
- If git status shows “working tree clean” and branch trevoros_v41, everything is fine.
    

  

4. When starting work on a new day
    

  

- Open Obsidian.
    
- In Terminal:
    
    cd ~/Downloads/trevoros_repo
    
    git switch trevoros_v41
    
    git pull
    
- Then edit in Obsidian as usual.
    

  

5. When something looks wrong in Obsidian Git
    

  

- Do not mash buttons.
    
- Flip to Terminal:
    
    cd ~/Downloads/trevoros_repo
    
    git status
    
    git log –oneline -5
    
- If status is dirty and you did not intend those edits, stop and use the recovery script below rather than guessing.
    

  

DISASTER RECOVERY SCRIPT

  

Goal: recover when the vault or plugin state feels cursed.

  

A. Snapshot the broken vault

1. In Terminal:
    
    cd /Library/Mobile\ Documents/iCloudmd~obsidian/Documents
    
    mv TrevorOS_v41 TrevorOS_v41_broken_$(date +%Y%m%d_%H%M)
    
2. Now the broken state sits in the _broken_ folder for inspection.
    

  

B. Recreate a fresh worktree from GitHub

1. Go to main repo:
    
    cd ~/Downloads/trevoros_repo
    
    git fetch origin
    
2. Ensure branch exists and is healthy:
    
    git show origin/trevoros_v41:AGENTS.md | head
    
    If that prints the agent rules, the branch is fine.
    
3. Recreate the worktree into iCloud:
    
    git worktree add 
    
    /Library/Mobile\ Documents/iCloudmd~obsidian/Documents/TrevorOS_v41 
    
    trevoros_v41
    
4. Open Obsidian, select the TrevorOS_v41 folder as a vault, let it index.
    
    Obsidian now points at a clean worktree tied to trevoros_v41.
    

  

C. Hard reset local branch to remote (when commits went bad)

  

Use this when the repo log in trevoros_v41 gained bad commits and you want remote to win.

1. In main repo:
    
    cd ~/Downloads/trevoros_repo
    
    git switch trevoros_v41
    
    git fetch origin
    
2. Force local branch to match remote:
    
    git reset –hard origin/trevoros_v41
    
3. Update the worktree files:
    
    git worktree prune
    
    # **then, if needed**
    
      
    
    git worktree remove 
    
    /Library/Mobile\ Documents/iCloudmdobsidian/Documents/TrevorOS_v41 –force
    
    git worktree add 
    
    /Library/Mobile\ Documents/iCloudmdobsidian/Documents/TrevorOS_v41 
    
    trevoros_v41
    
4. Open Obsidian again. The vault now matches origin/trevoros_v41 exactly.
    

  

D. Repair plugin confusion without nuking the vault

  

If Obsidian Git shows strange errors but git status in Terminal is clean:

1. In Obsidian Git settings, hit “Pull” once.
    
2. If error persists, disable the plugin, restart Obsidian, enable it again.
    
3. If errors remain, fall back to steps A–C.
    

  

BRANCHING MODEL FOR TREVOROS

  

Branches and roles

- main
    
    Upstream project branch on GitHub. Treat as read-only. No direct commits.
    
- trevoros_v41
    
    Your long-lived “vault branch”. The worktree in iCloud tracks this branch.
    
    All Obsidian edits land here.
    
- feature/*
    
    Optional short-lived branches for experiments. Live only in ~/Downloads/trevoros_repo, never as worktrees.
    

  

How you use it

1. Normal work (Obsidian)
    

  

- Work only in the TrevorOS_v41 vault.
    
- Let Obsidian Git commit and push to origin/trevoros_v41.
    
- In Terminal now and then:
    
    cd ~/Downloads/trevoros_repo
    
    git switch trevoros_v41
    
    git pull
    

  

2. Experimental change without touching the live vault
    

  

Example: refactor schema, write new tools, heavy edits.

- In Terminal:
    
    cd ~/Downloads/trevoros_repo
    
    git switch trevoros_v41
    
    git pull
    
    git switch -c feature/schema-tuning
    
- Edit files in the repo folder (not iCloud vault).
    
- Test, run tools, validate:
    
    make -f TrevorOS_v41/Makefile validate
    
- When satisfied:
    
    git add TrevorOS_v41
    
    git commit -m “tune schema and validator”
    
    git switch trevoros_v41
    
    git merge –no-ff feature/schema-tuning
    
    git push origin trevoros_v41
    
    git branch -d feature/schema-tuning
    
- Then refresh the vault worktree from trevoros_v41 if needed using the recovery script’s “recreate worktree” piece, or let git propagate through existing worktree with a pull.
    

  

3. Updating from upstream main (if the original repo evolves)
    

  

Occasionally the upstream owner might update main. To pull that into your tree:

  

cd ~/Downloads/trevoros_repo

git fetch origin

git switch trevoros_v41

git merge origin/main

  

Resolve conflicts once in the repo folder. Then push:

  

git push origin trevoros_v41

  

Finally pull in Obsidian Git so the vault sees the same state.

  

Summary

- Obsidian writes only to trevoros_v41 via worktree.
    
- Terminal work happens in ~/Downloads/trevoros_repo.
    
- Disaster script gives you a clean reset path.
    
- Feature branches stay outside the vault.
    

  

If you want next step, I can walk through a dry-run: create a tiny test note in Obsidian, watch Obsidian Git commit it, then inspect the exact commit in Terminal so your mental model locks in.
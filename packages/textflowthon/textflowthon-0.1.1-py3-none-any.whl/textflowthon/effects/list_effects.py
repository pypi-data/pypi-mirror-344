import os

if __name__ == "__main__":
    EFFECTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'textflowthon', 'effects')
    EFFECTS_DIR = os.path.abspath(EFFECTS_DIR)
    print("Available animation effects in TextFlowThon:")
    for fname in sorted(os.listdir(EFFECTS_DIR)):
        if fname.endswith('.py') and not fname.startswith('__'):
            print(" -", fname.replace('.py', ''))
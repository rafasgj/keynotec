"""Runs KeynoteC."""

if __name__ == "__main__":
    import keynotec
    try:
        keynotec.run()
    except Exception as e:
        print(e)

def chunk_text(text, chunk_size = 3000):
    chunk = []
    lines = text.strip().split()

    for i in range(0, len(lines), chunk_size):
        chunk.append(" ".join(lines[i:i+chunk_size])) #chunks text into 1000 word range

    return chunk
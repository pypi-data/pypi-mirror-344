import threading
import numpy as np

class ContextWindow:
    def __init__(self, max_chunks: int):
        """
        Initializes a thread-safe context window as a ring buffer.
        :param max_chunks: Maximum number of chunks to store.
        """
        self.max_chunks = max_chunks
        self.window = []
        self.start_index = 0
        self.lock = threading.Lock()  # Lock for thread-safe operations

    def not_empty(self) -> bool:
        """Check if the context window is not empty."""
        with self.lock:
            return len(self.window) > 0

    def is_empty(self) -> bool:
        """Check if the context window is empty."""
        with self.lock:
            return len(self.window) == 0
        
    def is_full(self) -> bool:
        """Check if the context window is full."""
        with self.lock:
            return len(self.window) >= self.max_chunks

    def add(self, chunk: bytes):
        """
        Adds a new chunk to the context window. Overwrites the oldest chunk if the buffer is full.
        :param chunk: The new chunk to add.
        """
        with self.lock:
            if len(self.window) < self.max_chunks:
                self.window.append(chunk)
                self.start_index = 0  # Reset start index on initial fills
            else:
                # Overwrite the oldest chunk
                self.window[self.start_index] = chunk
                self.start_index = (self.start_index + 1) % self.max_chunks

    def get(self) -> bytes:
        """
        Retrieves all chunks concatenated into a single array, starting from the start index.
        :return: Concatenated numpy array of all chunks.
        """
        with self.lock:
            if not self.window:
                return b""  # Return empty bytes if the window is empty

            # Return the concatenated bytes starting from the start index
            if self.start_index == 0:
                return b"".join(self.window)
            else:
                return b"".join(self.window[self.start_index:] + self.window[:self.start_index])

    def consume(self) -> bytes:
        """
        Consume all chunks in the context window and return them as a single byte array.
        :return: Concatenated numpy array of all chunks.
        """
        with self.lock:
            if not self.window:
                return b""
            # Create a copy of the current window
            if self.start_index == 0:
                data = b"".join(self.window)
            else:
                data = b"".join(self.window[self.start_index:] + self.window[:self.start_index])
            # Clear the window after consuming
            self.window.clear()
            self.start_index = 0
            
            return data
        
    def consume_into(self, output: bytearray, output_start_index: int = 0) -> int:
        """
        Consumes the entire buffer and appends its contents into the given bytearray.
        :param output: A bytearray to which the buffer's contents will be appended.
        :param output_start_index: The starting index in the output bytearray where the contents will be appended.
        :return: The number of bytes written to the output bytearray.
        """
        with self.lock:
            if not self.window:
                return
            
            bytes_written = 0
            for i in range(len(self.window)):
                i += self.start_index
                i = i % len(self.window)
                amt_bytes = len(self.window[i])
                
                bytes_written += amt_bytes
                output[output_start_index:output_start_index + amt_bytes] = self.window[i]
                output_start_index += amt_bytes
                
            self.window.clear()
            self.start_index = 0
            return bytes_written

    def get_last(self) -> bytes:
        """
        Retrieves the last chunk in the context window.
        :return: The last chunk in the context window.
        """
        with self.lock:
            if not self.window:
                return b""
            
            if self.start_index == 0:
                return self.window[-1]
            else:
                return self.window[self.start_index - 1]
            
    def amt_chunks(self) -> int:
        """Returns the number of chunks in the context window."""
        with self.lock:
            return len(self.window)
        
            
    def clear(self):
        """Clears the context window."""
        with self.lock:
            self.window.clear()
            self.start_index = 0
            
    def clear_bytes_from_start(self, bytes_to_clear: bytes):
        """
        Removes chunks from the beginning of the context window based on the provided byte sequence.
        
        This method physically removes chunks from the start of the window until it has removed
        at least the number of bytes in the provided sequence. This reduces memory usage and 
        keeps the buffer size optimal.
        
        Args:
            bytes_to_clear: A byte sequence representing the data to be cleared from the start
                            of the context window. The actual number of bytes removed may be
                            slightly larger due to chunking.
        
        Returns:
            int: The number of chunks removed from the window
        """
        # Check if the context window is empty
        if self.is_empty():
            return 0
        
        current_chunk: bytes = self.get()
        # Check if the current chunk is longer than the chunk to clear
        if len(current_chunk) < len(bytes_to_clear):
            # Just clear everything
            chunks_removed = len(self.window)
            self.clear()
            return chunks_removed
        
        with self.lock:
            # Calculate how many bytes we need to clear
            bytes_to_clear_length = len(bytes_to_clear)
            
            # Keep track of how many bytes and chunks we've processed
            bytes_cleared = 0
            chunks_removed = 0
            
            # Make a copy of the window to work with
            ordered_window = []
            
            # Rearrange the window to logical order starting from start_index
            if self.start_index > 0:
                ordered_window = self.window[self.start_index:] + self.window[:self.start_index]
            else:
                ordered_window = self.window.copy()
            
            # Count chunks until we've covered enough bytes
            for i, chunk in enumerate(ordered_window):
                bytes_cleared += len(chunk)
                chunks_removed += 1
                
                if bytes_cleared >= bytes_to_clear_length:
                    break
            
            # Now actually remove the chunks
            if chunks_removed > 0:
                # Keep only the chunks we want to retain
                self.window = ordered_window[chunks_removed:]
                self.start_index = 0  # Reset start index since we've reordered
                
            return chunks_removed
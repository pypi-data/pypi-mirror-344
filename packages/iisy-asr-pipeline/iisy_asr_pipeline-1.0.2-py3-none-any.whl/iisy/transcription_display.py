from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel

class TranscriptionDisplay:
    """Handles console display for transcriptions using the Rich library."""
    
    def __init__(self):
        self.console = Console()
        self.live = None
        self.current_text = None
    
    def _create_formatted_text(self, content, speaker, embedding_count, complete=False):
        """Create a formatted Text object for display."""
        text = Text()
        
        # Add speaker info with appropriate styling
        style = "green" if complete else "blue"
        text.append(f"[{embedding_count}] {speaker}: ", style=style)
        
        # Add the actual transcription content
        text.append(content)
        
        return text
    
    def start(self):
        """Start the live display."""
        if self.live is None:
            self.live = Live("", console=self.console, auto_refresh=False)
            self.live.start()
    
    def stop(self):
        """Stop the live display."""
        if self.live:
            self.live.stop()
            self.live = None
    
    def display_in_progress(self, text, speaker="(0)", embedding_count=0):
        """Display an in-progress transcription."""
        self.start()
        
        # Create formatted text
        self.current_text = self._create_formatted_text(
            text, speaker, embedding_count, complete=False
        )
        
        # Update the display
        self.live.update(self.current_text, refresh=True)
    
    def display_complete(self, text, speaker_id, embedding_count=0):
        """Display a complete transcription."""
        # Create formatted text for the complete transcription
        complete_text = self._create_formatted_text(
            text, speaker_id, embedding_count, complete=True
        )
        
        if self.live:
            # Update the display with the final content
            self.live.update(complete_text, refresh=True)
            
            # Stop the live display - this will render the content permanently
            self.stop()
        else:
            # If no live display is active, just print directly
            self.console.print(complete_text)
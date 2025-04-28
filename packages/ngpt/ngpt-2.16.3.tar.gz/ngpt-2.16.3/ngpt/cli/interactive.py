import os
import shutil
import traceback
from .formatters import COLORS
from .renderers import prettify_markdown, prettify_streaming_markdown

# Optional imports for enhanced UI
try:
    from prompt_toolkit import prompt as pt_prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.history import InMemoryHistory
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False

def interactive_chat_session(client, web_search=False, no_stream=False, temperature=0.7, top_p=1.0, max_tokens=None, preprompt=None, prettify=False, renderer='auto', stream_prettify=False, logger=None):
    """Start an interactive chat session with the AI.
    
    Args:
        client: The NGPTClient instance
        web_search: Whether to enable web search capability
        no_stream: Whether to disable streaming
        temperature: Controls randomness in the response
        top_p: Controls diversity via nucleus sampling
        max_tokens: Maximum number of tokens to generate in each response
        preprompt: Custom system prompt to control AI behavior
        prettify: Whether to enable markdown rendering
        renderer: Which markdown renderer to use
        stream_prettify: Whether to enable streaming with prettify
        logger: Logger instance for logging the conversation
    """
    # Get terminal width for better formatting
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 80  # Default fallback
    
    # Improved visual header with better layout
    header = f"{COLORS['cyan']}{COLORS['bold']}🤖 nGPT Interactive Chat Session 🤖{COLORS['reset']}"
    print(f"\n{header}")
    
    # Create a separator line - use a consistent separator length for all lines
    separator_length = min(40, term_width - 10)
    separator = f"{COLORS['gray']}{'─' * separator_length}{COLORS['reset']}"
    print(separator)
    
    # Group commands into categories with better formatting
    print(f"\n{COLORS['cyan']}Navigation:{COLORS['reset']}")
    print(f"  {COLORS['yellow']}↑/↓{COLORS['reset']} : Browse input history")
    
    print(f"\n{COLORS['cyan']}Session Commands:{COLORS['reset']}")
    print(f"  {COLORS['yellow']}history{COLORS['reset']} : Show conversation history")
    print(f"  {COLORS['yellow']}clear{COLORS['reset']}   : Reset conversation")
    print(f"  {COLORS['yellow']}exit{COLORS['reset']}    : End session")
    
    print(f"\n{separator}\n")
    
    # Show logging info if logger is available
    if logger:
        print(f"{COLORS['green']}Logging conversation to: {logger.get_log_path()}{COLORS['reset']}")
    
    # Custom separator - use the same length for consistency
    def print_separator():
        print(f"\n{separator}\n")
    
    # Initialize conversation history
    system_prompt = preprompt if preprompt else "You are a helpful assistant."
    
    # Add markdown formatting instruction to system prompt if prettify is enabled
    if prettify:
        if system_prompt:
            system_prompt += " You can use markdown formatting in your responses where appropriate."
        else:
            system_prompt = "You are a helpful assistant. You can use markdown formatting in your responses where appropriate."
    
    conversation = []
    system_message = {"role": "system", "content": system_prompt}
    conversation.append(system_message)
    
    # Log system prompt if logging is enabled
    if logger and preprompt:
        logger.log("system", system_prompt)
    
    # Initialize prompt_toolkit history
    prompt_history = InMemoryHistory() if HAS_PROMPT_TOOLKIT else None
    
    # Decorative chat headers with rounded corners
    def user_header():
        return f"{COLORS['cyan']}{COLORS['bold']}╭─ 👤 You {COLORS['reset']}"
    
    def ngpt_header():
        return f"{COLORS['green']}{COLORS['bold']}╭─ 🤖 nGPT {COLORS['reset']}"
    
    # Function to display conversation history
    def display_history():
        if len(conversation) <= 1:  # Only system message
            print(f"\n{COLORS['yellow']}No conversation history yet.{COLORS['reset']}")
            return
            
        print(f"\n{COLORS['cyan']}{COLORS['bold']}Conversation History:{COLORS['reset']}")
        print(separator)
        
        # Skip system message
        message_count = 0
        for i, msg in enumerate(conversation):
            if msg["role"] == "system":
                continue
                
            if msg["role"] == "user":
                message_count += 1
                print(f"\n{user_header()}")
                print(f"{COLORS['cyan']}│ [{message_count}] {COLORS['reset']}{msg['content']}")
            elif msg["role"] == "assistant":
                print(f"\n{ngpt_header()}")
                print(f"{COLORS['green']}│ {COLORS['reset']}{msg['content']}")
        
        print(f"\n{separator}")  # Consistent separator at the end
    
    # Function to clear conversation history
    def clear_history():
        nonlocal conversation
        conversation = [{"role": "system", "content": system_prompt}]
        print(f"\n{COLORS['yellow']}Conversation history cleared.{COLORS['reset']}")
        print(separator)  # Add separator for consistency
    
    try:
        while True:
            # Get user input
            if HAS_PROMPT_TOOLKIT:
                # Custom styling for prompt_toolkit
                style = Style.from_dict({
                    'prompt': 'ansicyan bold',
                    'input': 'ansiwhite',
                })
                
                # Create key bindings for Ctrl+C handling
                kb = KeyBindings()
                @kb.add('c-c')
                def _(event):
                    event.app.exit(result=None)
                    raise KeyboardInterrupt()
                
                # Get user input with styled prompt - using proper HTML formatting
                user_input = pt_prompt(
                    HTML("<ansicyan><b>╭─ 👤 You:</b></ansicyan> "),
                    style=style,
                    key_bindings=kb,
                    history=prompt_history
                )
            else:
                user_input = input(f"{user_header()}: {COLORS['reset']}")
            
            # Check for exit commands
            if user_input.lower() in ('exit', 'quit', 'bye'):
                print(f"\n{COLORS['green']}Ending chat session. Goodbye!{COLORS['reset']}")
                break
            
            # Check for special commands
            if user_input.lower() == 'history':
                display_history()
                continue
            
            if user_input.lower() == 'clear':
                clear_history()
                continue
            
            # Skip empty messages but don't raise an error
            if not user_input.strip():
                print(f"{COLORS['yellow']}Empty message skipped. Type 'exit' to quit.{COLORS['reset']}")
                continue
            
            # Add user message to conversation
            user_message = {"role": "user", "content": user_input}
            conversation.append(user_message)
            
            # Log user message if logging is enabled
            if logger:
                logger.log("user", user_input)
            
            # Print assistant indicator with formatting
            if not no_stream and not stream_prettify:
                print(f"\n{ngpt_header()}: {COLORS['reset']}", end="", flush=True)
            elif not stream_prettify:
                print(f"\n{ngpt_header()}: {COLORS['reset']}", flush=True)
            
            # If prettify is enabled with regular streaming
            if prettify and not no_stream and not stream_prettify:
                print(f"\n{COLORS['yellow']}Note: Streaming disabled to enable markdown rendering.{COLORS['reset']}")
                print(f"\n{ngpt_header()}: {COLORS['reset']}", flush=True)
                should_stream = False
            else:
                # Regular behavior with stream-prettify taking precedence
                should_stream = not no_stream
            
            # Setup for stream-prettify
            stream_callback = None
            live_display = None
            
            if stream_prettify and should_stream:
                # Get the correct header for interactive mode
                header = ngpt_header()
                live_display, stream_callback = prettify_streaming_markdown(renderer, is_interactive=True, header_text=header)
                if not live_display:
                    # Fallback to normal prettify if live display setup failed
                    prettify = True
                    stream_prettify = False
                    should_stream = False
                    print(f"{COLORS['yellow']}Falling back to regular prettify mode.{COLORS['reset']}")
            
            # Start live display if using stream-prettify
            if stream_prettify and live_display:
                live_display.start()
            
            # Get AI response with conversation history
            response = client.chat(
                prompt=user_input,
                messages=conversation,
                stream=should_stream,
                web_search=web_search,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                markdown_format=prettify or stream_prettify,
                stream_callback=stream_callback
            )
            
            # Stop live display if using stream-prettify
            if stream_prettify and live_display:
                live_display.stop()
            
            # Add AI response to conversation history
            if response:
                assistant_message = {"role": "assistant", "content": response}
                conversation.append(assistant_message)
                
                # Print response if not streamed (either due to no_stream or prettify)
                if no_stream or prettify:
                    if prettify:
                        prettify_markdown(response, renderer)
                    else:
                        print(response)
                
                # Log AI response if logging is enabled
                if logger:
                    logger.log("assistant", response)
            
            # Print separator between exchanges
            print_separator()
            
    except KeyboardInterrupt:
        print(f"\n\n{COLORS['yellow']}Chat session interrupted by user.{COLORS['reset']}")
    except Exception as e:
        print(f"\n{COLORS['yellow']}Error in chat session: {str(e)}{COLORS['reset']}")
        if os.environ.get("NGPT_DEBUG"):
            traceback.print_exc() 
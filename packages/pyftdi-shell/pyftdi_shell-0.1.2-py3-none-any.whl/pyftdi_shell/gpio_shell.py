from pyftdi.gpio import GpioController

class GPIOShell:
    def __init__(self, device_url: str, direction_mask: int):
        """Initialize the GPIO shell with the given FTDI device URL and direction mask."""
        self.device_url = device_url
        self.direction_mask = direction_mask
        self.gpio = GpioController()
        self.configure()

    def configure(self):
        """Configure the GPIO controller to connect to the FTDI device."""
        self.gpio.configure(self.device_url, direction=self.direction_mask)
        print("FTDI GPIO Interface Ready. Type 'exit' to quit.")

    def run(self):
        """Run the interactive shell for user commands."""
        while True:
            try:
                command = input("> ").strip()
                if command.lower() in ['exit', 'quit', 'q']:
                    break

                parts = command.split()
                if not parts:
                    continue

                cmd_type = parts[0].lower()
                if cmd_type == 'set':
                    self.handle_set(parts)
                elif cmd_type == 'clear':
                    self.handle_clear(parts)
                elif cmd_type == 'read':
                    self.handle_read(parts)
                else:
                    print("Unknown command. Use 'set', 'clear', or 'read'.")
            
            except Exception as e:
                print(f"Error: {e}")

    def handle_set(self, parts):
        """Handle the set command to set GPIO pins high."""
        if len(parts) < 2:
            print("Usage: set <pin_number>")
            return
        
        pin_number = int(parts[1], 0)
        current_state = self.gpio.read()
        new_state = current_state | (1 << pin_number)
        self.gpio.write(new_state)
        print(f"Pin {pin_number} set high.")

    def handle_clear(self, parts):
        """Handle the clear command to set GPIO pins low."""
        if len(parts) < 2:
            print("Usage: clear <pin_number>")
            return
        
        pin_number = int(parts[1], 0)
        current_state = self.gpio.read()
        new_state = current_state & ~(1 << pin_number)
        self.gpio.write(new_state)
        print(f"Pin {pin_number} set low.")

    def handle_read(self, parts):
        """Handle the read command to read GPIO pin states."""
        current_state = self.gpio.read()
        print(f"Current GPIO state: {bin(current_state)}")

# Example usage:
# if __name__ == "__main__":
#     device_url = "ftdi://ftdi:2232h/1"  # Replace with your actual device URL
#     direction_mask = 0xFF  # Set all pins as outputs; adjust as needed
#     shell = GPIOShell(device_url, direction_mask)
#     shell.run()

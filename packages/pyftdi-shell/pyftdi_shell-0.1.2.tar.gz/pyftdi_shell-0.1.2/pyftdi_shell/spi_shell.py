from pyftdi.spi import SpiController

class SPIShell:
    def __init__(self, device_url: str):
        """Initialize the SPI shell with the given FTDI device URL."""
        self.device_url = device_url
        self.spi = SpiController()
        self.configure()

    def configure(self):
        """Configure the SPI controller to connect to the FTDI device."""
        self.spi.configure(self.device_url)
        print("FTDI SPI Interface Ready. Type 'exit' to quit.")

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
                if cmd_type == 'write':
                    self.handle_write(parts)
                elif cmd_type == 'read':
                    self.handle_read(parts)
                else:
                    print("Unknown command. Use 'write' or 'read'.")
            
            except Exception as e:
                print(f"Error: {e}")

    def handle_write(self, parts):
        """Handle the write command."""
        if len(parts) < 3:
            print("Usage: write <cs> <data...>")
            return
        
        cs = int(parts[1], 0)
        data = [int(x, 0) for x in parts[2:]]

        slave = self.spi.get_port(cs)
        slave.write(bytes(data))

    def handle_read(self, parts):
        """Handle the read command."""
        if len(parts) != 3:
            print("Usage: read <cs> <length>")
            return
        
        cs = int(parts[1], 0)
        length = int(parts[2], 0)

        slave = self.spi.get_port(cs)
        data = slave.read(length)

        # Format read data as hex values for pretty print
        hex_data = [f"0x{byte:02X}" for byte in data]
        print(f"Read: {hex_data}")
